import bpy

from .camera import PearRayCameraProperties
from .scene import PearRaySceneProperties

from bpy.types import AddonPreferences

from bpy.props import (
        StringProperty,
        BoolProperty,
        PointerProperty
        )


### Global Settings
pearray_package = __import__(__name__.split('.')[0])
class PearRayPreferences(AddonPreferences):
    bl_idname = pearray_package.__package__
    
    executable = StringProperty(
                name="Executable",
                description="Path to renderer executable",
                subtype='FILE_PATH',
                )
    show_progress = BoolProperty(
                name="Show Progress",
                description="Experimental feature to show current progress status while rendering",
                default=False
                )
    def draw(self, context):
        layout = self.layout
        layout.prop(self, "executable")
        layout.prop(self, "show_progress")


def register():
    bpy.types.Scene.pearray = PointerProperty(type=PearRaySceneProperties)
    bpy.types.Camera.pearray = PointerProperty(type=PearRayCameraProperties)


def unregister():
    del bpy.types.Scene.pearray
    del bpy.types.Camera.pearray