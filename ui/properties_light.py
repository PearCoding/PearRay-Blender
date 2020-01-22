import bpy


from bl_ui.properties_data_light import DataButtonsPanel
from .properties_material import color_template


class DATA_PT_pr_light(DataButtonsPanel, bpy.types.Panel):
    bl_label = "Light"
    COMPAT_ENGINES = {'PEARRAY_RENDER'}

    def draw(self, context):
        layout = self.layout

        light = context.light

        layout.prop(light, "type", expand=True)
        if light.type == 'SPOT':
            layout.label(
                'Spot light will be converted to point light!', icon='INFO')
        elif light.type == 'HEMI':
            layout.label(
                'Hemi light will be converted to area light!', icon='INFO')

        split = layout.split()

        col = split.column(align=True)
        col.separator()
        color_template(light, col, "color")

        if light.type == 'POINT' or light.type == 'SPOT':
            col.separator()
            col.prop(light.pearray, 'point_radius')
        elif light.type == 'HEMI' or light.type == 'AREA':
            col.separator()
            col2 = col.column(align=True)
            col2.row().prop(light, "shape", expand=True)
            sub = col2.row(align=True)

            if light.shape == 'SQUARE':
                sub.prop(light, "size")
            elif light.shape == 'RECTANGLE':
                sub.prop(light, "size", text="Size X")
                sub.prop(light, "size_y", text="Size Y")

        if light.type == 'POINT' or light.type == 'SPOT' or light.type == 'HEMI' or light.type == 'AREA':
            col.separator()
            col.prop(light.pearray, 'camera_visible')


def register():
    bpy.utils.register_class(DATA_PT_pr_light)


def unregister():
    bpy.utils.unregister_class(DATA_PT_pr_light)
