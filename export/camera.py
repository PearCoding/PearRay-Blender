from .entity import inline_entity_matrix as inline_entity_matrix


def export_camera(exporter, camera):
    w = exporter.w
    scene = exporter.scene
    matrix = exporter.M_WORLD * camera.matrix_world

    w.write("(entity")
    w.goIn()

    w.write(":name '%s'" % camera.name)
    w.write(":type 'camera'")
        
    aspectW = 1
    aspectH = 1
    if scene.render.resolution_x > scene.render.resolution_y:
        aspectW = scene.render.resolution_x / scene.render.resolution_y
    else:
        aspectH = scene.render.resolution_y / scene.render.resolution_x
    
    aspectW = aspectW * exporter.CAM_UNIT_F
    aspectH = aspectH * exporter.CAM_UNIT_F

    if camera.data.type == 'ORTHO':
        w.write(":projection 'orthogonal'" )
        w.write(":width %f" % (camera.data.ortho_scale * aspectW))
        w.write(":height %f" % (camera.data.ortho_scale * aspectH))
    else:
        sw = camera.data.sensor_width
        sh = camera.data.sensor_height
        if camera.data.sensor_fit == 'AUTO':
            if sw > sh:
                sh = sw
            else:
                sw = sh
        elif camera.data.sensor_fit == 'HORIZONTAL':
            sh = sw
        else:
            sw = sh
        
        w.write(":width %f" % (sw * aspectW))
        w.write(":height %f" % (sh * aspectH))

    w.write(":lookAt [%f,%f,%f]" % tuple([e for e in matrix.to_3x3().to_euler()]))
    w.write(":zoom %f" % camera.data.pearray.zoom)
    w.write(":fstop %f" % camera.data.pearray.fstop)
    w.write(":apertureRadius %f" % camera.data.pearray.apertureRadius)
    inline_entity_matrix(exporter, camera)

    w.goOut()
    w.write(")")