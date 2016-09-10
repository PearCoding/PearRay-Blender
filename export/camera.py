import math


from .entity import inline_entity_matrix_pos_rot_sign


def export_camera(exporter, camera):
    w = exporter.w
    scene = exporter.scene

    w.write("(entity")
    w.goIn()

    w.write(":name '%s'" % camera.name)
    w.write(":type 'camera'")
        
    aspectW = 1
    aspectH = 1
    if scene.render.resolution_x > scene.render.resolution_y:
        aspectH = scene.render.resolution_y / scene.render.resolution_x
    else:
        aspectW = scene.render.resolution_x / scene.render.resolution_y

    aspectW = exporter.CAM_UNIT_F * aspectW
    aspectH = exporter.CAM_UNIT_F * aspectH

    if camera.data.type == 'ORTHO':
        w.write(":projection 'ortho'")
        w.write(":width %f" % (camera.data.ortho_scale * aspectW))
        w.write(":height %f" % (camera.data.ortho_scale * aspectH))
    else:
        l=1#0.95#???
        w.write(":width %f" % (l*aspectW))
        w.write(":height %f" % (l*aspectH))

    w.write(":zoom %f" % camera.data.pearray.zoom)
    w.write(":fstop %f" % camera.data.pearray.fstop)
    w.write(":apertureRadius %f" % camera.data.pearray.apertureRadius)
    w.write(":localDirection [0,0,-1]")
    w.write(":localUp [0,-1,0]")
    w.write(":localRight [1,0,0]")
    inline_entity_matrix_pos_rot_sign(exporter, camera)

    w.goOut()
    w.write(")")