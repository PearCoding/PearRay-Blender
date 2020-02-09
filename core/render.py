import bpy
import os
import sys
import time
import subprocess
import threading
import re
import importlib
from collections import deque

from .. import export

pearray_package = __import__(__name__.split('.')[0])


class PearRayRender(bpy.types.RenderEngine):
    bl_idname = 'PEARRAY_RENDER'
    bl_label = "PearRay"
    #bl_use_preview = True
    bl_use_exclude_layers = True
    bl_use_eevee_viewport = True

    @staticmethod
    def _setup_package():
        addon_prefs = bpy.context.preferences.addons[pearray_package.__package__].preferences

        if addon_prefs.package_dir:
            sys.path.append(bpy.path.resolve_ncase(
                bpy.path.abspath(addon_prefs.package_dir)))

        return importlib.import_module("pypearray")

    def check_break(self, renderer=None):
        # User interrupts the rendering
        if self.test_break():
            try:
                if renderer is not None:
                    renderer.stop()
                print("<<< PEARRAY INTERRUPTED >>>")
            except OSError:
                pass
            return True

        if renderer is not None and renderer.finished:
            return True

        return False

    def _proc_wait(self, renderer):
        time.sleep(0.1)
        return not self.check_break(renderer)

    def _handle_render_stat(self, renderer):
        stat = renderer.status

        line = "Pass %s S %i R %i EH %i BH %i" % (renderer.currentPass+1,
                                                  stat['global.pixel_sample_count'],
                                                  stat['global.ray_count'],
                                                  stat['global.entity_hit_count'],
                                                  stat['global.background_hit_count'])

        self.update_stats("", "PearRay: Rendering [%s]..." % (line))
        self.update_progress(stat.percentage)

    def render(self, depsgraph):
        addon_prefs = bpy.context.preferences.addons[pearray_package.__package__].preferences
        pr = PearRayRender._setup_package()
        pr.Logger.instance.verbosity = pr.LogLevel.DEBUG if addon_prefs.verbose else pr.LogLevel.INFO

        if addon_prefs.profile:
            pr.Profiler.start()

        import tempfile
        scene = depsgraph.scene
        render = scene.render

        x = int(render.resolution_x * render.resolution_percentage * 0.01)
        y = int(render.resolution_y * render.resolution_percentage * 0.01)

        print("<<< START PEARRAY >>>")
        blendSceneName = bpy.data.filepath.split(os.path.sep)[-1].split(".")[0]
        if not blendSceneName:
            blendSceneName = "blender_scene"

        sceneFile = ""
        renderPath = bpy.path.resolve_ncase(
            bpy.path.abspath(render.frame_path()))
        if not os.path.isdir(renderPath):
            renderPath = os.path.dirname(renderPath)

        if not renderPath:
            renderPath = tempfile.gettempdir()

        if not os.path.exists(renderPath):
            os.makedirs(renderPath)

        if scene.pearray.keep_prc:
            sceneFile = os.path.normpath(renderPath + "/scene.prc")
        else:
            sceneFile = tempfile.NamedTemporaryFile(suffix=".prc").name

        print(sceneFile)

        fileLog = pr.FileLogListener()
        fileLog.open(os.path.normpath(renderPath + "/%s.log" % time.time()))
        pr.Logger.instance.addListener(fileLog)

        if self.check_break():
            return

        self.update_stats("", "PearRay: Exporting data")
        scene_exporter = export.Exporter(sceneFile, depsgraph)
        scene_exporter.write_scene(pr)

        if self.check_break():
            return

        self.update_stats("", "PearRay: Starting render")
        scene_opts = pr.SceneLoader.LoadOptions()
        scene_opts.PluginPath = addon_prefs.package_dir
        scene_opts.WorkingDir = renderPath

        environment = pr.SceneLoader.loadFromFile(sceneFile, scene_opts)
        if not environment:
            self.report(
                {'ERROR'}, "PearRay: could not load environment from file")
            print("<<< PEARRAY FAILED >>>")
            return

        if self.check_break():
            return

        toneMapper = pr.ToneMapper()
        toneMapper.colorMode = pr.ToneColorMode.SRGB
        toneMapper.gammaMode = pr.ToneGammaMode.NONE
        toneMapper.mapperMode = pr.ToneMapperMode.NONE

        colorBuffer = pr.ColorBuffer(x, y, pr.ColorBufferMode.RGBA)

        environment.renderSettings.filmWidth = x
        environment.renderSettings.filmHeight = y

        integrator = environment.createSelectedIntegrator()
        if not integrator:
            self.report(
                {'ERROR'}, "PearRay: could not create pearray integrator instance")
            print("<<< PEARRAY FAILED >>>")
            pr.Logger.instance.removeListener(fileLog)
            del fileLog
            return

        if self.check_break():
            return

        factory = environment.createRenderFactory()
        if not factory:
            self.report(
                {'ERROR'}, "PearRay: could not create pearray render factory instance")
            print("<<< PEARRAY FAILED >>>")
            pr.Logger.instance.removeListener(fileLog)
            del fileLog
            return

        if self.check_break():
            return

        renderer = factory.create(integrator)

        if not renderer:
            self.report(
                {'ERROR'}, "PearRay: could not create pearray render instance")
            print("<<< PEARRAY FAILED >>>")
            pr.Logger.instance.removeListener(fileLog)
            del fileLog
            return

        environment.setup(renderer)

        if addon_prefs.verbose:
            environment.dumpInformation()

        threads = 0
        if render.threads_mode == 'FIXED':
            threads = render.threads

        print("<<< PEARRAY CONFIGURED >>>")
        if self.check_break():
            return

        renderer.start(render.tile_x, render.tile_y, threads)

        print("<<< PEARRAY STARTED >>>")

        # Update image
        result = self.begin_result(0, 0, x, y)
        layer = result.layers[0]

        def update_image():
            colorBuffer.map(
                toneMapper, environment.spectrumDescriptor, renderer.output.spectral)
            colorBuffer.flipY()
            layer.passes["Combined"].rect = colorBuffer.asLinearWithChannels()
            self.update_result(result)

        update_image()

        prog_start = time.time()
        img_start = time.time()
        while self._proc_wait(renderer):
            prog_end = time.time()
            if addon_prefs.show_progress_interval < (prog_end - prog_start):
                self._handle_render_stat(renderer)
                prog_start = prog_end

            if addon_prefs.show_image_interval > 0:
                img_end = time.time()
                if addon_prefs.show_image_interval < (img_end - img_start):
                    update_image()
                    img_start = img_end

        update_image()
        self.end_result(result)

        renderer.notifyEnd()
        environment.save(renderer, toneMapper, True)

        # The order here is important!
        # FIXME: This should be handled internally!!!
        del integrator
        del renderer
        del factory
        del environment

        if not scene.pearray.keep_prc:
            os.remove(sceneFile)

        if addon_prefs.profile:
            pr.Profiler.stop()
            pr.Profiler.dumpToFile(renderPath + "/pr_profile.prof")

        pr.Logger.instance.removeListener(fileLog)
        del fileLog

        self.update_stats("", "")
        print("<<< PEARRAY FINISHED >>>")


def register():
    bpy.utils.register_class(PearRayRender)


def unregister():
    bpy.utils.unregister_class(PearRayRender)
