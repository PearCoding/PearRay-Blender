import bpy
import re


from . import (
    properties_camera,
    properties_mesh,
    properties_output,
    properties_render,
    properties_world,
)

from ..core.render import PearRayRender

modules = (
    properties_camera,
    properties_mesh,
    properties_output,
    properties_render,
    properties_world,)


def get_panels():
    render_pt = re.compile('CYCLES_RENDER_PT_.*')
    freestyle_pt = re.compile('.*freestyle.*')

    cycles_render_panels = list(map(lambda v: v.__name__, filter(lambda v: render_pt.match(v.__name__), bpy.types.Panel.__subclasses__())))
    freestyle_panels = list(map(lambda v: v.__name__, filter(lambda v: freestyle_pt.match(v.__name__), bpy.types.Panel.__subclasses__())))

    exclude_panels = ['CYCLES_PT_integrator_presets', 'CYCLES_PT_sampling_presets',
                      *cycles_render_panels, *freestyle_panels,
                      'CYCLES_WORLD_PT_ambient_occlusion', 'CYCLES_WORLD_PT_mist', 'CYCLES_WORLD_PT_ray_visibility', 'CYCLES_WORLD_PT_settings_volume',
                      'CYCLES_WORLD_PT_volume', 'CYCLES_LIGHT_PT_nodes',
                      'RENDER_PT_stereoscopy', 'RENDER_PT_output', 'RENDER_PT_stamp']

    for panel in bpy.types.Panel.__subclasses__():
        if ('CYCLES' in getattr(panel, 'COMPAT_ENGINES', [])) and (panel.__name__ not in exclude_panels):
            yield panel


# Initialization
def register():
    for panel in get_panels():
        panel.COMPAT_ENGINES.add(PearRayRender.bl_idname)

    for m in modules:
        m.register()


def unregister():
    for m in reversed(modules):
        m.unregister()

    for panel in get_panels():
        if PearRayRender.bl_idname in panel.COMPAT_ENGINES:
            panel.COMPAT_ENGINES.remove(PearRayRender.bl_idname)
