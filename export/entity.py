import math
import mathutils


ROT_ORDER='XYZ'
VERBOSE=False

def inline_entity_matrix(exporter, obj):
    matrix = exporter.M_WORLD * obj.matrix_world
    trans, rot, scale = matrix.decompose()

    rot_s = tuple(math.degrees(a) + 0 for a in rot.to_euler(ROT_ORDER))

    if VERBOSE:
        print("%s: %s" % (obj.name, matrix))
        print("-> T: %s, R: %s, S: %s" % (trans, rot_s, scale))

    exporter.w.write(":position [%f,%f,%f]" % tuple(trans))
    exporter.w.write(":rotation (euler %.4f,%.4f,%.4f)" % rot_s)
    exporter.w.write(":scale [%f,%f,%f]" % tuple(scale))


def inline_entity_matrix_pos_rot(exporter, obj):
    matrix = exporter.M_WORLD * obj.matrix_world
    trans, rot, scale = matrix.decompose()

    rot_s = tuple(math.degrees(a) + 0 for a in rot.to_euler(ROT_ORDER))

    if VERBOSE:
        print("%s: %s" % (obj.name, matrix))
        print("-> T: %s, R: %s" % (trans, rot_s))

    exporter.w.write(":position [%f,%f,%f]" % tuple(trans))
    exporter.w.write(":rotation (euler %.4f,%.4f,%.4f)" % rot_s)


def inline_entity_matrix_pos_rot_sign(exporter, obj):
    matrix = exporter.M_WORLD * obj.matrix_world
    trans, rot, scale = matrix.decompose()

    scale.x = math.copysign(1,scale.x)
    scale.y = math.copysign(1,scale.y)
    scale.z = math.copysign(1,scale.z)

    rot_s = tuple(math.degrees(a) + 0 for a in rot.to_euler(ROT_ORDER))

    if VERBOSE:
        print("%s: %s" % (obj.name, matrix))
        print("-> T: %s, R: %s, S: %s" % (trans, rot_s, scale))
    
    exporter.w.write(":position [%f,%f,%f]" % tuple(trans))
    exporter.w.write(":rotation (euler %.4f,%.4f,%.4f)" % rot_s)
    exporter.w.write(":scale [%f,%f,%f]" % tuple(scale))


def inline_entity_matrix_pos(exporter, obj):
    matrix = exporter.M_WORLD * obj.matrix_world
    trans, rot, scale = matrix.decompose()

    if VERBOSE:
        print("%s: %s" % (obj.name, matrix))
        print("-> T: %s" % (trans))
    
    exporter.w.write(":position [%f,%f,%f]" % tuple(trans))