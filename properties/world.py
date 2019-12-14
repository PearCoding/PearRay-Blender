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
    split_background = BoolProperty(
        name="Split Background",
        description="Split Environment map into camera visible background and radiance",
        default=False
    )
    background_type = EnumProperty(
        name="Background Color Type",
        description="Background Color Type",
        items=enums.enum_fake_color_type,
        default='COLOR'
    )
    background_tex_slot = IntProperty(
        name="Background Texture Slot",
        description="Used Background Texture Slot",
        min=0, soft_max=100000, default=0
    )
    radiance_type = EnumProperty(
        name="Radiance Color Type",
        description="Radiance Color Type",
        items=enums.enum_fake_color_type,
        default='COLOR'
    )
    radiance_color = FloatVectorProperty(
        name="Radiance Color",
        description="Radiance Color",
        default=(1,1,1),
        subtype="COLOR",
        soft_max=1
    )
    radiance_tex_slot = IntProperty(
        name="Radiance Texture Slot",
        description="Used Radiance Texture Slot",
        min=0, soft_max=100000, default=0
    )
    radiance_factor = FloatProperty(
        name="Radiance Factor",
        description="Multiply factor to the given radiance map",
        min=0.0, soft_max=1.0, default=1.0
    )
