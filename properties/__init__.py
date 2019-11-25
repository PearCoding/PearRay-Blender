import bpy

from .camera import PearRayCameraProperties
from .scene import PearRaySceneProperties
from .layer import PearRaySceneRenderLayerProperties
from .material import PearRayMaterialProperties
from .mesh import PearRayMeshProperties
from .light import PearRayLightProperties
from .world import PearRayWorldProperties

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

    package_dir = StringProperty(
                name="Custom Package Directory",
                description="Path to pypearray package library. Can be empty to search in system paths",
                subtype='DIR_PATH',
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
                description="Update interval for image updates. Zero disables it",
                default=5,
                min=0,
                soft_max=10
                )
    verbose = BoolProperty(
                name="Verbose",
                description="Display verbose information in the produced log files",
                default=True
                )
    profile = BoolProperty(
                name="Profile",
                description="Profile execution if available and dump results to pr_profile.prof at the end",
                default=False
                )
    def draw(self, context):
        layout = self.layout
        layout.prop(self, "package_dir")
        row = layout.row(align=True)
        row.prop(self, "verbose")
        row.prop(self, "profile")
        col = layout.column(align=True)
        col.prop(self, "show_progress_interval")
        col.prop(self, "show_image_interval")


def register():
    bpy.types.Scene.pearray = PointerProperty(type=PearRaySceneProperties)
    bpy.types.Scene.pearray_layer = PointerProperty(type=PearRaySceneRenderLayerProperties)
    bpy.types.Camera.pearray = PointerProperty(type=PearRayCameraProperties)
    bpy.types.Material.pearray = PointerProperty(type=PearRayMaterialProperties)
    bpy.types.Mesh.pearray = PointerProperty(type=PearRayMeshProperties)
    bpy.types.Lamp.pearray = PointerProperty(type=PearRayLightProperties)
    bpy.types.World.pearray = PointerProperty(type=PearRayWorldProperties)


def unregister():
    del bpy.types.Scene.pearray
    del bpy.types.Scene.pearray_layer
    del bpy.types.Camera.pearray
    del bpy.types.Material.pearray
    del bpy.types.Mesh.pearray
    del bpy.types.Lamp.pearray
    del bpy.types.World.pearray