import bpy


class RenderButtonsPanel():
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "render"
    # COMPAT_ENGINES must be defined in each subclass, external engines can add themselves here

    @classmethod
    def poll(cls, context):
        rd = context.scene.render
        return (rd.engine in getattr(cls, 'COMPAT_ENGINES', []))


class RENDER_PT_pr_render(RenderButtonsPanel, bpy.types.Panel):
    bl_label = "Render"
    COMPAT_ENGINES = {'PEARRAY_RENDER'}

    def draw(self, context):
        layout = self.layout
        scene = context.scene

        row = layout.row(align=True)
        row.operator("render.render", text="Render", icon='RENDER_STILL')
        row.operator("render.render", text="Animation",
                     icon='RENDER_ANIMATION').animation = True
        row.operator("pr.export", text="Export", icon='FILE_BLANK')  # TODO

        layout.separator()

        split = layout.split(factor=0.33)
        split.label(text="Tile Mode:")
        row = split.row(align=True)
        row.prop(context.scene.pearray, "render_tile_mode", expand=True)

        layout.separator()
        layout.prop(scene.pearray, "integrator")

        layout.separator()
        layout.prop(context.scene.pearray, "pixel_filter_mode")
        layout.prop(context.scene.pearray, "pixel_filter_radius")


class RENDER_PT_pr_performance(RenderButtonsPanel, bpy.types.Panel):
    bl_label = "Performance"
    bl_options = {'DEFAULT_CLOSED'}
    COMPAT_ENGINES = {'PEARRAY_RENDER'}

    def draw(self, context):
        layout = self.layout

        rd = context.scene.render

        split = layout.split()

        col = split.column(align=True)
        col.label(text="Threads:")
        col.row(align=True).prop(rd, "threads_mode", expand=True)
        sub = col.column(align=True)
        sub.enabled = rd.threads_mode == 'FIXED'
        sub.prop(rd, "threads")

        col.label(text="Tile Size:")
        col.prop(rd, "tile_x", text="X")
        col.prop(rd, "tile_y", text="Y")


class RENDER_PT_pr_sampler(RenderButtonsPanel, bpy.types.Panel):
    bl_label = "Sampler"
    COMPAT_ENGINES = {'PEARRAY_RENDER'}

    def draw(self, context):
        layout = self.layout
        scene = context.scene

        layout.prop(scene.pearray, "sampler_max_samples", text="SPP")
        layout.separator()
        layout.prop(scene.pearray, "sampler_aa_mode", text="AA")
        layout.prop(scene.pearray, "sampler_lens_mode", text="Lens")
        layout.prop(scene.pearray, "sampler_time_mode", text="Time")
        layout.prop(scene.pearray, "sampler_time_mapping_mode", expand=True)
        layout.prop(scene.pearray, "sampler_time_scale")
        layout.prop(scene.pearray, "sampler_spectral_mode", text="Spectral")


class RENDER_PT_pr_integrator(RenderButtonsPanel, bpy.types.Panel):
    bl_label = "Integrator"
    COMPAT_ENGINES = {'PEARRAY_RENDER'}

    def draw(self, context):
        layout = self.layout
        scene = context.scene

        if scene.pearray.integrator == 'DIRECT':
            col = layout.column(align=True)
            col.prop(scene.pearray, "max_ray_depth")
            col.prop(scene.pearray, "soft_max_ray_depth")
            layout.prop(scene.pearray, "max_light_samples")
        elif scene.pearray.integrator == 'BIDIRECT':
            col = layout.column(align=True)
            col.prop(scene.pearray, "max_ray_depth")
            col.prop(scene.pearray, "soft_max_ray_depth")
            col = layout.column(align=True)
            col.prop(scene.pearray, "max_light_ray_depth")
            col.prop(scene.pearray, "soft_max_light_ray_depth")
        elif scene.pearray.integrator == 'PPM':
            layout.prop(scene.pearray, "ppm_photons_per_pass")
            col = layout.column(align=True)
            col.prop(scene.pearray, "max_ray_depth")
            col.prop(scene.pearray, "soft_max_ray_depth")
            col = layout.column(align=True)
            col.prop(scene.pearray, "max_light_ray_depth")
            col.prop(scene.pearray, "soft_max_light_ray_depth")
        elif scene.pearray.integrator == 'AO':
            layout.prop(scene.pearray, "ao_sample_count")
        elif scene.pearray.integrator == 'VF':
            layout.prop(scene.pearray, "vf_mode")
            layout.prop(scene.pearray, "vf_apply_weighting")


register, unregister = bpy.utils.register_classes_factory([
    RENDER_PT_pr_render,
    RENDER_PT_pr_performance,
    RENDER_PT_pr_sampler,
    RENDER_PT_pr_integrator
])
