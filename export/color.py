from .spectral import write_spectral_color, write_spectral_temp
from .texture import export_texture


def export_color(exporter, material, type, required,
    factor=1, asLight=False):
    name = "%s_%s" % (material.name, type)

    attr_col = type
    attr_temp = "%s_temp" % type
    attr_temp_type = "%s_temp_type" % type
    attr_temp_factor = "%s_temp_factor" % type
    attr_type = "%s_type" % type
    attr_tex_slot = "%s_tex_slot" % type

    sub_mat = material
    if not hasattr(material, attr_col):
        sub_mat = material.pearray

    color_type = getattr(material.pearray, attr_type)
    if color_type == 'COLOR' or not hasattr(material.pearray, attr_type):
        color = getattr(sub_mat, attr_col)
        if required or color.r > 0 or color.g > 0 or color.b > 0:
            return "'%s'" % write_spectral_color(exporter, name,
                                                 factor * color,
                                                 asLight=asLight)
    elif color_type == 'TEX' and hasattr(material.pearray, attr_tex_slot):
        if len(material.texture_slots) <= 0:
            if required:
                return "''"
            else:
                return ""

        tex_slot = getattr(material.pearray, attr_tex_slot)
        if tex_slot >= len(material.texture_slots):
            tex_slot = 0
        return "(texture '%s')" % export_texture(
            exporter, material.texture_slots[tex_slot].texture)
    elif hasattr(material.pearray, attr_temp):
        temp = getattr(material.pearray, attr_temp)
        if required or temp > 0:
            return "'%s'" % write_spectral_temp(
                exporter, name, temp, getattr(material.pearray,
                                              attr_temp_type),
                factor * getattr(material.pearray, attr_temp_factor))

    if required:
        return "''"
    else:
        return ""
