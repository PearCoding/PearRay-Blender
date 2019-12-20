import bpy


from bl_ui.properties_data_mesh import MeshButtonsPanel


class DATA_PT_pr_mesh_subdivision(MeshButtonsPanel, bpy.types.Panel):
    bl_label = "Subdivision"
    COMPAT_ENGINES = {'PEARRAY_RENDER'}

    @classmethod
    def poll(cls, context):
        return context.mesh and not context.mesh.pearray.is_primitive

    def draw_header(self, context):
        layout = self.layout
        mesh = context.mesh
        layout.prop(mesh.pearray, "subdivision", text="")

    def draw(self, context):
        layout = self.layout

        mesh = context.mesh
        layout.enabled = mesh.pearray.subdivision

        row = layout.row(align=True)
        row.prop(mesh.pearray, "subdivision_scheme", text="")
        row.prop(mesh.pearray, "subdivision_max_level", text="Level")

        layout.prop(mesh.pearray, "subdivision_adaptive", text="Adaptive")

        col = layout.column(align=True)
        col.prop(mesh.pearray, "subdivision_boundary_interp", text="Boundary")
        col.prop(mesh.pearray, "subdivision_uv_interp", text="UV")
        col.prop(mesh.pearray, "subdivision_fvar_interp", text="Face Varying")


class DATA_PT_pr_mesh_primitive(MeshButtonsPanel, bpy.types.Panel):
    bl_label = "Primitive"
    COMPAT_ENGINES = {'PEARRAY_RENDER'}

    @classmethod
    def poll(cls, context):
        return context.mesh and context.mesh.pearray.is_primitive

    def draw(self, context):
        layout = self.layout

        mesh = context.mesh
        prim = mesh.pearray.primitive

        col = layout.column()
        col.enabled = False
        col.prop(prim, 'primitive_type')

        if prim.primitive_type == 'SPHERE' or prim.primitive_type == 'DISK':
            layout.prop(prim, 'radius')
        elif prim.primitive_type == 'BOX':
            col = layout.column(align=True)
            col.prop(prim, 'width')
            col.prop(prim, 'height')
            col.prop(prim, 'depth')
        elif prim.primitive_type == 'CYLINDER':
            col = layout.column(align=True)
            col.prop(prim, 'radius', text='Base Radius')
            col.prop(prim, 'top_radius', text='Top Radius')
            col.prop(prim, 'height')
        elif prim.primitive_type == 'CONE':
            col.prop(prim, 'radius')
            col.prop(prim, 'height')
        elif prim.primitive_type == 'PLANE':
            layout.prop(prim, 'width')
            layout.prop(prim, 'height')
        elif prim.primitive_type == 'QUADRIC':
            layout.prop(prim, 'parameters')


from bl_ui import properties_data_mesh
for member in dir(properties_data_mesh):
    subclass = getattr(properties_data_mesh, member)
    try:
        subclass.COMPAT_ENGINES.add('PEARRAY_RENDER')
    except:
        pass
del properties_data_mesh
