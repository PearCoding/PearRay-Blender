import bpy
import mathutils
from .entity import inline_entity_matrix as inline_entity_matrix

def export_trimesh(exporter, mw, name, mesh):
    if not exporter.scene.pearray.apply_transform:
        M = mathutils.Matrix.Identity(4)
    else:
        M = exporter.M_WORLD * mw

    NM = M.inverted_safe().transposed()

    w = exporter.w

    faces = mesh.tessfaces[:]
    faces_verts = [f.vertices[:] for f in faces]
    faces_norms = [f.normal[:] for f in faces]
    faces_colors = mesh.tessface_vertex_colors[:]
    faces_uv = mesh.tessface_uv_textures[:]

    verts = mesh.vertices
    verts_normals = [v.normal[:] for v in verts]

    if len(verts) < 1:
        return False
    
    #if len(faces_uv) > 0:
    #    if mesh.uv_textures.active and faces_uv.active.data:
    #        uv_layer = faces_uv.active.data
    #else:
    #    uv_layer = None

    w.write("(mesh")
    w.goIn()

    w.write(":name '%s'" % name)
    w.write(":type 'triangles'")

    w.write("(attribute")
    w.goIn()
    line = ":type 'p'"
    for v in verts:
        nv = M * mathutils.Vector(v.co[:])
        line = line + ", [%f, %f, %f]" % nv[:]
    w.write(line)

    w.goOut()
    w.write(")")

    if len(verts_normals) > 0:
        w.write("(attribute")
        w.goIn()
        line = ":type 'n'"
        for n in verts_normals:
            nn = M * mathutils.Vector(n)
            line = line + ", [%f, %f, %f]" % nn[:]
        w.write(line)
        w.goOut()
        w.write(")")

    # TODO: Add UVs, Colors etc.

    line = "(faces"
    for fi, f in enumerate(faces):
        fv = faces_verts[fi]
        if len(fv) == 4:# Cube
            indices = (0, 1, 2), (0, 2, 3)
        else:# Triangle
            indices = ((0, 1, 2),)
        
        for i1, i2, i3 in indices:
            line = line + ", %i, %i, %i" % (fv[i1], fv[i2], fv[i3])
    w.write(line + ")")

    w.goOut()
    w.write(")")

    return True


def export_mesh(exporter, obj):
    w = exporter.w

    # Check if in instance list
    if not obj.data.name in exporter.instances['MESH']:
        try:
            mesh = obj.to_mesh(exporter.scene, True, 'RENDER', calc_tessface=True)
        except:
            print("Couldn't export %s as mesh" % obj.name)
            return
        succ = export_trimesh(exporter, obj.matrix_world, obj.data.name, mesh)
        bpy.data.meshes.remove(mesh)
        
        if not succ:
            print("Couldn't export %s" % obj.name)
            return

    exporter.register_unique_name('MESH', obj.data.name)

    w.write("(entity")
    w.goIn()

    w.write(":name '%s'" % obj.name)
    w.write(":type 'mesh'")

    if len(obj.data.materials) >= 1 and obj.data.materials[0]:
        w.write(":material '%s'" % obj.data.materials[0].name)
    else:
        w.write(":material '%s'" % exporter.MISSING_MAT)
        print("Mesh %s has no material!" % obj.name)
        
    w.write(":mesh '%s'" % obj.data.name)
    if not exporter.scene.pearray.apply_transform:
        inline_entity_matrix(exporter, obj)

    w.goOut()
    w.write(")")