import bpy
from mathutils import Matrix

from bpy.props import (
    StringProperty,
    BoolProperty,
    FloatProperty,
    EnumProperty,
    CollectionProperty,
)

from bpy_extras.io_utils import (
    ExportHelper,
    orientation_helper,
    axis_conversion,
)

from .. import export


@orientation_helper(axis_forward='Z', axis_up='Y')
class ExportPRC(bpy.types.Operator, ExportHelper):
    """Export a PearRay file"""
    bl_idname = "export_scene.prc"
    bl_label = "Export PearRay"
    bl_description = "Export to PearRay format"
    bl_options = {'UNDO'}

    filename_ext = ".prc"
    filter_glob: StringProperty(default="*.prc", options={'HIDDEN'})
    use_selection: BoolProperty(
        name="Selection Only",
        description="Export selected objects only",
        default=False)
    external_mesh_files: BoolProperty(
        name="External Mesh Files",
        description="Export meshes into their own prc file in generated/. Recommended",
        default=True)

    global_scale: FloatProperty(
        name="Scale",
        min=0.01, max=1000.0,
        default=1.0,
    )

    check_extension = True

    def draw(self, context):
        pass

    def execute(self, context):
        if not self.filepath:
            raise Exception("filepath not set")

        global_matrix = (Matrix.Scale(self.global_scale, 4) @
                         axis_conversion(to_forward=self.axis_forward,
                                         to_up=self.axis_up,
                                         ).to_4x4())

        scene_exporter = export.Exporter(
            self.filepath, context.evaluated_depsgraph_get())
        scene_exporter.M_WORLD = global_matrix
        scene_exporter.EXTERNAL_MESH_FILES = self.external_mesh_files
        scene_exporter.write_scene()

        return {'FINISHED'}


class PR_PT_export_include(bpy.types.Panel):
    bl_space_type = 'FILE_BROWSER'
    bl_region_type = 'TOOL_PROPS'
    bl_label = "Include"
    bl_parent_id = "FILE_PT_operator"

    @classmethod
    def poll(cls, context):
        sfile = context.space_data
        operator = sfile.active_operator

        return operator.bl_idname == "EXPORT_SCENE_OT_prc"

    def draw(self, context):
        layout = self.layout
        layout.use_property_split = True
        layout.use_property_decorate = False  # No animation.

        sfile = context.space_data
        operator = sfile.active_operator

        layout.prop(operator, 'use_selection')


class PR_PT_export_transform(bpy.types.Panel):
    bl_space_type = 'FILE_BROWSER'
    bl_region_type = 'TOOL_PROPS'
    bl_label = "Transform"
    bl_parent_id = "FILE_PT_operator"

    @classmethod
    def poll(cls, context):
        sfile = context.space_data
        operator = sfile.active_operator

        return operator.bl_idname == "EXPORT_SCENE_OT_prc"

    def draw(self, context):
        layout = self.layout
        layout.use_property_split = True
        layout.use_property_decorate = False  # No animation.

        sfile = context.space_data
        operator = sfile.active_operator

        layout.prop(operator, 'global_scale')
        layout.prop(operator, 'axis_forward')
        layout.prop(operator, 'axis_up')


class PR_PT_export_output(bpy.types.Panel):
    bl_space_type = 'FILE_BROWSER'
    bl_region_type = 'TOOL_PROPS'
    bl_label = "Output"
    bl_parent_id = "FILE_PT_operator"

    @classmethod
    def poll(cls, context):
        sfile = context.space_data
        operator = sfile.active_operator

        return operator.bl_idname == "EXPORT_SCENE_OT_prc"

    def draw(self, context):
        layout = self.layout
        layout.use_property_split = True
        layout.use_property_decorate = False  # No animation.

        sfile = context.space_data
        operator = sfile.active_operator

        layout.prop(operator, 'external_mesh_files')


_classes = [ExportPRC,
            PR_PT_export_include, PR_PT_export_transform, PR_PT_export_output]
_bl_register, _bl_unregister = bpy.utils.register_classes_factory(_classes)


def menu_func_export(self, context):
    self.layout.operator(
        ExportPRC.bl_idname, text="PearRay (.prc)")


def register():
    _bl_register()
    bpy.types.TOPBAR_MT_file_export.append(menu_func_export)


def unregister():
    bpy.types.TOPBAR_MT_file_export.remove(menu_func_export)
    _bl_unregister()
