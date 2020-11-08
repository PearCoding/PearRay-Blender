import bpy

from . import primitives, export


def register():
    primitives.register()
    export.register()


def unregister():
    export.unregister()
    primitives.unregister()
