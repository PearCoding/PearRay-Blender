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


class PearRaySceneProperties(PropertyGroup):
    beautiful_prc = BoolProperty(
        name="Beautiful PRC",
        description="Export the prc in a beautiful way. (Just using tabs :P)",
        default=False
    )
    keep_prc = BoolProperty(
        name="Keep PRC",
        description="Keep generated prc file after rendering",
        default=False
    )
    color_format = EnumProperty(
        name="Color output format",
        description="Output format of color channel in file",
        items=enums.enum_color_format,
        default='XYZ'
    )
    max_ray_depth = IntProperty(
        name="Max Ray Depth",
        description="Maximum ray depth",
        min=1,
        soft_max=4096,
        subtype="UNSIGNED",
        default=8
        )
    integrator = EnumProperty(
        name="Integrator",
        description="Integrator to be used",
        items=enums.enum_integrator_mode,
        default='DIRECT'
        )
    msi = BoolProperty(
        name="Use MSI",
        description="Use Multiple Importance Sampling",
        default=True
    )
    render_tile_mode = EnumProperty(
        name="Tile Mode",
        description="Tiling Mode to be used while rendering",
        items=enums.enum_tile_mode,
        default='LINEAR'
        )
    pixel_filter_mode = EnumProperty(
        name="Pixel Filter",
        description="Pixel filter to be used while rendering",
        items=enums.enum_pixel_filter_type,
        default='MITCHELL'
        )
    pixel_filter_radius = IntProperty(
        name="Pixel Filter Radius",
        description="Radius of the pixel filter",
        min=0,
        soft_max=4,
        subtype="UNSIGNED",
        default=1
        )
    sampler_aa_mode = EnumProperty(
        name="AA Sampler Mode",
        description="AA sampling technique",
        items=enums.enum_sampler_mode,
        default='MULTI_JITTER'
        )
    sampler_max_aa_samples = IntProperty(
        name="Max AA Samples",
        description="Maximum AA samples",
        min=1,
        soft_max=4096,
        subtype="UNSIGNED",
        default=4
        )
    sampler_lens_mode = EnumProperty(
        name="Lens Sampler Mode",
        description="Lens sampling technique",
        items=enums.enum_sampler_mode,
        default='MULTI_JITTER'
        )
    sampler_max_lens_samples = IntProperty(
        name="Max Lens Samples",
        description="Maximum Lens samples",
        min=1,
        soft_max=4096,
        subtype="UNSIGNED",
        default=1
        )
    sampler_time_mode = EnumProperty(
        name="Time Sampler Mode",
        description="Time sampling technique",
        items=enums.enum_sampler_mode,
        default='MULTI_JITTER'
        )
    sampler_max_time_samples = IntProperty(
        name="Max Time Samples",
        description="Maximum Time samples",
        min=1,
        soft_max=4096,
        subtype="UNSIGNED",
        default=1
        )
    sampler_time_mapping_mode = EnumProperty(
        name="Time Mapping Mode",
        description="Time Mapping Mode",
        items=enums.enum_time_mapping_mode,
        default='CENTER'
        )
    sampler_time_scale = FloatProperty(
        name="Time Scale",
        description="Time Scale",
        min=0,
        soft_min=0.001,
        soft_max=1000,
        default=1
        )
    max_light_samples = IntProperty(
        name="Max Light Samples",
        description="Maximum light samples",
        min=1,
        soft_max=4096,
        subtype="UNSIGNED",
        default=1
        )
