from bl_ui.properties_output import RenderOutputButtonsPanel
from bl_ui.properties_view_layer import ViewLayerButtonsPanel
import bpy


class RENDER_PT_pr_output(RenderOutputButtonsPanel, bpy.types.Panel):
    bl_label = "Output"
    COMPAT_ENGINES = {'PEARRAY_RENDER'}

    def draw(self, context):
        layout = self.layout

        rd = context.scene.render
        layout.prop(rd, "filepath", text="")


class VIEWLAYER_OP_pr_lpe_actions(bpy.types.Operator):
    bl_idname = "pr.lpe_actions"
    bl_label = "Adds or removes lpes"

    action: bpy.props.EnumProperty(
        name="Action",
        items=(('REMOVE', 'Remove', ''), ('ADD', 'Add', ''))
    )

    def invoke(self, context, event):
        scene = context.scene
        rl2 = scene.pearray_layer
        idx = rl2.active_lpe_index

        if idx < len(rl2.lpes):
            if self.action == 'REMOVE':
                rl2.active_lpe_index -= 1
                rl2.lpes.remove(idx)

        if self.action == 'ADD':
            rl2.lpes.add()
            rl2.active_lpe_index = len(rl2.lpes)-1

        return {'FINISHED'}


class VIEWLAYER_UL_pr_lpe_entry(bpy.types.UIList):
    use_filter_show = False
    layout_type = 'COMPACT'

    def draw_item(self, context, layout, data, item, icon, active_data, active_propname):
        el = layout.split().row(align=True)

        el.label(text='', icon='RENDER_RESULT')
        el.prop(item, "channel", text="")
        el.prop(item, "expression", text="")


class VIEWLAYER_PT_pr_lpe(ViewLayerButtonsPanel, bpy.types.Panel):
    bl_label = "LPEs"
    bl_options = {'DEFAULT_CLOSED'}
    COMPAT_ENGINES = {'PEARRAY_RENDER'}

    def draw(self, context):
        layout = self.layout

        scene = context.scene
        rl2 = scene.pearray_layer

        row = layout.row()
        row.template_list("VIEWLAYER_UL_pr_lpe_entry",
                          "", rl2, "lpes", rl2, "active_lpe_index")
        col = row.column(align=True)
        col.operator("pr.lpe_actions", icon='ADD', text="").action = 'ADD'
        col.operator("pr.lpe_actions", icon='REMOVE',
                     text="").action = 'REMOVE'


class VIEWLAYER_PT_pr_aovs(ViewLayerButtonsPanel, bpy.types.Panel):
    bl_label = "AOVs"
    bl_options = {'DEFAULT_CLOSED'}
    COMPAT_ENGINES = {'PEARRAY_RENDER'}

    def draw(self, context):
        layout = self.layout

        scene = context.scene
        rl = scene.view_layers[0]
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


class RENDER_PT_pr_export_settings(RenderOutputButtonsPanel, bpy.types.Panel):
    bl_label = "Export Settings"
    bl_options = {'DEFAULT_CLOSED'}
    COMPAT_ENGINES = {'PEARRAY_RENDER'}

    def draw_header(self, context):
        pass

    def draw(self, context):
        layout = self.layout
        scene = context.scene

        layout.prop(scene.pearray, "keep_prc")
        layout.prop(scene.pearray, "beautiful_prc")
        layout.prop(scene.pearray, "color_format")


register, unregister = bpy.utils.register_classes_factory([
    RENDER_PT_pr_output,
    RENDER_PT_pr_export_settings,
    VIEWLAYER_OP_pr_lpe_actions,
    VIEWLAYER_UL_pr_lpe_entry,
    VIEWLAYER_PT_pr_lpe,
    VIEWLAYER_PT_pr_aovs,
])
