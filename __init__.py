import bpy
from . import (core,
               export,
               operators,
               properties,
               ui)

bl_info = {
    "name": "PearRay",
    "description": "Basic PearRay integration for blender.",
    "author": "Ömercan Yazici",
    "version": (0, 6),
    "blender": (2, 80, 0),
    "location": "Render > Engine > PearRay",
    "warning": "experimental",
    "tracker_url": "https://github.com/PearCoding/PearRay/issues/new",
    "category": "Render"
}


modules = (
    core,
    operators,
    properties,
    ui)


def get_panels():
    exclude_panels = {}

    panels = []
    for panel in bpy.types.Panel.__subclasses__():
        if hasattr(panel, 'COMPAT_ENGINES') and 'BLENDER_RENDER' in panel.COMPAT_ENGINES:
            if panel.__name__ not in exclude_panels:
                panels.append(panel)

    return panels


# Initialization
def register():
    for m in modules:
        m.register()

    for panel in get_panels():
        panel.COMPAT_ENGINES.add('PEARRAY')


def unregister():
    for m in reversed(modules):
        m.unregister()

    for panel in get_panels():
        if 'PEARRAY' in panel.COMPAT_ENGINES:
            panel.COMPAT_ENGINES.remove('PEARRAY')


if __name__ == "__main__":
    register()
