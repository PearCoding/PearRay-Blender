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
    ('VF', "Visual Feedback", "Visual and Debug Feedback"),
)

enum_vf_mode = (
    ("COLORED_ENTITY_ID", "Colored Entity ID", "Entity colored based on id"),
    ("COLORED_MATERIAL_ID", "Colored Material ID", "Material colored based on id"),
    ("COLORED_EMISSION_ID", "Colored Emission ID", "Emission colored based on id"),
    ("COLORED_DISPLACE_ID", "Colored Displace ID", "Displace colored based on id"),
    ("COLORED_PRIMITIVE_ID", "Colored Primitive ID", "Primitive/Face colored based on id"),
    ("COLORED_RAY_ID", "Colored Ray ID", "Ray colored based on id"),
    ("COLORED_CONTAINER_ID", "Colored Container ID", "Colored based on container id the entity is in"),
    ('RAY_DIRECTION', "Ray Direction", "Rescaled ray direction"),
    ('PARAMETER', "Parameter", "Internal parameterization of surfaces/volumes"),
    ('INSIDE', "Inside", "Green if determined as inside"),
    ('NDOTV', "NdotV", "Positive NdotV in red, negative NdotV in green"),
    ('VALIDATE_MATERIAL', "Validate Material", "Validation of underlying material. White is good"),
)

enum_tile_mode = (
    ("LINEAR", "Linear", "From top-left to bottom-right"),
    ("TILE", "Tile", "From top-left to bottom-right in intervals"),
    ("SPIRAL", "Spiral", "From the mid to border"),
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

enum_pixel_filter_type = (
    ("BLOCK", "Block", "Block"),
    ("TRIANGLE", "Triangle", "Triangle filter"),
    ("GAUSSIAN", "Gaussian", "Gaussian filter"),
    ("LANCZOS", "Lanczos", "Lanczos (sinc-sinc) filter"),
    ("MITCHELL", "Mitchell-Netravali", "Mitchell-Netravali filter"),
)

enum_subdivision_scheme = (
    ("BILINEAR", "Bilinear", "Bilinear scheme"),
    ("CATMARK", "Catmark", "Catmark scheme"),
    ("LOOP", "Loop", "Loop scheme"),
)

enum_subdivision_boundary_interp = (
    ("NONE", "None", "Do not interpolate boundaries"),
    ("EDGE_ONLY", "Edge", "Sharp edges"),
    ("EDGE_AND_CORNER", "Edge and Corner", "Sharp edges and corners"),
)

enum_subdivision_fvar_interp = (
    ("NONE", "None", "Smooth everywhere"),
    ("CORNERS_ONLY", "Corner", "Sharp corners only"),
    ("CORNERS_PLUS1", "Edge Corner", "Sharp edge corners only"),
    ("CORNERS_PLUS2", "Edge and Corner",
     "Sharp edges, corners and propagate corners"),
    ("BOUNDARIES", "Boundary", "Sharp all boundaries"),
    ("ALL", "All", "Bilinear everywhere"),
)

enum_subdivision_uv_interp = (
    ("VERTEX", "Vertex", "Smooth based on vertices"),
    ("VARYING", "Varying", "Smooth based on varyings"),
)

enum_primitive_type = (
    ("SPHERE", "Sphere", "Sphere"),
    ("BOX", "Box", "Box"),
    ("PLANE", "Plane", "Plane"),
    ("DISK", "Disk", "Disk"),
    ("CYLINDER", "Cylinder", "Cylinder"),
    ("CONE", "Cone", "Cone"),
    ("QUADRIC", "Quadric", "Quadric"),
)
