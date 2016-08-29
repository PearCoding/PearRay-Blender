from .spectral import write_spectral as write_spectral


def inline_material_diffuse(exporter, material):
    exporter.w.write(":type 'diffuse'")
    exporter.w.write(":albedo '%s_diff_col'" % material.name)


def inline_material_mirror(exporter, material):
    exporter.w.write(":type 'mirror'")
    exporter.w.write(":specularity '%s_spec_col'" % material.name)
    exporter.w.write(":index %f" % 1.55)#TODO


def inline_material_glass(exporter, material):
    exporter.w.write(":type 'glass'")
    exporter.w.write(":specularity '%s_spec_col'" % material.name)
    exporter.w.write(":index %f" % material.raytrace_transparency.ior)


def inline_material_oren_nayar(exporter, material):
    exporter.w.write(":type 'orennayar'")
    exporter.w.write(":albedo '%s_diff_col''" % material.name)
    exporter.w.write(":roughness %f" % material.roughness)


def export_material(exporter, material):
    if not material or not material.use_raytrace:
        return
    
    if material.name in exporter.instances['MATERIAL']:
        return

    exporter.register_unique_name('MATERIAL', material.name)

    write_spectral(exporter, "%s_diff_col" % material.name, material.diffuse_intensity * material.diffuse_color)
    if material.emit > 0:
        write_spectral(exporter, "%s_emit_col" % material.name, material.emit * material.diffuse_color)
    write_spectral(exporter, "%s_spec_col" % material.name, material.specular_intensity * material.specular_color)

    exporter.w.write("(material")
    exporter.w.goIn()

    exporter.w.write(":name '%s'" % material.name)

    if material.use_shadeless or material.use_only_shadow:
        exporter.w.write(":shadeable false")

    if material.emit > 0:
        exporter.w.write(":emission '%s_emit_col'" % material.name)
    
    if material.diffuse_shader == 'OREN_NAYAR':
        inline_material_oren_nayar(exporter, material)
    else:
        #if material.alpha > 0:
        #    inline_material_glass(exporter, material)
        #elif material.raytrace_mirror.use:
        #    inline_material_mirror(exporter, material)
        #else:
            inline_material_diffuse(exporter, material)
    
    exporter.w.goOut()
    exporter.w.write(")")


def export_default_materials(exporter):
    missing_mat = exporter.register_unique_name('MATERIAL', "missing_mat")

    missing_spec_n = write_spectral(exporter, "%s_spec" % missing_mat, (10,7,8))

    exporter.w.write("(material")
    exporter.w.goIn()

    exporter.w.write(":name '%s'" % missing_mat)
    exporter.w.write(":type 'diffuse'")
    exporter.w.write(":emission '%s'" % missing_spec_n)

    exporter.w.goOut()
    exporter.w.write(")")

    return missing_mat