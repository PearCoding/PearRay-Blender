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


modules = (
    properties_camera,
    properties_light,
    properties_material,
    properties_mesh,
    properties_output,
    properties_render,
    properties_world,)


# Initialization
def register():
    for m in modules:
        m.register()


def unregister():
    for m in reversed(modules):
        m.unregister()
