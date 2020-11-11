import collections
import bpy
import mathutils
from .entity import inline_entity_matrix


def rvec3(v):
    return round(v[0], 6), round(v[1], 6), round(v[2], 6)


def rvec2(v):
    return round(v[0], 6), round(v[1], 6)


def export_mesh_data(exporter, name, mesh):
    w = exporter.w

    mesh.transform(exporter.M_WORLD)
    if exporter.M_WORLD.is_negative:
        mesh.flip_normals()
    mesh.calc_loop_triangles()

    has_uv = bool(mesh.uv_layers)
    if has_uv:
        uv_layer = mesh.uv_layers.active
        if not uv_layer:
            has_uv = False
        else:
            uv_layer = uv_layer.data

    orig_verts = mesh.vertices
    vert_dict = {}
    vert_uniq = []
    vert_count = 0
    face_map = []

    uvcoord = uvcoord_key = normal = normal_key = None

    for f in mesh.loop_triangles:
        smooth = f.use_smooth
        if not smooth:
            normal = f.normal[:]
            normal_key = rvec3(normal)

        if has_uv:
            uv = [uv_layer[l].uv[:] for l in f.loops]

        local_ids = []
        for j, vidx in enumerate(f.vertices):
            v = orig_verts[vidx]

            if smooth:
                normal = v.normal[:]
                normal_key = rvec3(normal)

            if has_uv:
                uvcoord = uv[j][0], uv[j][1]
                uvcoord_key = rvec2(uvcoord)
            else:
                uvcoord = None
                uvcoord_key = None

            key = vidx, normal_key, uvcoord_key
            id = vert_dict.get(key)
            if id is None:
                id = vert_dict[key] = vert_count
                vert_uniq.append((vidx, normal, uvcoord))
                vert_count += 1

            local_ids.append(id)

        face_map.append(local_ids)

    w.write("(mesh")
    w.goIn()

    w.write(":name '%s'" % name)

    # Vertices
    w.write("(attribute")
    w.goIn()
    w.write(":type 'p'")
    w.write(",".join("[%f, %f, %f]" % mesh.vertices[v[0]].co[:]
                     for v in vert_uniq))
    w.goOut()
    w.write(")")

    # Normals
    w.write("(attribute")
    w.goIn()
    w.write(":type 'n'")
    w.write(",".join("[%f, %f, %f]" % v[1][:] for v in vert_uniq))
    w.goOut()
    w.write(")")

    # UV
    if has_uv:
        w.write("(attribute")
        w.goIn()
        w.write(":type 'uv'")
        w.write(",".join("[%f, %f]" % v[2][:] for v in vert_uniq))
        w.goOut()
        w.write(")")

    # Material Indices
    if len(mesh.materials) > 1:
        w.write("(materials")
        w.goIn()
        w.write(",".join(str(f.material_index) for f in mesh.loop_triangles))
        w.goOut()
        w.write(")")

    # Faces
    w.write("(faces")
    w.goIn()
    w.write(",".join("[" + ",".join(str(v) for v in face_map[f.index]) + "]"
                     for f in mesh.loop_triangles))
    w.goOut()
    w.write(")")

    w.goOut()
    w.write(")")

    return name


def export_mesh_only(exporter, obj):
    try:
        mesh = obj.to_mesh()
    except:
        print("Couldn't export %s as mesh" % obj.name)
        return None

    name = exporter.register_unique_name('MESH', obj.data.name)
    name = export_mesh_data(exporter, name, mesh)
    obj.to_mesh_clear()

    return name


def export_mesh_material_part(exporter, obj):
    w = exporter.w
    if len(obj.data.materials) == 1 and obj.data.materials[0] is not None:
        w.write(":materials '%s'" % obj.data.materials[0].name)
    elif len(obj.data.materials) > 1:
        w.write(":materials [%s]" % ', '.join(
            ['"%s"' % (m.name if m is not None else exporter.MISSING_MAT) for m in obj.data.materials]))
    else:
        w.write(":materials '%s'" % exporter.MISSING_MAT)
        print("Mesh %s has no material!" % obj.name)


def export_mesh(exporter, instance):
    w = exporter.w

    name = exporter.get_mesh_name(instance.object.data.name)
    if name is None:
        name = export_mesh_only(exporter, instance.object)
        exporter.register_mesh(name, instance.object.data.name)

    obj = instance.instance_object if instance.is_instance else instance.object
    w.write("(entity")
    w.goIn()

    w.write(":name '%s'" % obj.name)

    if not obj.data.pearray.subdivision:
        w.write(":type 'mesh'")
    else:
        w.write(":type 'subdiv'")
        w.write(":max_level %i" % obj.data.pearray.subdivision_max_level)
        w.write(":adaptive %s" %
                ("true" if obj.data.pearray.subdivision_adaptive else "false"))
        w.write(":scheme '%s'" % obj.data.pearray.subdivision_scheme.lower())
        w.write(":boundary_interpolation '%s'" %
                obj.data.pearray.subdivision_boundary_interp.lower())
        w.write(":uv_interpolation '%s'" %
                obj.data.pearray.subdivision_uv_interp.lower())
        w.write(":fvar_interpolation '%s'" %
                obj.data.pearray.subdivision_fvar_interp.lower())

    export_mesh_material_part(exporter, obj)

    w.write(":mesh '%s'" % name)
    inline_entity_matrix(exporter, obj)

    w.goOut()
    w.write(")")
