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

### Scene
class PearRaySceneProperties(PropertyGroup):
    scene_name = StringProperty(
        name="Scene Name",
        description="Name of PearRay scene to create. Empty name will use "
                    "the name of the blend file",
        maxlen=1024
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
        default='NONE',
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
class PearRayPreferences(AddonPreferences):
    bl_idname = __package__
    
    filepath_pearray = StringProperty(
                name="Binary Location",
                description="Path to renderer executable",
                subtype='FILE_PATH',
                )
    def draw(self, context):
        layout = self.layout
        layout.prop(self, "filepath_pearray")


def register():
    bpy.types.Scene.pearray = PointerProperty(type=PearRaySceneProperties)
    bpy.types.Camera.pearray = PointerProperty(type=PearRayCameraProperties)


def unregister():
    del bpy.types.Scene.pearray
    del bpy.types.Camera.pearray
    