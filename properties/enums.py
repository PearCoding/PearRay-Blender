enum_color_format = (
    ("XYZ", "CIE XYZ", "CIE XYZ format"),
    ("RGB", "Linear sRGB", "Linear sRGB"),
    ("SRGB", "sRGB", "sRGB with 2.2 gamma"),
)

enum_sampler_mode = (
    ("RANDOM", "Random", "Random sampling technique"),
    ("UNIFORM", "Uniform", "Uniform sampling technique"),
    ("JITTER", "Jitter", "Jitter sampling technique"),
    ("MULTI_JITTER", "Multi-Jitter", "Multi-Jitter sampling technique"),
    ("HALTON", "Halton",
     "Quasi-Monte Carlo sampling method based on the Halton sequence"),
    ("SOBOL", "Sobol",
     "Quasi-Monte Carlo sampling method based on the Sobol sequence"),
)

enum_time_mapping_mode = (
    ("CENTER", "Center", "Center Mapping [-1/2,1/2]"),
    ("LEFT", "Left", "Left Mapping [-1,0]"),
    ("RIGHT", "Right", "Right Mapping [0,1]"),
)

enum_integrator_mode = (
    ('DIRECT', "Direct", "Direct Rendering"),
    ('AO', "Ambient Occulusion", "Ambient Occulusion"),
)

enum_tile_mode = (
    ("LINEAR", "Linear", "From top-left to bottom-right"),
    ("TILE", "Tile", "From top-left to bottom-right in intervals"),
    ("SPIRAL", "Spiral", "From the mid to border"),
)

enum_photon_gathering_mode = (
    ("DOME", "Dome", "Gather only front side of surface"),
    ("SPHERE", "Sphere", "Gather around a point"),
)

enum_color_type = (
    ("COLOR", "Color", "Standard RGB value"),
    ("TEMP", "Temperature", "Blackbody Temperature in Kelvin"),
    ("TEX", "Texture", "Texture"),
    #("NODE", "Node", "Node"),
)

enum_fake_color_type = (
    ("COLOR", "Color", "Standard RGB value"),
    ("TEX", "Texture", "Texture"),
    #("NODE", "Node", "Node"),
)

enum_flat_color_type = (
    ("COLOR", "Color", "Standard RGB value"),
    ("TEMP", "Temperature", "Blackbody Temperature in Kelvin"),
)

enum_ior_type = (
    ("VALUE", "Value", "Floating point value"),
    ("COLOR", "Color", "Standard RGB value"),
)

enum_temp_type = (
    ("LUM", "Luminance", "Blackbody curve output in luminance"),
    ("RAD", "Radiance", "Blackbody curve output in radiance"),
    ("LUM_NORM", "Luminance Normalized",
     "Normalized luminance blackbody output"),
    ("RAD_NORM", "Radiance Normalized",
     "Normalized radiance blackbody output"),
)

enum_material_bsdf = (
    ("DIFFUSE", "Diffuse", "Simple lambertian material"),
    ("ORENNAYAR", "Oren-Nayar", "Oren-Nayar BRDF"),
    ("MICROFACET", "Microfacet", "Generic microfacet BRDF"),
    ("PRINCIPLED", "Principled", "Generic principled BRDF"),
    ("WARD", "Ward", "Ward BRDF"),
    ("GRID", "Grid", "Special material grid"),
    ("GLASS", "Glass", "Specialized glass material"),
    ("MIRROR", "Mirror", "Specialized mirror material"),
)

enum_material_ct_fresnel_mode = (
    ("DIELECTRIC", "Dielectric", "Dielectric fresnel"),
    ("CONDUCTOR", "Conductor",
     "Conductor fresnel (for metal). Absorption based on diffuse term"),
)

enum_material_ct_distribution_mode = (
    ("BLINN", "Blinn", "Blinn based distribution term"),
    ("BECKMANN", "Beckmann", "Beckmann based distribution term"),
    ("GGX", "GGX", "GGX based distribution term"),
)

enum_material_ct_geometry_mode = (
    ("IMPLICIT", "Implicit", "Implicit based geometry term"),
    ("NEUMANN", "Neumann", "Neumann based geometry term"),
    ("COOK_TORRANCE", "Cook-Torrance", "Cook-Torrance based geometry term"),
    ("KELEMEN", "Kelemen", "Kelemen based geometry term"),
    ("SCHLICK", "Schlick", "Schlick based geometry term"),
    ("WALTER", "Walter", "Walter based geometry term"),
)

enum_aov_type = (
    ("SPECTRAL", "Spectral", "Spectral output"),
    ("POSITION", "Position", "Position output"),
    ("NORMAL", "Normal", "Normal output"),
    ("NORMALG", "Geometric Normal", "Geometric Normal output"),
    ("TANGENT", "Tangent", "Tangent output"),
    ("BITANGENT", "Bitangent", "Bitangent output"),
    ("VIEW", "View", "View output"),
    ("UVW", "Texture", "Texture (UV) output"),
    ("DPDT", "Velocity", "Velocity dp/dt output"),
    ("ENTITY_ID", "Entity ID", "Entity ID output"),
    ("MATERIAL_ID", "Material ID", "Material ID output"),
    ("EMISSION_ID", "Emission ID", "Emission ID output"),
    ("DISPLACE_ID", "Displace ID", "Displace ID output"),
    ("DEPTH", "Depth", "(Ray) Depth output"),
    ("TIME", "Time", "Time output"),
)
