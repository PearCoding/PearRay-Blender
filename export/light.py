from .entity import inline_entity_matrix as inline_entity_matrix
from .spectral import write_spectral as write_spectral


def export_pointlight(exporter, light):
    w = exporter.w

    light_data = light.data
    w.write("; Light %s" % light.name)

    color = tuple([c * light_data.energy * exporter.LIGHT_POW_F for c in light_data.color])
    light_spec_n = write_spectral(exporter, light.name + "_spec", color)

    light_mat_n = exporter.make_unique_name(exporter.material_instances, light.name + "_mat")
    exporter.material_instances.append(light_mat_n)

    w.write("(material")
    w.goIn()

    w.write(":name '%s'" % light_mat_n)
    w.write(":type 'diffuse'")
    w.write(":emission '%s'" % light_spec_n)

    w.goOut()
    w.write(")")

    w.write("(entity")
    w.goIn()

    w.write(":name '%s'" % light.name)
    w.write(":type 'sphere'")
    w.write(":radius 0.01")# Really?
    inline_entity_matrix(exporter, light)

    w.goOut()
    w.write(")")


def export_arealight(exporter, light):
    w = exporter.w
    light_data = light.data
    w.write("; Light %s" % light.name)

    color = tuple([c * light_data.energy * exporter.LIGHT_POW_F for c in light_data.color])
    light_spec_n = write_spectral(light.name + "_spec", color)

    light_mat_n = exporter.make_unique_name(exporter.material_instances, light.name + "_mat")
    exporter.material_instances.append(light_mat_n)

    w.write("(material")
    w.goIn()

    w.write(":name '%s'" % light_mat_n)
    w.write(":type 'diffuse'")
    w.write(":emission '%s'" % light_spec_n)

    w.goOut()
    w.write(")")

    w.write("(entity")
    w.goIn()

    w.write(":name '%s'" % light.name)
    w.write(":type 'plane'")
    w.write(":xAxis %f" % light_data.size)
    w.write(":yAxis %f" % light_data.size_y)
    inline_entity_matrix(exporter, light)

    w.goOut()
    w.write(")")


def export_light(exporter, light):
    if light.data.type == 'POINT':
        export_pointlight(exporter, light)# Interpret as spherical area light
    elif light.data.type == 'AREA':
        export_arealight(exporter, light)
    else:
        print("PearRay does not support lights of type '%s'" % light.data.type)