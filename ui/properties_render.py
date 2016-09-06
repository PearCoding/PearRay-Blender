import bpy


from bl_ui import properties_render
properties_render.RENDER_PT_render.COMPAT_ENGINES.add('PEARRAY_RENDER')
properties_render.RENDER_PT_dimensions.COMPAT_ENGINES.add('PEARRAY_RENDER')
properties_render.RENDER_PT_performance.COMPAT_ENGINES.add('PEARRAY_RENDER')
properties_render.RENDER_PT_output.COMPAT_ENGINES.add('PEARRAY_RENDER')
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


class RENDER_PT_pixel_sampler(RenderButtonsPanel, bpy.types.Panel):
    bl_label = "Pixel Sampler"
    COMPAT_ENGINES = {'PEARRAY_RENDER'}

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        
        layout.prop(scene.pearray, "pixel_sampler_mode")
        layout.prop(scene.pearray, "max_pixel_samples")


class RENDER_PT_integrator(RenderButtonsPanel, bpy.types.Panel):
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


class RENDER_PT_export_settings(RenderButtonsPanel, bpy.types.Panel):
    bl_label = "Export Settings"
    COMPAT_ENGINES = {'PEARRAY_RENDER'}

    def draw_header(self, context):
        pass

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        
        layout.prop(scene.pearray, "keep_prc")
        layout.prop(scene.pearray, "beautiful_prc")
        layout.prop(scene.pearray, "apply_transform")
    

def draw_pearray_render(self, context):
    layout = self.layout
    scene = context.scene

    if scene.render.engine == 'PEARRAY_RENDER':
        layout.prop(scene.pearray, "integrator")
        layout.prop(scene.pearray, "debug_mode")
        layout.prop(scene.pearray, "incremental")
        layout.prop(scene.pearray, "max_ray_depth")