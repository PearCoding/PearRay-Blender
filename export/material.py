from .spectral import write_spectral_color, write_spectral_temp
from .texture import export_texture


def export_material(exporter, material):
    if not material:
        return

    if material.name in exporter.instances['MATERIAL']:
        return

    exporter.register_unique_name('MATERIAL', material.name)

    # TODO


def export_default_materials(exporter):
    exporter.MISSING_MAT = exporter.register_unique_name(
        'MATERIAL', "_missing_mat")

    missing_spec_n = write_spectral_color(
        exporter, "%s_spec" % exporter.MISSING_MAT, (10, 7, 8))

    exporter.w.write("(material")
    exporter.w.goIn()

    exporter.w.write(":name '%s'" % exporter.MISSING_MAT)
    exporter.w.write(":type 'diffuse'")
    exporter.w.write(":albedo '%s'" % missing_spec_n)

    exporter.w.goOut()
    exporter.w.write(")")
