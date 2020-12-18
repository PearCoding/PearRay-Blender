import math
import mathutils


def _inline_entity_matrix(exporter, matrix):
    exporter.w.write(":transform [" + ",".join(
        [",".join(map(str, matrix[i])) for i in range(4)]) + "]")


def inline_entity_matrix(exporter, obj):
    _inline_entity_matrix(exporter, obj.matrix_world)


# Blender uses M = Translation * Rotation * Scale
def inline_entity_uniform(exporter,
                          loc,
                          rot,
                          s,
                          parent_m=mathutils.Matrix.Identity(4)):
    mat_loc = mathutils.Matrix.Translation(loc)

    # Uniform scale
    mat_sca = mathutils.Matrix.Identity(4)*s
    mat_sca[3][3] = 1

    # Create a rotation matrix from a quaternion
    mat_rot = mathutils.Quaternion(rot).to_matrix().to_4x4()

    mat_out = mat_loc @ mat_rot @ mat_sca

    _inline_entity_matrix(exporter, parent_m @ mat_out)
