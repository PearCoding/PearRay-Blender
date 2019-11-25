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


class PearRayMeshProperties(PropertyGroup):
    subdivision_scheme = EnumProperty(
        name="Scheme",
        description="Subdivision Scheme",
        items=enums.enum_subdivision_scheme,
        default='CATMARK'
    )
    
    subdivision_max_level = IntProperty(
        name="Max Level",
        description="Max subdivision level",
        min=1, soft_max=10, default=4
    )

    subdivision_adaptive = BoolProperty(
        name="Adaptive",
        description="Use adaptive subdivision",
        default=False
    )
    
    subdivision_boundary_interp = EnumProperty(
        name="Boundary Interpolation",
        description="Subdivision boundary interpolation type",
        items=enums.enum_subdivision_boundary_interp,
        default='EDGE_ONLY'
    )
    
    subdivision_fvar_interp = EnumProperty(
        name="Face Varying Interpolation",
        description="Subdivision face varying interpolation type",
        items=enums.enum_subdivision_fvar_interp,
        default='ALL'
    )
    
    subdivision_uv_interp = EnumProperty(
        name="UV Interpolation",
        description="Subdivision uv interpolation type",
        items=enums.enum_subdivision_uv_interp,
        default='VERTEX'
    )

    subdivision = BoolProperty(
        name="Subdivision",
        description="Use OpenSubdiv",
        default=False
    )