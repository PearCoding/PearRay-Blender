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


# Initialization
def register():
    for m in modules:
        m.register()


def unregister():
    for m in reversed(modules):
        m.unregister()


if __name__ == "__main__":
    register()
