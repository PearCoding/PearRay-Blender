import math
import mathutils


from .entity import inline_entity_matrix
from .material import export_color

def write_emission(exporter, light):
    w = exporter.w
    color_name = export_color(exporter, light.data, 'color', True)
    light_mat_n = exporter.register_unique_name('EMISSION', light.name + "_em")

    w.write("(emission")
    w.goIn()

    w.write(":name '%s'" % light_mat_n)
    w.write(":type 'standard'")
    w.write(":emission %s" % color_name)
    if not light.data.pearray.camera_visible:
        w.write(":camera_visible false")
    else:
        w.write(":albedo %s" % color_name)

    w.goOut()
    w.write(")")
    return light_mat_n


def export_pointlight(exporter, light):
    w = exporter.w

    light_data = light.data
    w.write("; Light %s" % light.name)

    light_mat_n = write_emission(exporter, light)

    w.write("(entity")
    w.goIn()

    w.write(":name '%s'" % light.name)
    w.write(":type 'sphere'")
    w.write(":radius %f" % light_data.pearray.point_radius)# Really?
    w.write(":emission '%s'" % light_mat_n)
    inline_entity_matrix(exporter, light)

    w.goOut()
    w.write(")")


def export_arealight(exporter, light):
    w = exporter.w
    light_data = light.data
    w.write("; Light %s" % light.name)

    if light_data.shape == 'SQUARE':
        ysize = light_data.size
    else:
        ysize = light_data.size_y

    light_mat_n = write_emission(exporter, light)

    w.write("(entity")
    w.goIn()

    w.write(":name '%s'" % light.name)
    w.write(":type 'plane'")
    w.write(":centering true")
    w.write(":xAxis %f" % light_data.size)
    w.write(":yAxis %f" % (-ysize))
    w.write(":emission '%s'" % light_mat_n)
    inline_entity_matrix(exporter, light)

    w.goOut()
    w.write(")")


def export_sunlight(exporter, light):
    w = exporter.w
    light_data = light.data
    w.write("; Light %s" % light.name)

    light_mat_n = write_emission(exporter, light)

    matrix = exporter.M_WORLD * light.matrix_world
    trans, rot, scale = matrix.decompose()
    direction = rot * mathutils.Vector((0, 0, -1))
    w.write("(light")
    w.goIn()

    w.write(":type 'distant'")
    w.write(":direction [%f, %f, %f]" % direction[:])
    w.write(":emission '%s'" % light_mat_n)

    w.goOut()
    w.write(")")


def export_light(exporter, light):
    if light.data.type == 'POINT' or light.data.type == 'SPOT':
        export_pointlight(exporter, light)# Interpret as spherical area light
    elif light.data.type == 'HEMI' or light.data.type == 'AREA':
        export_arealight(exporter, light)
    elif light.data.type == 'SUN':
        export_sunlight(exporter, light)
    else:
        print("PearRay does not support lights of type '%s'" % light.data.type)
