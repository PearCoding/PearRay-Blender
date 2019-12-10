from .spectral import write_spectral_color
from .texture import export_texture

def export_world(exporter, world):
    background_rad_n = None
    if getattr(world.pearray, "background_type") == 'COLOR':
        color = getattr(world, "horizon_color")
        if color.r > 0 or color.g > 0 or color.b > 0:
            background_rad_n = "'%s'" % write_spectral_color(exporter, '_blender_world_background_spec', color)
    else:
        if len(world.texture_slots) <= 0:
            return

        tex_slot = getattr(world.pearray, "background_tex_slot")
        if tex_slot >= len(world.texture_slots):
            return

        background_rad_n = "(texture '%s')" % export_texture(
            exporter, world.texture_slots[tex_slot].texture)

    if background_rad_n is not None:
        exporter.w.write("(light")
        exporter.w.goIn()
        exporter.w.write(":name '_blender_world_background_env'")
        exporter.w.write(":type 'env'")
        exporter.w.write(":radiance %s" % background_rad_n)
        exporter.w.goOut()
        exporter.w.write(")")