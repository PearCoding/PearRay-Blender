def inline_entity_matrix(exporter, obj):
    matrix = exporter.M_WORLD * obj.matrix_world
    trans, rot, scale = matrix.decompose()

    exporter.w.write(":position [%f,%f,%f]" % tuple(trans))
    exporter.w.write(":rotation [%f,%f,%f,%f]" % (rot.x, rot.y, rot.z, rot.w))
    exporter.w.write(":scale [%f,%f,%f]" % tuple(scale))