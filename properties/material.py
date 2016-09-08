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


class PearRayMaterialProperties(PropertyGroup):
    brdf = EnumProperty(
        name="BRDF",
        description="BRDF type",
        items=enums.enum_material_brdf,
        default='DIFFUSE'
    )

    cast_shadows = BoolProperty(
        name="Cast Shadows",
        description="Cast Shadows",
        default=True
    )

    cast_self_shadows = BoolProperty(
        name="Cast Self Shadows",
        description="Cast shadows on himself",
        default=True
    )

    is_camera_visible = BoolProperty(
        name="Camera Visible",
        description="Is visible through the camera",
        default=True
    )

    is_shadeable = BoolProperty(
        name="Shadeable",
        description="Will be shaded",
        default=True
    )

    # Emission
    emission_color_type = EnumProperty(
        name="Emission Color Type",
        description="Emission Color Type",
        items=enums.enum_color_type,
        default='COLOR'
    )

    emission_color = FloatVectorProperty(
        name="Emission Color",
        description="Emission Color",
        default=(0,0,0),
        subtype="COLOR",
    )

    emission_color_temp = FloatProperty(
        name="Emission Color Temperature",
        description="Emission Blackbody Color Temperature",
        min=0, soft_max=100000.00, default=0, step=100
    )

    # Diffuse
    diffuse_color_type = EnumProperty(
        name="Diffuse Color Type",
        description="Diffuse Color Type",
        items=enums.enum_color_type,
        default='COLOR'
    )

    diffuse_color_temp = FloatProperty(
        name="Diffuse Color Temperature",
        description="Diffuse Blackbody Color Temperature",
        min=0, soft_max=100000.00, default=1000, step=100
    )

    # Specular
    specular_color_type = EnumProperty(
        name="Specular Color Type",
        description="Specular Color Type",
        items=enums.enum_color_type,
        default='COLOR'
    )

    specular_color_temp = FloatProperty(
        name="Specular Color Temperature",
        description="Specular Blackbody Color Temperature",
        min=0, soft_max=100000.00, default=1000, step=100
    )

    # Ward
    roughnessX = FloatProperty(
        name="Roughness X",
        description="Roughness to tangent direction",
        min=0, soft_max=1.00, default=0.50
    )
    roughnessY = FloatProperty(
        name="Roughness Y",
        description="Roughness to binormal direction",
        min=0, soft_max=1.00, default=0.50
    )

    # Grid
    grid_first_material = None
    grid_second_material = None
    grid_count = IntProperty(
        name="Grid Count",
        description="Grid Count",
        min=1, soft_max=100000, default=10
    )
    grid_tile_uv = BoolProperty(
        name="Tile UV",
        description="Tile the UV coordinates",
        default=True
    )