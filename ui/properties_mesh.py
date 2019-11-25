import bpy


from bl_ui.properties_data_mesh import MeshButtonsPanel


class DATA_PT_pr_mesh_subdivision(MeshButtonsPanel, bpy.types.Panel):
    bl_label = "Subdivision"
    COMPAT_ENGINES = {'PEARRAY_RENDER'}
    
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
        

from bl_ui import properties_data_mesh
for member in dir(properties_data_mesh):
    subclass = getattr(properties_data_mesh, member)
    try:
        subclass.COMPAT_ENGINES.add('PEARRAY_RENDER')
    except:
        pass
del properties_data_mesh