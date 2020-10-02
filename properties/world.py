import bpy

from bpy.types import (
    PropertyGroup,
)

from bpy.props import (
    StringProperty,
    BoolProperty,
    IntProperty,
    IntVectorProperty,
    FloatProperty,
    FloatVectorProperty,
    EnumProperty,
    PointerProperty,
    CollectionProperty,
)


from . import enums


class PearRayWorldProperties(PropertyGroup):
    # Background (Environment)
    split_background: BoolProperty(
        name="Split Background",
        description="Split Environment map into camera visible background and radiance",
        default=False
    )
    radiance_color: FloatVectorProperty(
        name="Radiance Color",
        description="Radiance Color",
        default=(1, 1, 1),
        subtype="COLOR",
        soft_max=1
    )
    radiance_factor: FloatProperty(
        name="Radiance Factor",
        description="Multiply factor to the given radiance map",
        min=0.0, soft_max=1.0, default=1.0
    )


def register():
    bpy.utils.register_class(PearRayWorldProperties)
    bpy.types.World.pearray = PointerProperty(type=PearRayWorldProperties)


def unregister():
    del bpy.types.World.pearray
    bpy.utils.unregister_class(PearRayWorldProperties)
