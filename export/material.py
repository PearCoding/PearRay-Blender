from .spectral import write_spectral_color, write_spectral_temp


def inline_material_defaults(exporter, material):
    exporter.w.write(":name '%s'" % material.name)

    if not material.pearray.cast_shadows:
        #exporter.w.write(":castShadows false")
        pass

    if not material.pearray.cast_self_shadows:
        exporter.w.write(":selfShadow false")

    if not material.pearray.is_shadeable:
        exporter.w.write(":shadeable false")

    if not material.pearray.is_camera_visible:
        exporter.w.write(":cameraVisible false")


def export_material_diffuse(exporter, material):
    diff_name = export_color(exporter, material, 'diffuse', True)
    em_name = export_color(exporter, material, 'emission', False)

    exporter.w.write("(material")
    exporter.w.goIn()

    inline_material_defaults(exporter, material)

    if em_name:
        exporter.w.write(":emission '%s'" % em_name)
    
    exporter.w.write(":type 'diffuse'")
    exporter.w.write(":albedo '%s'" % diff_name)
    
    exporter.w.goOut()
    exporter.w.write(")")


def export_material_orennayar(exporter, material):
    diff_name = export_color(exporter, material, 'diffuse', True)
    em_name = export_color(exporter, material, 'emission', False)

    exporter.w.write("(material")
    exporter.w.goIn()

    inline_material_defaults(exporter, material)

    if em_name:
        exporter.w.write(":emission '%s'" % em_name)
    
    exporter.w.write(":type 'orennayar'")
    exporter.w.write(":albedo '%s'" % diff_name)
    exporter.w.write(":roughness '%f'" % material.roughness)
    
    exporter.w.goOut()
    exporter.w.write(")")


def export_material_ward(exporter, material):
    diff_name = export_color(exporter, material, 'diffuse', True)
    spec_name = export_color(exporter, material, 'specular', True)
    em_name = export_color(exporter, material, 'emission', False)

    exporter.w.write("(material")
    exporter.w.goIn()

    inline_material_defaults(exporter, material)

    if em_name:
        exporter.w.write(":emission '%s'" % em_name)
    
    exporter.w.write(":type 'ward'")
    exporter.w.write(":albedo '%s'" % diff_name)
    exporter.w.write(":specularity '%s'" % spec_name)
    exporter.w.write(":roughnessX '%f'" % material.pearray.roughnessX)
    exporter.w.write(":roughnessY '%f'" % material.pearray.roughnessY)
    
    exporter.w.goOut()
    exporter.w.write(")")


def export_material_glass(exporter, material):
    spec_name = export_color(exporter, material, 'specular', True)
    em_name = export_color(exporter, material, 'emission', False)

    exporter.w.write("(material")
    exporter.w.goIn()

    inline_material_defaults(exporter, material)

    if em_name:
        exporter.w.write(":emission '%s'" % em_name)
    
    exporter.w.write(":type 'glass'")
    exporter.w.write(":specularity '%s'" % spec_name)
    exporter.w.write(":index '%f'" % material.specular_ior)
    
    exporter.w.goOut()
    exporter.w.write(")")


def export_material_mirror(exporter, material):
    spec_name = export_color(exporter, material, 'specular', True)
    em_name = export_color(exporter, material, 'emission', False)

    exporter.w.write("(material")
    exporter.w.goIn()

    inline_material_defaults(exporter, material)

    if em_name:
        exporter.w.write(":emission '%s'" % em_name)
    
    exporter.w.write(":type 'mirror'")
    exporter.w.write(":specularity '%s'" % spec_name)
    exporter.w.write(":index '%f'" % material.specular_ior)
    
    exporter.w.goOut()
    exporter.w.write(")")


def export_material_grid(exporter, material):
    exporter.w.write("(material")
    exporter.w.goIn()

    inline_material_defaults(exporter, material)
    
    exporter.w.write(":type 'grid'")
    exporter.w.write(":first '%s'" % material.pearray.grid_first_material)
    exporter.w.write(":second '%s'" % material.pearray.grid_second_material)
    exporter.w.write(":gridCount '%i'" % material.pearray.grid_count)
    exporter.w.write(":tileUV '%s'" % material.pearray.grid_tile_uv)
    
    exporter.w.goOut()
    exporter.w.write(")")


def export_color(exporter, material, type, required):
    name = "%s_%s_color" % (material.name, type)

    attr_col = "%s_color" % type
    attr_temp = "%s_color_temp" % type
    attr_type = "%s_color_type" % type

    sub_mat = material
    if not hasattr(material, attr_col):
        sub_mat = material.pearray

    if getattr(material.pearray, attr_type) == 'COLOR':
        color = getattr(sub_mat, attr_col)
        if required or color.r > 0 or color.g > 0 or color.b > 0:
            return write_spectral_color(exporter, name, color)
    else:
        temp = getattr(material.pearray, attr_temp)
        if required or temp > 0:
            return write_spectral_temp(exporter, name, temp)

    return ""


def export_material(exporter, material):
    if not material or not material.use_raytrace:
        return
    
    if material.name in exporter.instances['MATERIAL']:
        return

    exporter.register_unique_name('MATERIAL', material.name)

    brdf = material.pearray.brdf

    if brdf == 'DIFFUSE':
        export_material_diffuse(exporter, material)
    elif brdf == 'ORENNAYAR':
        export_material_orennayar(exporter, material)
    elif brdf == 'WARD':
        export_material_ward(exporter, material)
    elif brdf == 'GLASS':
        export_material_glass(exporter, material)
    elif brdf == 'MIRROR':
        export_material_mirror(exporter, material)
    elif brdf == 'GRID':
        export_material_grid(exporter, material)
    else:
        print("UNKNOWN BRDF %s\n" % brdf)
   

def export_default_materials(exporter):
    exporter.MISSING_MAT = exporter.register_unique_name('MATERIAL', "_missing_mat")
    exporter.DEBUG_MAT = exporter.register_unique_name('MATERIAL', "_debug_mat")

    missing_spec_n = write_spectral_color(exporter, "%s_spec" % exporter.MISSING_MAT, (10,7,8))
    debug_spec_n = write_spectral_color(exporter, "%s_spec" % exporter.DEBUG_MAT, (1,0,0))

    exporter.w.write("(material")
    exporter.w.goIn()

    exporter.w.write(":name '%s'" % exporter.MISSING_MAT)
    exporter.w.write(":type 'diffuse'")
    exporter.w.write(":emission '%s'" % missing_spec_n)

    exporter.w.goOut()
    exporter.w.write(")")

    exporter.w.write("(material")
    exporter.w.goIn()

    exporter.w.write(":name '%s'" % exporter.DEBUG_MAT)
    exporter.w.write(":type 'debugBoundingBox'")
    exporter.w.write(":color '%s'" % debug_spec_n)
    exporter.w.write(":density 0.3")

    exporter.w.goOut()
    exporter.w.write(")")
