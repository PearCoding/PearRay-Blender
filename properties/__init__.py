import bpy

from . import properties
from bpy.props import PointerProperty


def register():
    bpy.types.Scene.pearray = PointerProperty(type=properties.PearRaySceneProperties)
    bpy.types.Camera.pearray = PointerProperty(type=properties.PearRayCameraProperties)


def unregister():
    del bpy.types.Scene.pearray
    del bpy.types.Camera.pearray