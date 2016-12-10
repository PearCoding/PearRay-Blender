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
    apply_transform = BoolProperty(
        name="Apply Transform",
        description="Apply transform prior export for meshes",
        default=False
    )
    linear_rgb = BoolProperty(
        name="Use linear sRGB",
        description="Return output in linear sRGB",
        default=False
    )
    debug_mode = EnumProperty(
        name="Debug Mode",
        description="Render in debug mode",
        items=enums.enum_debug_mode,
        default='NONE'
        )
    incremental = BoolProperty(
        name="Incremental",
        description="Render incremental and improve after each step",
        default=True
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
        default='BIDI'
        )
    distortion_quality = FloatProperty(
        name="Quality",
        description="Distortion Quality",
        min=0.0, max=100.0, default=10,
        subtype="PERCENTAGE"
        )
    pixel_sampler_mode = EnumProperty(
        name="Sampler Mode",
        description="Pixel sampling technique",
        items=enums.enum_pixel_sampler_mode,
        default='MJITT'
        )
    max_pixel_samples = IntProperty(
        name="Max Pixel Samples",
        description="Maximum pixel samples",
        min=1,
        soft_max=4096,
        subtype="UNSIGNED",
        default=4
        )
    min_pixel_samples = IntProperty(
        name="Min Pixel Samples",
        description="Minimum pixel samples",
        min=1,
        soft_max=4096,
        subtype="UNSIGNED",
        default=1
        )
    adaptive_sampling = BoolProperty(
        name="Adaptive Sampling",
        description="Use Adaptive Sampling",
        default=False
        )
    as_quality = FloatProperty(
        name="Quality",
        description="Adaptive Sampling Quality",
        min=0.0, max=100.0, default=80,
        subtype="PERCENTAGE"
        )
    max_diffuse_bounces = IntProperty(
        name="Max Diffuse Bounces",
        description="Maximum diffuse bounces",
        min=0,
        soft_max=4096,
        subtype="UNSIGNED",
        default=2
        )
    max_light_samples = IntProperty(
        name="Max Light Samples",
        description="Maximum light samples",
        min=1,
        soft_max=4096,
        subtype="UNSIGNED",
        default=2
        )
    photon_count = IntProperty(
        name="Photons",
        description="Amount of photons emitted per pass into scene",
        min=1,
        soft_max=1000000000,
        step=100,
        subtype="UNSIGNED",
        default=1000000
        )
    photon_passes = IntProperty(
        name="Max Passes",
        description="Maximum count of passes",
        min=1,
        soft_max=1000000000,
        subtype="UNSIGNED",
        default=50
        )
    photon_gather_radius = FloatProperty(
        name="Gather Radius",
        description="Maximum radius of gathering",
        min=0.0001, soft_max=1000.0, default=0.1
        )
    photon_max_gather_count = IntProperty(
        name="Max Gather Count",
        description="Maximum amount of photons used for estimating radiance",
        min=1,
        soft_max=1000000000,
        step=100,
        subtype="UNSIGNED",
        default=1000
        )
    photon_gathering_mode = EnumProperty(
        name="Gathering Mode",
        description="Gathering mode used for estimating radiance",
        items=enums.enum_photon_gathering_mode,
        default='SPHERE'
        )
    photon_squeeze = FloatProperty(
        name="Squeeze Factor",
        description="Squeeze factor to press sphere/dome into a disk",
        min=0.0, max=100, default=0.0,
        subtype="PERCENTAGE"
        )
    photon_ratio = FloatProperty(
        name="Contract Ratio",
        description="Ratio of radius contraction",
        min=1, max=100, default=20,
        subtype="PERCENTAGE"
        )
    photon_proj_weight = FloatProperty(
        name="Projection Map Weight",
        description="Projection Map Weight. 0 disables it",
        min=0.0, max=100, default=80,
        subtype="PERCENTAGE"
        )
    photon_proj_qual = FloatProperty(
        name="Projection Map Quality",
        description="Quality of projection map",
        min=1, max=100, default=80,
        subtype="PERCENTAGE"
        )
    photon_proj_caustic = FloatProperty(
        name="Projection Map Caustic Favor",
        description="Ratio of how much to prefer caustic paths. 0 disables it",
        min=0, soft_max=100, default=20,
        subtype="PERCENTAGE"
        )
