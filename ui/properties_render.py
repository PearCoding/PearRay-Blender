import bpy


from bl_ui import properties_render
properties_render.RENDER_PT_dimensions.COMPAT_ENGINES.add('PEARRAY_RENDER')
del properties_render


class RenderButtonsPanel():
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "render"
    # COMPAT_ENGINES must be defined in each subclass, external engines can add themselves here

    @classmethod
    def poll(cls, context):
        rd = context.scene.render
        return (rd.use_game_engine is False) and (rd.engine in cls.COMPAT_ENGINES)


class RENDER_PT_pr_render(RenderButtonsPanel, bpy.types.Panel):
    bl_label = "Render"
    COMPAT_ENGINES = {'PEARRAY_RENDER'}

    def draw(self, context):
        layout = self.layout

        rd = context.scene.render
        scene = context.scene

        row = layout.row(align=True)
        row.operator("render.render", text="Render", icon='RENDER_STILL')
        row.operator("render.render", text="Animation", icon='RENDER_ANIMATION').animation = True
        row.operator("pearray.run_rayview", text="RayView", icon='EXPORT')

        split = layout.split(percentage=0.33)

        split.label(text="Display:")
        row = split.row(align=True)
        row.prop(rd, "display_mode", text="")
        row.prop(rd, "use_lock_interface", icon_only=True)

        layout.separator()

        layout.prop(scene.pearray, "integrator")
        layout.prop(scene.pearray, "debug_mode")
        layout.prop(scene.pearray, "incremental")
        layout.prop(scene.pearray, "max_ray_depth")


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


class RENDER_PT_pr_output(RenderButtonsPanel, bpy.types.Panel):
    bl_label = "Output"
    COMPAT_ENGINES = {'PEARRAY_RENDER'}

    def draw(self, context):
        layout = self.layout

        rd = context.scene.render
        image_settings = rd.image_settings
        file_format = image_settings.file_format

        layout.prop(rd, "filepath", text="")

        split = layout.split()

        layout.template_image_settings(image_settings, color_management=False)


class RENDER_PT_pr_pixel_sampler(RenderButtonsPanel, bpy.types.Panel):
    bl_label = "Pixel Sampler"
    COMPAT_ENGINES = {'PEARRAY_RENDER'}

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        
        layout.prop(scene.pearray, "pixel_sampler_mode")
        layout.prop(scene.pearray, "max_pixel_samples")

        col = layout.column()
        col.prop(scene.pearray, "adaptive_sampling", text="Adaptive Sampling")
        sub = col.column()
        sub.active = scene.pearray.adaptive_sampling
        sub.prop(scene.pearray, "min_pixel_samples")
        sub.prop(scene.pearray, "as_quality")


class RENDER_PT_pr_integrator(RenderButtonsPanel, bpy.types.Panel):
    bl_label = "Integrator"
    COMPAT_ENGINES = {'PEARRAY_RENDER'}

    def draw(self, context):
        layout = self.layout
        scene = context.scene

        layout.prop(scene.pearray, "max_diffuse_bounces")

        if scene.pearray.integrator == 'DI' or scene.pearray.integrator == 'BIDI':
            layout.prop(scene.pearray, "max_light_samples")

        if scene.pearray.integrator == 'PPM':
            layout.separator()
            layout.prop(scene.pearray, "photon_count")
            layout.prop(scene.pearray, "photon_passes")
            col = layout.column(align=True)
            col.label("Gathering:")
            col.prop(scene.pearray, "photon_gather_radius")
            col.prop(scene.pearray, "photon_max_gather_count")
            col.prop(scene.pearray, "photon_gathering_mode", text="")
            col.prop(scene.pearray, "photon_squeeze")


class RENDER_PT_pr_export_settings(RenderButtonsPanel, bpy.types.Panel):
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
        layout.prop(scene.pearray, "apply_transform")
    
