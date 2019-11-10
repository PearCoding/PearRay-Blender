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
    # Background
    background_type = EnumProperty(
        name="Background Color Type",
        description="Background Color Type",
        items=enums.enum_fake_color_type,
        default='COLOR'
    )
    background_tex_slot = IntProperty(
        name="Texture Slot",
        description="Used Texture Slot",
        min=0, soft_max=100000, default=0
    )
