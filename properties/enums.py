
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
    ('EMISSION', "Emission", "Show emission part of the rendering equation"),
    ('VALIDITY', "Validity", "Show if material is valid"),
    )

enum_pixel_sampler_mode= (
	("RAND", "Random", "Random sampling technique"),
	("UNIF", "Uniform", "Uniform sampling technique"),
	("JITT", "Jitter", "Jitter sampling technique"),
	("MJITT", "Multi-Jitter", "Multi-Jitter sampling technique"),
	("HALTON", "Halton QMC", "Quasi-Monte Carlo sampling method based on the Halton sequence"),
    )

enum_integrator_mode= (
    ('DI', "Direct", "Direct Rendering"),
    ('BIDI', "Bi-Direct", "Bidirect Rendering"),
    ('PPM', "Progressive Photon Mapping", "Progressive Photon Mapping"),
    )

enum_photon_gathering_mode= (
	("DOME", "Dome", "Gather only front side of surface"),
	("SPHERE", "Sphere", "Gather around a point"),
    )

enum_color_type= (
	("COLOR", "Color", "Standard RGB value"),
	("TEMP", "Temperature", "Blackbody Temperature in Kelvin"),
    )

enum_material_brdf= (
	("DIFFUSE", "Diffuse", "Simple lambertian material"),
	("ORENNAYAR", "Oren-Nayar", "Oren-Nayar BRDF"),
	("WARD", "Ward", "Ward BRDF"),
	("GRID", "Grid", "Special material grid"),
	("GLASS", "Glass", "Specialized glass material"),
	("MIRROR", "Mirror", "Specialized mirror material"),
    )