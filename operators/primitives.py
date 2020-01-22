import bpy


class OBJECT_OT_AddSphereOperator(bpy.types.Operator):
    bl_idname = "pr.add_sphere"
    bl_label = "Sphere"
    bl_description = "Add Sphere"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        bpy.ops.mesh.primitive_uv_sphere_add(radius=1.0)
        sphere = bpy.context.object

        sphere.display_type = 'WIRE'

        sphere.data.pearray.is_primitive = True
        sphere.data.pearray.primitive.primitive_type = 'SPHERE'
        sphere.data.pearray.primitive.radius = 1.0

        return {'FINISHED'}


class OBJECT_OT_AddCylinderOperator(bpy.types.Operator):
    bl_idname = "pr.add_cylinder"
    bl_label = "Cylinder"
    bl_description = "Add Cylinder"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        bpy.ops.mesh.primitive_cylinder_add(radius=1.0, depth=1.0)
        obj = bpy.context.object

        obj.display_type = 'WIRE'

        obj.data.pearray.is_primitive = True
        obj.data.pearray.primitive.primitive_type = 'CYLINDER'
        obj.data.pearray.primitive.radius = 1.0
        obj.data.pearray.primitive.top_radius = 1.0
        obj.data.pearray.primitive.height = 1.0

        return {'FINISHED'}


class OBJECT_OT_AddConeOperator(bpy.types.Operator):
    bl_idname = "pr.add_cone"
    bl_label = "Cone"
    bl_description = "Add Cone"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        bpy.ops.mesh.primitive_cone_add(radius1=1.0, depth=1.0)
        obj = bpy.context.object

        obj.display_type = 'WIRE'

        obj.data.pearray.is_primitive = True
        obj.data.pearray.primitive.primitive_type = 'CONE'
        obj.data.pearray.primitive.radius = 1.0
        obj.data.pearray.primitive.height = 1.0

        return {'FINISHED'}


class OBJECT_OT_AddBoxOperator(bpy.types.Operator):
    bl_idname = "pr.add_box"
    bl_label = "Box"
    bl_description = "Add Box"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        bpy.ops.mesh.primitive_cube_add(size=1.0)
        obj = bpy.context.object

        obj.display_type = 'WIRE'

        obj.data.pearray.is_primitive = True
        obj.data.pearray.primitive.primitive_type = 'BOX'

        return {'FINISHED'}


class OBJECT_OT_AddPlaneOperator(bpy.types.Operator):
    bl_idname = "pr.add_plane"
    bl_label = "Plane"
    bl_description = "Add Plane"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        bpy.ops.mesh.primitive_plane_add(size=1.0)
        obj = bpy.context.object

        obj.display_type = 'WIRE'

        obj.data.pearray.is_primitive = True
        obj.data.pearray.primitive.primitive_type = 'PLANE'

        return {'FINISHED'}


class OBJECT_OT_AddDiskOperator(bpy.types.Operator):
    bl_idname = "pr.add_disk"
    bl_label = "Disk"
    bl_description = "Add Disk"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        bpy.ops.mesh.primitive_circle_add(radius=1.0)
        obj = bpy.context.object

        obj.display_type = 'WIRE'

        obj.data.pearray.is_primitive = True
        obj.data.pearray.primitive.primitive_type = 'DISK'

        return {'FINISHED'}


class OBJECT_OT_AddQuadricOperator(bpy.types.Operator):
    bl_idname = "pr.add_quadric"
    bl_label = "Quadric"
    bl_description = "Add Quadric"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        bpy.ops.mesh.primitive_cube_add(size=1.0)
        obj = bpy.context.object

        obj.display_type = 'WIRE'

        obj.data.pearray.is_primitive = True
        obj.data.pearray.primitive.primitive_type = 'QUADRIC'

        return {'FINISHED'}


# Menu
class VIEW3D_MT_add_primitives(bpy.types.Menu):
    bl_idname = 'VIEW3D_MT_add_primitives'
    bl_label = 'Primitives'

    def draw(self, context):
        layout = self.layout
        layout.operator(OBJECT_OT_AddSphereOperator.bl_idname)
        layout.operator(OBJECT_OT_AddBoxOperator.bl_idname)
        layout.operator(OBJECT_OT_AddCylinderOperator.bl_idname)
        layout.operator(OBJECT_OT_AddConeOperator.bl_idname)
        layout.operator(OBJECT_OT_AddPlaneOperator.bl_idname)
        layout.operator(OBJECT_OT_AddDiskOperator.bl_idname)
        layout.operator(OBJECT_OT_AddQuadricOperator.bl_idname)


_classes = [OBJECT_OT_AddSphereOperator, OBJECT_OT_AddBoxOperator, OBJECT_OT_AddCylinderOperator, OBJECT_OT_AddConeOperator, OBJECT_OT_AddPlaneOperator,
            OBJECT_OT_AddDiskOperator, OBJECT_OT_AddQuadricOperator, VIEW3D_MT_add_primitives]
_bl_register, _bl_unregister = bpy.utils.register_classes_factory(_classes)

def _sub_menu(self, context):
    self.layout.menu("VIEW3D_MT_add_primitives")

def register():
    _bl_register()
    bpy.types.VIEW3D_MT_add.append(_sub_menu)

def unregister():
    bpy.types.VIEW3D_MT_add.remove(_sub_menu)
    _bl_unregister()
