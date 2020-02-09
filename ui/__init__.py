import bpy


from . import (
    properties_camera,
    properties_light,
    properties_material,
    properties_mesh,
    properties_output,
    properties_render,
    properties_world,
)

from ..core.render import PearRayRender

modules = (
    properties_camera,
    properties_light,
    properties_material,
    properties_mesh,
    properties_output,
    properties_render,
    properties_world,)


def get_panels():
    exclude_panels = {}

    for panel in bpy.types.Panel.__subclasses__():
        if 'BLENDER_RENDER' in getattr(panel, 'COMPAT_ENGINES', []):
            if panel.__name__ not in exclude_panels:
                yield panel


# Initialization
def register():
    for panel in get_panels():
        panel.COMPAT_ENGINES.add(PearRayRender.bl_idname)

    for m in modules:
        m.register()


def unregister():
    for m in reversed(modules):
        m.unregister()

    for panel in get_panels():
        if PearRayRender.bl_idname in panel.COMPAT_ENGINES:
            panel.COMPAT_ENGINES.remove(PearRayRender.bl_idname)
