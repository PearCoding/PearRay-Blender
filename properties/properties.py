import bpy

from bpy.types import (
        AddonPreferences,
        PropertyGroup,
        Operator,
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

enum_debug_mode= (
    ('NONE', "None", "No debug mode"),
    ('DEPTH', "Depth", "Show depth information"),
    ('NORM_B', "Normal", "Show normals"),
    ('NORM_P', "Normal Positive", "Show positive normals"),
    ('NORM_N', "Normal Negative", "Show negative normals"),
    ('NORM_S', "Normal Spherical", "Show normals in spherical coordinates"),
    ('TANG_B', "Tangent", "Show tangents"),
    ('TANG_P', "Tangent Positive", "Show positive tangents"),
    ('TANG_N', "Tangent Negative", "Show negative tangents"),
    ('TANG_S', "Tangent Spherical", "Show tangents in spherical coordinates"),
    ('BINO_B', "Binormal", "Show binormals"),
    ('BINO_P', "Binormal Positive", "Show positive binormals"),
    ('BINO_N', "Binormal Negative", "Show negative binormals"),
    ('BINO_S', "Binormal Spherical", "Show binormals in spherical coordinates"),
    ('UV', "UV", "Show UV/texture coordinates"),
    ('PDF', "PDF", "Show probability distribution function values"),
    ('APPLIED', "Applied", "Show applied BRDF values"),
    ('VALIDITY', "Validity", "Show if material is valid"),
    )

enum_pixel_sampler_mode= (
	("RAND", "Random", "Random sampling technique"),
	("UNIF", "Uniform", "Uniform sampling technique"),
	("JITT", "Jitter", "Jitter sampling technique"),
	("MJITT", "Multi-Jitter", "Multi-Jitter sampling technique"),
    )

enum_photon_gathering_mode= (
	("DOME", "Dome", "Gather only front side of surface"),
	("SPHERE", "Sphere", "Gather around a point"),
    )

### Scene
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
    debug_mode = EnumProperty(
        name="Debug Mode",
        description="Render in debug mode",
        items=enum_debug_mode,
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
    pixel_sampler_mode = EnumProperty(
        name="Sampler Mode",
        description="Pixel sampling technique",
        items=enum_pixel_sampler_mode,
        default='MJITT'
        )
    max_pixel_samples = IntProperty(
        name="Max Pixel Samples",
        description="Maximum pixel samples",
        min=1,
        soft_max=4096,
        subtype="UNSIGNED",
        default=64
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
        default=1
        )
    use_bidirect = BoolProperty(
        name="Use Bidirect",
        description="Use bidirect renderer",
        default=True
        )   
    photon_count = IntProperty(
        name="Photons",
        description="Amount of photons emitted into scene",
        min=0,
        soft_max=1000000000,
        step=100,
        subtype="UNSIGNED",
        default=100000
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
        default=500
        )
    photon_max_diffuse_bounces = IntProperty(
        name="Max Diffuse Bounces",
        description="Maximum diffuse bounces in photon mapping",
        min=1,
        soft_max=4096,
        subtype="UNSIGNED",
        default=4
        )
    photon_min_specular_bounces = IntProperty(
        name="Min Specular Bounces",
        description="Minimum specular bounces in photon mapping",
        min=1,
        soft_max=4096,
        subtype="UNSIGNED",
        default=1
        )
    photon_gathering_mode = EnumProperty(
        name="Gathering Mode",
        description="Gathering mode used for estimating radiance",
        items=enum_photon_gathering_mode,
        default='SPHERE'
        )
    photon_squeeze = FloatProperty(
        name="Squeeze Factor",
        description="Squeeze factor to press sphere/dome into a disk",
        min=0.0, max=1, default=0.0
        )


### Camera
class PearRayCameraProperties(PropertyGroup):
    zoom = FloatProperty(
        name="Zoom",
        description="Zoom factor",
        min=0.0001, max=1000.00, default=1.0
    )
    fstop = FloatProperty(
        name="FStop",
        description="Focus point for Depth of Field."
                    "0 disables DOF rendering",
        min=0.0, max=1000.0, default=0.0
    )
    apertureRadius = FloatProperty(
        name="Aperture Radius",
        description="Similar to a real camera's aperture effect over focal blur (though not "
                    "in physical units and independant of focal length). "
                    "Increase to get more blur",
        min=0.01, max=1.00, default=0.50
    )


### Global Settings
pearray_package = __import__(__name__.split('.')[0])
class PearRayPreferences(AddonPreferences):
    bl_idname = pearray_package.__package__
    
    executable = StringProperty(
                name="Executable",
                description="Path to renderer executable",
                subtype='FILE_PATH',
                )
    show_progress = BoolProperty(
                name="Show Progress",
                description="Experimental feature to show current progress status while rendering",
                default=False
                )
    def draw(self, context):
        layout = self.layout
        layout.prop(self, "executable")
        layout.prop(self, "show_progress")

    