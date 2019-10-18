import math


from .entity import inline_entity_matrix


def export_camera(exporter, camera):
    w = exporter.w
    scene = exporter.scene

    w.write("(camera")
    w.goIn()

    aspectW = (camera.data.sensor_width/camera.data.lens)
    aspectH = aspectW#(camera.data.sensor_height/camera.data.lens)

    if scene.render.resolution_x > scene.render.resolution_y:
        aspectH = aspectH * scene.render.resolution_y / scene.render.resolution_x
    else:
        aspectW = aspectW * scene.render.resolution_x / scene.render.resolution_y

    w.write(":name '%s'" % camera.name)
    if camera.data.type == 'ORTHO':
        w.write(":type 'orthographic'")
        w.write(":width %f" % (camera.data.ortho_scale*aspectW))
        w.write(":height %f" % (camera.data.ortho_scale*aspectH))
    else:
        w.write(":type 'standard'")
        w.write(":width %f" % (aspectW))
        w.write(":height %f" % (aspectH))
        w.write(":zoom %f" % camera.data.pearray.zoom)
        w.write(":fstop %f" % camera.data.pearray.fstop)
        w.write(":apertureRadius %f" % camera.data.pearray.apertureRadius)

    w.write(":localDirection [0,0,-1]")
    w.write(":localUp [0,-1,0]")
    w.write(":localRight [1,0,0]")
    inline_entity_matrix(exporter, camera)

    w.goOut()
    w.write(")")