import bpy

from .camera import PearRayCameraProperties
from .scene import PearRaySceneProperties
from .material import PearRayMaterialProperties
from .light import PearRayLightProperties

from bpy.types import AddonPreferences

from bpy.props import (
        StringProperty,
        BoolProperty,
        IntProperty,
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
    show_progress_interval = IntProperty(
                name="Show Progress",
                description="Update interval for progress status. Zero disables it",
                default=2,
                min=0,
                soft_max=10
                )
    show_image_interval = IntProperty(
                name="Show Image",
                description="(Experimental) Update interval for image updates. Zero disables it",
                default=5,
                min=0,
                soft_max=10
                )
    def draw(self, context):
        layout = self.layout
        layout.prop(self, "executable")
        col = layout.column(align=True)
        col.prop(self, "show_progress_interval")
        col.prop(self, "show_image_interval")


def register():
    bpy.types.Scene.pearray = PointerProperty(type=PearRaySceneProperties)
    bpy.types.Camera.pearray = PointerProperty(type=PearRayCameraProperties)
    bpy.types.Material.pearray = PointerProperty(type=PearRayMaterialProperties)
    bpy.types.Lamp.pearray = PointerProperty(type=PearRayLightProperties)


def unregister():
    del bpy.types.Scene.pearray
    del bpy.types.Camera.pearray
    del bpy.types.Material.pearray
    del bpy.types.Lamp.pearray