bl_info = {
    "name": "PearRay",
    "description": "Basic PearRay integration for blender.",
    "author": "Ömercan Yazici",
    "version": (0, 2),
    "blender": (2, 70, 0),
    "location": "Render > Engine > PearRay",
    "warning": "experimental", # used for warning icon and text in addons panel
    "tracker_url": "https://github.com/PearCoding/PearRay/issues/new",
    "category": "Render"
    }


if "bpy" in locals():
    import importlib
    importlib.reload(ui)
    importlib.reload(render)
    importlib.reload(properties)
else:
    import bpy
    from . import (
            ui,
            render,
            properties
            )


## Initialization
def register():
    bpy.utils.register_module(__name__)
    properties.register()
    ui.register()


def unregister():
    ui.unregister()
    properties.unregister()
    bpy.utils.unregister_module(__name__)


if __name__ == "__main__":
    register()
