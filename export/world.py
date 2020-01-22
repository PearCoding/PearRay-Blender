from .spectral import write_spectral_color
from .texture import export_texture


def export_world(exporter, world):
    env_background_name = None
    color = world.color
    if color.r > 0 or color.g > 0 or color.b > 0:
        env_background_name = "'%s'" % write_spectral_color(
            exporter, '_blender_world_env_background_spec', color, asLight=True)

    env_radiance_name = None
    if world.pearray.split_background:
        #rad_type = world.pearray.radiance_type
        rad_color = world.pearray.radiance_color
        #rad_tex = world.pearray.radiance_color
    else:
        #rad_type = world.pearray.background_type
        rad_color = world.color
        #rad_tex = world.pearray.radiance_tex_slot

    if rad_color.r > 0 or rad_color.g > 0 or rad_color.b > 0:
        env_radiance_name = "'%s'" % write_spectral_color(
            exporter, '_blender_world_env_radiance_spec', rad_color, asLight=True)

    if env_background_name is not None:
        exporter.w.write("(light")
        exporter.w.goIn()
        exporter.w.write(":name '_blender_world_background_env'")
        exporter.w.write(":type 'env'")
        if env_radiance_name is not None:
            exporter.w.write(":radiance %s" % env_radiance_name)
            exporter.w.write(":background %s" % env_background_name)
        else:
            exporter.w.write(":radiance %s" % env_background_name)
        exporter.w.write(":factor %f" % world.pearray.radiance_factor)
        exporter.w.goOut()
        exporter.w.write(")")
