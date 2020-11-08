import bpy

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
class PearRayExportSceneOperator(bpy.types.Operator, ExportHelper):
    """Export a PearRay file"""
    bl_idname = "pr.export"
    bl_label = "Export PearRay"
    bl_description = "Export to PearRay format"
    bl_options = {'UNDO'}

    filename_ext = ".pr"
    filter_glob: StringProperty(default="*.pr", options={'HIDDEN'})

    def draw(self, context):
        pass

    def execute(self, context):
        if not self.filepath:
            raise Exception("filepath not set")

        global_matrix = (axis_conversion(to_forward=self.axis_forward,
                                         to_up=self.axis_up,
                                         ).to_4x4())

        scene_exporter = export.Exporter(self.filepath, context.evaluated_depsgraph_get())
        scene_exporter.M_WORLD = global_matrix
        scene_exporter.write_scene()

        return {'FINISHED'}


_classes = [PearRayExportSceneOperator]
_bl_register, _bl_unregister = bpy.utils.register_classes_factory(_classes)


def menu_func_export(self, context):
	self.layout.operator(
	    PearRayExportSceneOperator.bl_idname, text="PearRay (.pr)")


def register():
    _bl_register()
    bpy.types.TOPBAR_MT_file_export.append(menu_func_export)


def unregister():
    bpy.types.TOPBAR_MT_file_export.remove(menu_func_export)
    _bl_unregister()
