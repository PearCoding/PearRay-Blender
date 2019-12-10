import math
import mathutils


from .entity import inline_entity_matrix


def export_prim_material_part(exporter, obj):
    w = exporter.w
    if len(obj.data.materials) >= 1:
        w.write(":material '%s'" % obj.data.materials[0].name)
    else:
        w.write(":material '%s'" % exporter.MISSING_MAT)
        print("Primitive %s has no material!" % obj.name)


def export_sphere(exporter, prim):
    w = exporter.w

    prim_data = prim.data

    w.write("(entity")
    w.goIn()
    w.write(":name '%s'" % prim.name)
    w.write(":type 'sphere'")
    w.write(":radius %f" % prim_data.pearray.primitive.radius)
    export_prim_material_part(exporter, prim)
    inline_entity_matrix(exporter, prim)
    w.goOut()
    w.write(")")


def export_box(exporter, prim):
    w = exporter.w

    prim_data = prim.data

    w.write("(entity")
    w.goIn()
    w.write(":name '%s'" % prim.name)
    w.write(":type 'box'")
    w.write(":width %f" % prim_data.pearray.primitive.width)
    w.write(":height %f" % prim_data.pearray.primitive.height)
    w.write(":depth %f" % prim_data.pearray.primitive.depth)
    export_prim_material_part(exporter, prim)
    inline_entity_matrix(exporter, prim)
    w.goOut()
    w.write(")")


def export_cylinder(exporter, prim):
    w = exporter.w

    prim_data = prim.data

    w.write("(entity")
    w.goIn()
    w.write(":name '%s'" % prim.name)
    w.write(":type 'cylinder'")
    w.write(":base_radius %f" % prim_data.pearray.primitive.radius)
    w.write(":top_radius %f" % prim_data.pearray.primitive.top_radius)
    w.write(":height %f" % prim_data.pearray.primitive.width)
    export_prim_material_part(exporter, prim)
    inline_entity_matrix(exporter, prim)
    w.goOut()
    w.write(")")


def export_cone(exporter, prim):
    w = exporter.w

    prim_data = prim.data

    w.write("(entity")
    w.goIn()
    w.write(":name '%s'" % prim.name)
    w.write(":type 'cone'")
    w.write(":base_radius %f" % prim_data.pearray.primitive.radius)
    w.write(":top_radius %f" % prim_data.pearray.primitive.top_radius)
    w.write(":height %f" % prim_data.pearray.primitive.width)
    export_prim_material_part(exporter, prim)
    inline_entity_matrix(exporter, prim)
    w.goOut()
    w.write(")")


def export_plane(exporter, prim):
    w = exporter.w

    prim_data = prim.data

    w.write("(entity")
    w.goIn()
    w.write(":name '%s'" % prim.name)
    w.write(":type 'plane'")
    w.write(":centering true")
    w.write(":width %f" % prim_data.pearray.primitive.width)
    w.write(":height %f" % prim_data.pearray.primitive.height)
    export_prim_material_part(exporter, prim)
    inline_entity_matrix(exporter, prim)
    w.goOut()
    w.write(")")


def export_disk(exporter, prim):
    w = exporter.w

    prim_data = prim.data

    w.write("(entity")
    w.goIn()
    w.write(":name '%s'" % prim.name)
    w.write(":type 'disk'")
    w.write(":radius %f" % prim_data.pearray.primitive.radius)
    export_prim_material_part(exporter, prim)
    inline_entity_matrix(exporter, prim)
    w.goOut()
    w.write(")")


def export_quadric(exporter, prim):
    w = exporter.w

    prim_data = prim.data

    w.write("(entity")
    w.goIn()
    w.write(":name '%s'" % prim.name)
    w.write(":type 'quadric'")
    w.write(":parameters [%s]" % (",".join(str(f) for f in prim_data.pearray.primitive.parameters)))
    export_prim_material_part(exporter, prim)
    inline_entity_matrix(exporter, prim)
    w.goOut()
    w.write(")")


def export_primitive(exporter, prim):
    if prim.type != 'MESH' or not prim.data.pearray.is_primitive:
        return

    prim_type = prim.data.pearray.primitive.primitive_type
    if prim_type == 'SPHERE':
        export_sphere(exporter, prim)
    elif prim_type == 'BOX':
        export_box(exporter, prim)
    elif prim_type == 'CYLINDER':
        export_cylinder(exporter, prim)
    elif prim_type == 'CONE':
        export_cone(exporter, prim)
    elif prim_type == 'PLANE':
        export_plane(exporter, prim)
    elif prim_type == 'DISK':
        export_disk(exporter, prim)
    elif prim_type == 'QUADRIC':
        export_quadric(exporter, prim)
    else:
        print("PearRay does not support primitives of type '%s'" % prim_type)
