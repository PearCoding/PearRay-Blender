import bpy


from bl_ui.properties_data_camera import CameraButtonsPanel


class CAMERA_PT_pr_cam_settings(CameraButtonsPanel, bpy.types.Panel):
    bl_label = "PearRay Settings"
    COMPAT_ENGINES = {'PEARRAY_RENDER'}

    def draw(self, context):
        layout = self.layout

        cam = context.camera

        layout.prop(cam.pearray, "zoom")

        split = layout.split()

        split.prop(cam.pearray, "fstop")
        split.prop(cam.pearray, "apertureRadius")


register, unregister = bpy.utils.register_classes_factory(
    [CAMERA_PT_pr_cam_settings])
