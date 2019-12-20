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


class PearRayLPEProperty(PropertyGroup):
    channel = EnumProperty(
        name="Channel",
        description="Channel Type",
        items=enums.enum_aov_type,
        default='SPECTRAL'
    )
    expression = StringProperty(
        name="Expression",
        description="Light Path Expression. See documentation for syntax",
        default="C.*"
    )


class PearRaySceneRenderLayerProperties(PropertyGroup):
    aov_t = BoolProperty(
        name="Time",
        description="Deliver T (time) values as an extra file",
        default=False
    )
    aov_samples = BoolProperty(
        name="Samples",
        description="Deliver samples values as an extra file",
        default=False
    )

    aov_p = BoolProperty(
        name="Position",
        description="Deliver P (position) values as an extra file",
        default=False
    )
    aov_ng = BoolProperty(
        name="Ng",
        description="Deliver Ng (geometric normal) values as an extra file",
        default=False
    )
    aov_nx = BoolProperty(
        name="Nx",
        description="Deliver Nx (tangent) values as an extra file",
        default=False
    )
    aov_ny = BoolProperty(
        name="Ny",
        description="Deliver Ny (bitangent/binormal) values as an extra file",
        default=False
    )
    aov_feedback = BoolProperty(
        name="Feedback",
        description="Output feedback and error bit mask image",
        default=True
    )
    aov_emission_index = BoolProperty(
        name="Emission Index",
        description="Index of the internal emission descriptor",
        default=False
    )
    aov_displace_index = BoolProperty(
        name="Displace Index",
        description="Index of the internal displace descriptor",
        default=False
    )

    raw_spectral = BoolProperty(
        name="Raw Spectral",
        description="Deliver raw spectral values",
        default=False
    )

    separate_files = BoolProperty(
        name="Separate Files",
        description="Output each AOV into his each own file",
        default=False
    )

    lpes = CollectionProperty(
        type=PearRayLPEProperty,
        name="Light Path Expressions"
    )
    active_lpe_index = IntProperty(
        # This property is redundant, but needed by blender
        # We do not use it for rendering!
        name="Active LPE",
        description="Currently active LPE",
        default=0
    )
