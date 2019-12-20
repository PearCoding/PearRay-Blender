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


class PearRayPrimitiveProperties(PropertyGroup):
    primitive_type = EnumProperty(
        name="Type",
        description="Primitive Type",
        items=enums.enum_primitive_type,
        default='SPHERE'
    )

    radius = FloatProperty(
        name="Radius",
        description="Sphere Radius",
        min=0, soft_max=10, default=1
    )

    top_radius = FloatProperty(
        name="Top Radius",
        description="Top Radius",
        min=0, soft_max=10, default=1
    )

    width = FloatProperty(
        name="Width",
        description="Width",
        min=0, soft_max=10, default=1
    )

    height = FloatProperty(
        name="Height",
        description="Height",
        min=0, soft_max=10, default=1
    )

    depth = FloatProperty(
        name="Depth",
        description="Depth",
        min=0, soft_max=10, default=1
    )

    normal = FloatVectorProperty(
        name="Normal",
        description="Local Normal",
        default=(0, 0, 1),
        subtype='DIRECTION',
        min=0, soft_max=10
    )

    parameters = FloatVectorProperty(
        name="Parameters",
        description="Quadric Parameter",
        default=(1, 1, 1, 0, 0, 0, 0, 0, 0, -1),
        size=10,
        min=0, soft_max=10
    )
