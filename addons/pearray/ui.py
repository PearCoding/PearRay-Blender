import bpy


from bl_ui import properties_render
properties_render.RENDER_PT_render.COMPAT_ENGINES.add('PEARRAY_RENDER')
properties_render.RENDER_PT_dimensions.COMPAT_ENGINES.add('PEARRAY_RENDER')
properties_render.RENDER_PT_output.COMPAT_ENGINES.add('PEARRAY_RENDER')
del properties_render


from bl_ui import properties_world
properties_world.WORLD_PT_preview.COMPAT_ENGINES.add('PEARRAY_RENDER')
properties_world.WORLD_PT_context_world.COMPAT_ENGINES.add('PEARRAY_RENDER')
properties_world.WORLD_PT_world.COMPAT_ENGINES.add('PEARRAY_RENDER')
del properties_world


from bl_ui import properties_texture
from bl_ui.properties_texture import context_tex_datablock
for member in dir(properties_texture):
    subclass = getattr(properties_texture, member)
    try:
        subclass.COMPAT_ENGINES.add('PEARRAY_RENDER')
    except:
        pass
del properties_texture


from bl_ui import properties_material
for member in dir(properties_material):
    subclass = getattr(properties_material, member)
    if subclass not in (properties_material.MATERIAL_PT_transp_game,
                        properties_material.MATERIAL_PT_game_settings,
                        properties_material.MATERIAL_PT_physics):
        try:
            subclass.COMPAT_ENGINES.add('PEARRAY_RENDER')
        except:
            pass
del properties_material


from bl_ui import properties_data_camera
for member in dir(properties_data_camera):
    subclass = getattr(properties_data_camera, member)
    try:
        subclass.COMPAT_ENGINES.add('PEARRAY_RENDER')
    except:
        pass
del properties_data_camera


from bl_ui import properties_particle as properties_particle
for member in dir(properties_particle):
    subclass = getattr(properties_particle, member)
    try:
        subclass.COMPAT_ENGINES.add('PEARRAY_RENDER')
    except:
        pass
del properties_particle

## Setup panels
class RenderButtonsPanel():
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "render"
    # COMPAT_ENGINES must be defined in each subclass, external engines can add themselves here

    @classmethod
    def poll(cls, context):
        rd = context.scene.render
        return (rd.use_game_engine is False) and (rd.engine in cls.COMPAT_ENGINES)


class MaterialButtonsPanel():
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "material"
    # COMPAT_ENGINES must be defined in each subclass, external engines can add themselves here

    @classmethod
    def poll(cls, context):
        mat = context.material
        rd = context.scene.render
        return mat and (rd.use_game_engine is False) and (rd.engine in cls.COMPAT_ENGINES)


class TextureButtonsPanel():
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "texture"
    # COMPAT_ENGINES must be defined in each subclass, external engines can add themselves here

    @classmethod
    def poll(cls, context):
        tex = context.texture
        rd = context.scene.render
        return tex and (rd.use_game_engine is False) and (rd.engine in cls.COMPAT_ENGINES)


class ObjectButtonsPanel():
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "object"
    # COMPAT_ENGINES must be defined in each subclass, external engines can add themselves here

    @classmethod
    def poll(cls, context):
        obj = context.object
        rd = context.scene.render
        return obj and (rd.use_game_engine is False) and (rd.engine in cls.COMPAT_ENGINES)


class CameraDataButtonsPanel():
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "data"
    # COMPAT_ENGINES must be defined in each subclass, external engines can add themselves here

    @classmethod
    def poll(cls, context):
        cam = context.camera
        rd = context.scene.render
        return cam and (rd.use_game_engine is False) and (rd.engine in cls.COMPAT_ENGINES)


class WorldButtonsPanel():
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "world"
    # COMPAT_ENGINES must be defined in each subclass, external engines can add themselves here

    @classmethod
    def poll(cls, context):
        wld = context.world
        rd = context.scene.render
        return wld and (rd.use_game_engine is False) and (rd.engine in cls.COMPAT_ENGINES)

## Native panels

### Camera
class CAMERA_PT_pearray_cam_settings(CameraDataButtonsPanel, bpy.types.Panel):
    bl_label = "PearRay Settings"
    COMPAT_ENGINES = {'PEARRAY_RENDER'}

    def draw_header(self, context):
        cam = context.camera

    def draw(self, context):
        layout = self.layout

        cam = context.camera

        layout.prop(cam.pearray, "zoom", text="Zoom")

        split = layout.split()

        split.prop(cam.pearray, "fstop", text="DOF FStop")
        split.prop(cam.pearray, "apertureRadius", text="DOF Aperture Radius")

### PearRay
class RENDER_PT_export_settings(RenderButtonsPanel, bpy.types.Panel):
    bl_label = "Export Settings"
    COMPAT_ENGINES = {'PEARRAY_RENDER'}

    def draw_header(self, context):
        pass

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        
        layout.prop(scene.pearray, "scene_name", text="Scene Name")
        layout.prop(scene.pearray, "keep_prc", text="Keep PRC")


def draw_pearray_render(self, context):
    layout = self.layout
    scene = context.scene

    if scene.render.engine == 'PEARRAY_RENDER':
        layout.prop(scene.pearray, "debug_mode")


def register():
    bpy.types.RENDER_PT_render.append(draw_pearray_render)
    pass


def unregister():
    bpy.types.RENDER_PT_render.remove(draw_pearray_render)
    pass