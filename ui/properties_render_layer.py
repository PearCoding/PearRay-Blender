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


class RENDERLAYER_OP_pr_layer_lpe_actions(bpy.types.Operator):
    bl_idname = "pr.lpe_actions"
    bl_label = "Adds or removes lpes"

    action = bpy.props.EnumProperty(
        items=(('REMOVE', 'Remove', ''), ('ADD', 'Add', ''))
    )

    def invoke(self, context, event):
        scene = context.scene
        rl2 = scene.pearray_layer
        idx = rl2.active_lpe_index

        try:
            item = rl2.lpes[idx]
        except IndexError:
            pass
        else:
            if self.action == 'REMOVE':
                rl2.active_lpe_index -= 1
                rl2.lpes.remove(idx)

        if self.action == 'ADD':
            rl2.lpes.add()
            rl2.active_lpe_index = len(rl2.lpes)-1

        return {'FINISHED'}


class RENDERLAYER_PT_pr_layer_lpe_entry(bpy.types.UIList):
    use_filter_show = False
    layout_type = 'COMPACT'

    def draw_item(self, context, layout, data, item, icon, active_data, active_propname):
        el = layout.split().row(align=True)

        el.label('', icon='RENDER_RESULT')
        el.prop(item, "channel", text="")
        el.prop(item, "expression", text="")


class RENDERLAYER_PT_pr_layer_lpe(RenderLayerButtonsPanel, bpy.types.Panel):
    bl_label = "LPEs"
    bl_options = {'DEFAULT_CLOSED'}
    COMPAT_ENGINES = {'PEARRAY_RENDER'}

    def draw(self, context):
        layout = self.layout

        scene = context.scene
        rl2 = scene.pearray_layer

        row = layout.row()
        row.template_list("RENDERLAYER_PT_pr_layer_lpe_entry", "", rl2, "lpes", rl2, "active_lpe_index")
        col = row.column(align=True)
        col.operator("pr.lpe_actions", icon='ZOOMIN', text="").action = 'ADD'
        col.operator("pr.lpe_actions", icon='ZOOMOUT', text="").action = 'REMOVE'


class RENDERLAYER_PT_pr_layer_aovs(RenderLayerButtonsPanel, bpy.types.Panel):
    bl_label = "AOVs"
    bl_options = {'DEFAULT_CLOSED'}
    COMPAT_ENGINES = {'PEARRAY_RENDER'}

    def draw(self, context):
        layout = self.layout

        scene = context.scene
        rd = scene.render
        rl = rd.layers.active
        rl2 = scene.pearray_layer

        split = layout.split()

        col = split.column()
        col.prop(rl, "use_pass_combined")
        col.prop(rl, "use_pass_z")
        col.prop(rl, "use_pass_normal")
        col.prop(rl2, "aov_ng")
        col.prop(rl2, "aov_nx")
        col.prop(rl2, "aov_ny")
        col.prop(rl, "use_pass_vector")
        col.prop(rl, "use_pass_uv")

        col = split.column()
        col.prop(rl2, "aov_p")
        col.prop(rl2, "aov_t")
        col.prop(rl2, "aov_samples")
        col.prop(rl2, "aov_feedback")
        col.prop(rl, "use_pass_object_index")
        col.prop(rl, "use_pass_material_index")
        col.prop(rl2, "aov_emission_index")
        col.prop(rl2, "aov_displace_index")

        layout.separator()
        split = layout.split()
        split.prop(rl2, "raw_spectral")

        layout.separator()
        split = layout.split()
        split.prop(rl2, "separate_files")
