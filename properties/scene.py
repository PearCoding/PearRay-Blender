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
    beautiful_prc: BoolProperty(
        name="Beautiful PRC",
        description="Export the prc in a beautiful way. (Just using tabs :P)",
        default=False
    )
    keep_prc: BoolProperty(
        name="Keep PRC",
        description="Keep generated prc file after rendering",
        default=False
    )
    color_format: EnumProperty(
        name="Color output format",
        description="Output format of color channel in file",
        items=enums.enum_color_format,
        default='XYZ'
    )
    max_ray_depth: IntProperty(
        name="Max Ray Depth",
        description="Maximum ray depth",
        min=1,
        soft_max=4096,
        subtype="UNSIGNED",
        default=64
    )
    soft_max_ray_depth: IntProperty(
        name="Soft Max Ray Depth",
        description="Maximum ray depth after which russian roulette is used",
        min=1,
        soft_max=4096,
        subtype="UNSIGNED",
        default=4
    )
    max_light_ray_depth: IntProperty(
        name="Max Light Ray Depth",
        description="Maximum ray depth for rays starting from light sources",
        min=1,
        soft_max=4096,
        subtype="UNSIGNED",
        default=16
    )
    soft_max_light_ray_depth: IntProperty(
        name="Soft Max Light Ray Depth",
        description="Maximum light ray depth after which russian roulette is used",
        min=1,
        soft_max=4096,
        subtype="UNSIGNED",
        default=2
    )
    integrator: EnumProperty(
        name="Integrator",
        description="Integrator to be used",
        items=enums.enum_integrator_mode,
        default='DIRECT'
    )
    vf_mode: EnumProperty(
        name="Mode",
        description="Visual Feedback Mode",
        items=enums.enum_vf_mode,
        default='COLORED_ENTITY_ID'
    )
    vf_apply_weighting: BoolProperty(
        name="Apply Weighting",
        description="Apply view dependent weighting for better scene visibility",
        default=True
    )
    ppm_photons_per_pass: IntProperty(
        name="Max Photons per Pass",
        description="Maximum amount of photons to trace each pass",
        min=1000,
        soft_max=100000000,
        subtype="UNSIGNED",
        default=1000000
    )
    render_tile_mode: EnumProperty(
        name="Tile Mode",
        description="Tiling Mode to be used while rendering",
        items=enums.enum_tile_mode,
        default='LINEAR'
    )
    pixel_filter_mode: EnumProperty(
        name="Pixel Filter",
        description="Pixel filter to be used while rendering",
        items=enums.enum_pixel_filter_type,
        default='MITCHELL'
    )
    pixel_filter_radius: IntProperty(
        name="Pixel Filter Radius",
        description="Radius of the pixel filter",
        min=0,
        soft_max=4,
        subtype="UNSIGNED",
        default=1
    )
    sampler_max_samples: IntProperty(
        name="Max Samples",
        description="Maximum samples",
        min=1,
        soft_max=4096,
        subtype="UNSIGNED",
        default=512
    )
    sampler_aa_mode: EnumProperty(
        name="AA Sampler Mode",
        description="AA sampling technique",
        items=enums.enum_sampler_mode,
        default='MULTI_JITTER'
    )
    sampler_lens_mode: EnumProperty(
        name="Lens Sampler Mode",
        description="Lens sampling technique",
        items=enums.enum_sampler_mode,
        default='MULTI_JITTER'
    )
    sampler_time_mode: EnumProperty(
        name="Time Sampler Mode",
        description="Time sampling technique",
        items=enums.enum_sampler_mode,
        default='MULTI_JITTER'
    )
    sampler_spectral_mode: EnumProperty(
        name="Spectral Sampler Mode",
        description="Spectral sampling technique",
        items=enums.enum_sampler_mode,
        default='RANDOM'
    )
    sampler_time_mapping_mode: EnumProperty(
        name="Time Mapping Mode",
        description="Time Mapping Mode",
        items=enums.enum_time_mapping_mode,
        default='CENTER'
    )
    sampler_time_scale: FloatProperty(
        name="Time Scale",
        description="Time Scale",
        min=0,
        soft_min=0.001,
        soft_max=1000,
        default=1
    )
    max_light_samples: IntProperty(
        name="Max Light Samples",
        description="Maximum light samples",
        min=1,
        soft_max=4096,
        subtype="UNSIGNED",
        default=1
    )
    ao_sample_count: IntProperty(
        name="AO Sample Count",
        description="Occlusion test samples",
        min=1,
        soft_max=4096,
        subtype="UNSIGNED",
        default=42
    )


def register():
    bpy.utils.register_class(PearRaySceneProperties)
    bpy.types.Scene.pearray = PointerProperty(type=PearRaySceneProperties)


def unregister():
    del bpy.types.Scene.pearray
    bpy.utils.unregister_class(PearRaySceneProperties)
