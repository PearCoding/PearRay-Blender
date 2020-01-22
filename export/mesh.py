import collections
import bpy
import mathutils
from .entity import inline_entity_matrix


def export_mesh_data(exporter, name, mesh):
    w = exporter.w
    mesh.calc_loop_triangles()

    w.write("(mesh")
    w.goIn()

    w.write(":name '%s'" % name)

    # Vertices
    w.write("(attribute")
    w.goIn()
    w.write(":type 'p'")
    w.write(",".join("[%f, %f, %f]" % v.co[:] for v in mesh.vertices))
    w.goOut()
    w.write(")")

    # Normals
    w.write("(attribute")
    w.goIn()
    w.write(":type 'n'")
    w.write(",".join("[%f, %f, %f]" % v.normal[:] for v in mesh.vertices))
    w.goOut()
    w.write(")")

    # UV (TODO)
    uv_layer = mesh.uv_layers.active.data
    if uv_layer:
        w.write("(attribute")
        w.goIn()
        w.write(":type 'uv'")
        w.write(",".join("[%f, %f]" % v.uv[:] for v in uv_layer))
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
    for f in mesh.loop_triangles:
        w.write("[" + ",".join(str(mesh.vertices[v].index)
                               for v in f.vertices) + "]")

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
    if len(obj.data.materials) == 1:
        w.write(":materials '%s'" % obj.data.materials[0].name)
    elif len(obj.data.materials) > 1:
        w.write(":materials [%s]" % ', '.join(
            ['"%s"' % m.name for m in obj.data.materials]))
    else:
        w.write(":materials '%s'" % exporter.MISSING_MAT)
        print("Mesh %s has no material!" % obj.name)


def export_mesh(exporter, instance):
    w = exporter.w

    name = exporter.get_mesh_name(instance.object)
    if name is None:
        name = export_mesh_only(exporter, instance.object)
        exporter.register_mesh(name, instance.object)

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
