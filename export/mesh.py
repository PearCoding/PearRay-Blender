import collections
import bpy
import mathutils
from .entity import inline_entity_matrix


def export_mesh_data(exporter, mw, name, mesh):
    w = exporter.w

    # First collect vertex data
    faces = mesh.tessfaces[:]
    uv_tex = mesh.tessface_uv_textures

    if len(uv_tex) > 0 and uv_tex.active and uv_tex.active.data:
        uv_layer = uv_tex.active.data
    else:
        uv_layer = None

    vertex_color = mesh.tessface_vertex_colors.active
    if vertex_color:
        color_layer = vertex_color.data
    else:
        color_layer = None

    face_indices = []
    material_indices = []
    points = []
    normals = []
    uvs = []
    colors = []

    # Temporary
    vert_index = 0
    vert_indices = {}
    vert_cache = set()

    for face in faces:
        face_data = []

        for j, vertex in enumerate(face.vertices):
            v = mesh.vertices[vertex]

            if uv_layer:
                uv = uv_layer[face.index].uv[j]

            if color_layer:
                if j == 0:
                    color = color_layer[face.index].color1
                elif j == 1:
                    color = color_layer[face.index].color2
                elif j == 2:
                    color = color_layer[face.index].color3
                elif j == 3:
                    color = color_layer[face.index].color4

            if face.use_smooth:
                #if uv_layer:
                #    if color_layer:
                #        vert_data = (v.co[:], v.normal[:], uv[:], color[:])
                #    else:
                #        vert_data = (v.co[:], v.normal[:], uv[:])
                #else:
                #    if color_layer:
                #        vert_data = (v.co[:], v.normal[:], color[:])
                #    else:
                #        vert_data = (v.co[:], v.normal[:])

                vert_data = (v.co[:], v.normal[:])
                if vert_data not in vert_cache:
                    vert_cache.add(vert_data)

                    points.append(v.co[:])
                    normals.append(v.normal[:])

                    if uv_layer:
                        uvs.append(uv[:])

                    if color_layer:
                        colors.append(color[:])

                    vert_indices[vert_data] = vert_index
                    face_data.append(vert_index)

                    vert_index += 1
                else:
                    face_data.append(vert_indices[vert_data])
            else:
                # They are always unique
                points.append(v.co[:])
                normals.append(face.normal[:])

                if uv_layer:
                    uvs.append(uv[:])

                if color_layer:
                    colors.append(color[:])

                face_data.append(vert_index)

                vert_index += 1

        if not len(face_data) in (3, 4):
            print("Mesh %s contains non triangle or quad face" % obj.name)
        face_indices.append(face_data[0:max(4, len(face_data))])
        material_indices.append(face.material_index)

    del vert_indices
    del vert_cache

    n, in_cache = exporter.register_mesh_data(
        name, (points, normals, uvs, colors, face_indices, material_indices))
    if in_cache:
        return n

    w.write("(mesh")
    w.goIn()

    w.write(":name '%s'" % name)

    w.write("(attribute")
    w.goIn()
    line = ":type 'p'"
    for v in points:
        line = line + ", [%f, %f, %f]" % v[:]
    w.write(line)

    w.goOut()
    w.write(")")

    w.write("(attribute")
    w.goIn()
    line = ":type 'n'"
    for n in normals:
        line = line + ", [%f, %f, %f]" % n[:]
    w.write(line)
    w.goOut()
    w.write(")")

    if uv_layer:
        w.write("(attribute")
        w.goIn()
        line = ":type 't'"
        for uv in uvs:
            line = line + ", [%f, %f]" % uv[:]
        w.write(line)
        w.goOut()
        w.write(")")

    if color_layer:
        w.write("(attribute")
        w.goIn()
        w.write(":type 'u'")
        line = ":name 'color'"
        for c in colors:
            line = line + ", [%f, %f, %f, 1]" % c[:]
        w.write(line)
        w.goOut()
        w.write(")")

    w.write("(materials")
    w.goIn()
    w.write(",".join(map(str, material_indices)))
    w.goOut()
    w.write(")")

    w.write("(faces")
    w.goIn()
    w.write(",".join("[" + ",".join(map(str, f)) + "]" for f in face_indices))
    w.goOut()
    w.write(")")

    w.goOut()
    w.write(")")

    del face_indices
    del material_indices
    del points
    del normals
    del uvs
    del colors

    return name


def export_mesh_only(exporter, obj, has_subsurf):
    try:
        mesh = obj.to_mesh(
            exporter.scene,
            not has_subsurf,
            'RENDER',
            calc_tessface=True,
            calc_undeformed=True)
    except:
        print("Couldn't export %s as mesh" % obj.name)
        return None

    name = exporter.register_unique_name('MESH', obj.data.name)
    name = export_mesh_data(exporter, obj.matrix_world, name, mesh)
    bpy.data.meshes.remove(mesh)

    return name

def export_mesh_material_part(exporter, obj):
    w = exporter.w
    if len(obj.data.materials) == 1:
        w.write(":materials '%s'" % obj.data.materials[0].name)
    elif len(obj.data.materials) > 1:
        w.write(":materials [%s]" % ', '.join(
            ['"%s"' % m.name for m in obj.data.materials]))
    else:
        w.write(":materials '%s'" % exporter.MISSING_MAT)
        print("Mesh %s has no material!" % obj.name)


def export_mesh(exporter, obj):
    w = exporter.w

    subsurf_modifiers = [m for m in obj.modifiers if m.type == 'SUBSURF' and m.show_render]
    has_subsurf = len(subsurf_modifiers) > 0

    if len(subsurf_modifiers) > 1:
        print("Object %s has more then one subsurf modifiers. Ignoring others except first one" % obj.name)

    if has_subsurf and len(obj.modifiers) != 1:
        print("Object %s has other modifiers. Can not apply them when subsurf modifier is present" % obj.name)

    name = export_mesh_only(exporter, obj, has_subsurf)
    if not name:
        return

    w.write("(entity")
    w.goIn()

    w.write(":name '%s'" % obj.name)

    if not has_subsurf:
        w.write(":type 'mesh'")
    else:
        w.write(":type 'subdiv'")
        w.write(":max_subdivision %i" % subsurf_modifiers[0].render_levels)
        #w.write(":use_creases %s" % ("true" if subsurf_modifiers[0].use_creases else "false"))

    export_mesh_material_part(exporter, obj)

    w.write(":mesh '%s'" % name)
    inline_entity_matrix(exporter, obj)

    w.goOut()
    w.write(")")