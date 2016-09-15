import bpy


from bl_ui.properties_render_layer import RenderLayerButtonsPanel


from bl_ui import properties_render_layer
properties_render_layer.RENDERLAYER_PT_layers.COMPAT_ENGINES.add('PEARRAY_RENDER')
del properties_render_layer



class RENDERLAYER_PT_pr_layer_options(RenderLayerButtonsPanel, bpy.types.Panel):
    bl_label = "Layer"
    COMPAT_ENGINES = {'PEARRAY_RENDER'}

    def draw(self, context):
        layout = self.layout

        scene = context.scene
        rd = scene.render
        rl = rd.layers.active

        split = layout.split()

        col = split.column()
        col.prop(scene, "layers", text="Scene")
        col.prop(rl, "layers_exclude", text="Exclude")

        col = split.column()
        col.prop(rl, "layers", text="Layer")
        col.prop(rl, "layers_zmask", text="Mask Layer")

        split = layout.split()

        col = split.column()
        col.label(text="Material:")
        col.prop(rl, "material_override", text="")