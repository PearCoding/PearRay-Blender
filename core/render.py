import bpy
import os
import sys
import time
import subprocess
import queue
import threading

from .. import export

pearray_package = __import__(__name__.split('.')[0])


class PearRayRender(bpy.types.RenderEngine):
    bl_idname = 'PEARRAY_RENDER'
    bl_label = "PearRay"
    #bl_use_preview = True
    bl_use_exclude_layers = True
    
    DELAY = 2 # seconds

    @staticmethod
    def _locate_binary():
        addon_prefs = bpy.context.user_preferences.addons[pearray_package.__package__].preferences

        # Use the system preference if its set.
        pearray_binary = addon_prefs.executable
        if pearray_binary:
            if os.path.exists(pearray_binary):
                return pearray_binary
            else:
                self.report({'ERROR'}, "User Preferences path to pearray %r NOT FOUND, checking $PATH" % pearray_binary)

        # Windows Only
        if sys.platform[:3] == "win":
            import winreg
            win_reg_key = winreg.OpenKey(winreg.HKEY_CURRENT_USER,
                "Software\\PearRay\\v0.9\\Windows")
            win_home = winreg.QueryValueEx(win_reg_key, "Home")[0]
            
            pearray_binary = os.path.join(win_home, "bin", "pearray.exe")
            if os.path.exists(pearray_binary):
                return pearray_binary

        # search the path all os's
        pearray_binary_default = "pearray"

        os_path_ls = os.getenv("PATH").split(':') + [""]

        for dir_name in os_path_ls:
            pearray_binary = os.path.join(dir_name, pearray_binary_default)
            if os.path.exists(pearray_binary):
                return pearray_binary
        return ""


    def _proc_wait(self):
        time.sleep(self.DELAY)

        # User interrupts the rendering
        if self.test_break():
            try:
                self._process.terminate()
                print("<<< PEARRAY INTERRUPTED >>>")
            except OSError:
                pass
            return False

        poll_result = self._process.poll()

        # PearRay process is finised, one way or the other
        if poll_result is not None:
            if poll_result < 0:
                self.report({'ERROR'}, "PearRay process failed with return code %i" % poll_result)
                self.update_stats("", "PearRay: Failed")
            return False

        return True


    def _enqueue_output(out, queue, stop_event):
        for line in iter(out.readline, b''):
            if stop_event.is_set():
                break
            queue.put(line)
        out.close()


    def _handle_render_stat(self, percent, q):
        while True:
            try:
                line = q.get_nowait()
            except queue.Empty:
                break
            else:
                if line == 'preprocess':
                    pass
                else:
                    try:
                        p = float(line)
                        if p > percent:
                            percent = p
                    except ValueError:
                        pass

        if percent == -1:
            self.update_stats("", "PearRay: Preprocessing...")
            self.update_progress(0)
        else:
            self.update_stats("", "PearRay: Rendering [%3.2f%%]..." % (percent*100))
            self.update_progress(percent)
                
        return percent

    def render(self, scene):
        import tempfile

        render = scene.render

        print("<<< START PEARRAY >>>")
        blendSceneName = bpy.data.filepath.split(os.path.sep)[-1].split(".")[0]
        if not blendSceneName:
            blendSceneName = "blender_scene"

        sceneFile = ""
        iniFile = ""
        renderPath = ""

        # has to be called to update the frame on exporting animations
        scene.frame_set(scene.frame_current)

        renderPath = bpy.path.resolve_ncase(bpy.path.abspath(render.filepath))

        if scene.pearray.keep_prc:
            sceneFile = os.path.normpath(renderPath + "/scene.prc")
            iniFile = os.path.normpath(renderPath + "/scene.ini")
        else:
            sceneFile = tempfile.NamedTemporaryFile(suffix=".prc").name
            iniFile = tempfile.NamedTemporaryFile(suffix=".ini").name

        image_name = "image"
        image_ext = {
                'BMP': 'bmp',
                'PNG': 'png',
                'JPEG': 'jpg',
                'JPEG2000': 'jp2',
                'TARGA': 'tga',
                'OPEN_EXR_MULTILAYER': 'exr',
                'OPEN_EXR': 'exr',
                'HDR': 'hdr',
                'TIFF': 'tiff',
            }.get(render.image_settings.file_format, 'NONE')
        if image_ext == 'NONE':
            self.report({'WARNING'}, "Couldn't work with choosen extension. Setting it back to png")
            image_ext = 'png'
        
        self.update_stats("", "PearRay: Exporting data from Blender")
        ini_exporter = export.Exporter(iniFile, scene)
        ini_exporter.write_ini()
        scene_exporter = export.Exporter(sceneFile, scene)
        scene_exporter.write_scene()

        self.update_stats("", "PearRay: Starting render")
        pearray_binary = PearRayRender._locate_binary()
        if not pearray_binary:
            self.report({'ERROR'}, "PearRay: could not execute pearray, possibly PearRay isn't installed")
            print("<<< PEARRAY FAILED >>>")
            return

        args = [sceneFile,
                renderPath, 
                "-q",# be quiet
                "-C",
                iniFile,
                "--img-update=" + str(self.DELAY), # Updates image while rendering
                "--img-ext=%s" % image_ext,
                "-v",
                ]
        addon_prefs = bpy.context.user_preferences.addons[pearray_package.__package__].preferences
        if addon_prefs.show_progress:
            args.append("-p")# show progress (ignores quiet option)

        if not scene.pearray.debug_mode == 'NONE':
            args.append("--debug=%s" % scene.pearray.debug_mode.lower())
        
        if not os.path.exists(renderPath):
            os.makedirs(renderPath)
        output_image = os.path.normpath(renderPath + "/" + image_name + "." + image_ext)

        if os.path.exists(output_image):
            os.remove(output_image)
        
        # Start Rendering!
        try:
            self._process = subprocess.Popen([pearray_binary] + args,
                                             stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        except OSError:
            self.report({'ERROR'}, "PearRay: could not execute '%s'" % pearray_binary)
            import traceback
            traceback.print_exc()
            print ("<<< PEARRAY FAILED >>>")
            return

        else:
            print ("<<< PEARRAY STARTED >>>")
            print ("Command line arguments passed: " + str(args))

        # Update image
        x = int(render.resolution_x * render.resolution_percentage * 0.01)
        y = int(render.resolution_y * render.resolution_percentage * 0.01)
        xmin = int(render.border_min_x * x)
        ymin = int(render.border_min_y * y)
        xmax = int(render.border_max_x * x)
        ymax = int(render.border_max_y * y)
        result = self.begin_result(0, 0, x, y)
        layer = result.layers[0]

        time.sleep(self.DELAY)

        def update_image():# FIXME: How do we prevent crashes? -> Bus Error/Segmentation Faults
            try:
                layer.load_from_file(output_image)
                self.update_result(result)
            except RuntimeError:
                pass
        
        update_image()

        # Line handler
        if addon_prefs.show_progress:
            stdout_queue = queue.Queue()
            stdout_thread_stop = threading.Event()
            stdout_thread = threading.Thread(target=PearRayRender._enqueue_output, args=(self._process.stdout, stdout_queue, stdout_thread_stop))
            stdout_thread.daemon = True # thread dies with the program
            stdout_thread.start()

        prev_size = -1
        prev_mtime = -1
        percent = -1
        while self._proc_wait():
            if addon_prefs.show_progress:
                percent = self._handle_render_stat(percent, stdout_queue)
            else:
                self.update_stats("", "PearRay: Rendering...")

            if os.path.exists(output_image):
                new_size = os.path.getsize(output_image)
                new_mtime = os.path.getmtime(output_image)

                if new_size != prev_size or new_mtime != prev_mtime:
                    update_image()
                    prev_size = new_size
                    prev_mtime = new_mtime

        if addon_prefs.show_progress:
            stdout_thread_stop.set()
            stdout_thread.join()

        update_image()
        self.end_result(result)

        if not scene.pearray.keep_prc:
            os.remove(sceneFile)
        
        self.update_stats("", "")
        print("<<< PEARRAY FINISHED >>>")