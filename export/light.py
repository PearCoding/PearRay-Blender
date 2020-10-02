import math
import mathutils


from .entity import inline_entity_matrix
from .node import export_node


def write_emission(exporter, light, factor=1):
    w = exporter.w
    node_name = export_node(exporter, light.name, light.data.color, True, factor, asLight=True)
    light_mat_n = exporter.register_unique_name('EMISSION', light.name + "_em")
    energy = light.data.energy

    w.write("(emission")
    w.goIn()

    w.write(":name '%s'" % light_mat_n)
    w.write(":type 'standard'")
    w.write(":radiance (smul (smul (illuminant 'd65') %s) %f)" % (node_name, energy))

    w.goOut()
    w.write(")")
    return light_mat_n


def export_pointlight(exporter, light):
    w = exporter.w

    light_data = light.data
    w.write("; Light %s" % light.name)

    surf = 4*math.pi*math.pow(light_data.shadow_soft_size, 2)
    light_mat_n = write_emission(exporter, light, surf)

    w.write("(entity")
    w.goIn()

    w.write(":name '%s'" % light.name)
    w.write(":type 'sphere'")
    w.write(":radius %f" % light_data.shadow_soft_size)
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
    w.write(":width %f" % (light_data.size))
    w.write(":height %f" % (-ysize))
    w.write(":emission '%s'" % light_mat_n)
        
    inline_entity_matrix(exporter, light)

    w.goOut()
    w.write(")")


def export_sunlight(exporter, light):
    w = exporter.w
    w.write("; Light %s" % light.name)
    node_name = export_node(exporter, light.name, light.data.color, True, asLight=True)
    energy = light.data.energy

    w.write("(light")
    w.goIn()

    w.write(":type 'distant'")
    w.write(":direction [0, 0, -1]")
    w.write(":radiance (smul %s %f)" % (node_name, energy))
    inline_entity_matrix(exporter, light)

    w.goOut()
    w.write(")")


def export_light(exporter, light):
    if light.data.type == 'POINT':
        export_pointlight(exporter, light)  # Interpret as spherical area light
    elif light.data.type == 'SPOT':
        export_pointlight(exporter, light)  # TODO
    elif light.data.type == 'AREA':
        export_arealight(exporter, light)
    elif light.data.type == 'SUN':
        export_sunlight(exporter, light)
    else:
        print("PearRay does not support lights of type '%s'" % light.data.type)
