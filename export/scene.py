import bpy
from .camera import export_camera
from .light import export_light
from .material import export_default_materials, export_material
from .mesh import export_mesh
from .particlesystem import export_particlesystem
from .spectral import write_spectral_color
from .settings import export_settings
from .world import export_world


def is_renderable(scene, ob):
    return (not ob.hide_render) and (ob.layers[scene.active_layer])


def renderable_objects(scene):
    return [ob for ob in bpy.data.objects if is_renderable(scene, ob)]


def is_allowed_mesh(ob):
    return (ob.type in {'MESH', 'SURFACE'})


def write_scene(exporter, pr):
    w = exporter.w
    scene = exporter.scene

    res_x = exporter.render.resolution_x * exporter.render.resolution_percentage * 0.01
    res_y = exporter.render.resolution_y * exporter.render.resolution_percentage * 0.01

    # Exporters
    def export_scene():
        w.write(":name '_from_blender'")
        w.write(":renderWidth %i" % res_x)
        w.write(":renderHeight %i" % res_y)
        w.write(":camera '%s'" % scene.camera.name)


    def export_outputs():
        rl = scene.render.layers.active
        rl2 = scene.pearray_layer

        def start_output(str):
            if rl2.separate_files:
                w.write("(output")
                w.goIn()
                w.write(":name '%s'" % str)
            w.write("(channel")
            w.goIn()

        def end_output():
            w.goOut()
            w.write(")")
            if rl2.separate_files:
                w.goOut()
                w.write(")")

        def raw_output(str, lpe):
            start_output(str)
            w.write(":type '%s'" % str)
            if lpe:
                w.write(":lpe '%s'" % lpe)
            end_output()

        def export_channel(type, lpe=None):
            if type == 'SPECTRAL':
                start_output('image')
                w.write(":type 'color'")
                if scene.pearray.color_format == 'XYZ':
                    w.write(":color 'xyz'")
                    w.write(":gamma 'none'")
                elif scene.pearray.color_format == 'SRGB':
                    w.write(":color 'rgb'")
                    w.write(":gamma 'srgb'")
                else:
                    w.write(":color 'rgb'")
                    w.write(":gamma 'none'")
                w.write(":mapper 'none'")
                if lpe:
                    w.write(":lpe '%s'" % lpe)
                end_output()
            elif type == 'POSITION':
                raw_output('p', lpe)
            elif type == 'NORMAL':
                raw_output('n', lpe)
            elif type == 'NORMALG':
                raw_output('ng', lpe)
            elif type == 'TANGENT':
                raw_output('nx', lpe)
            elif type == 'BITANGENT':
                raw_output('ny', lpe)
            elif type == 'VIEW':
                raw_output('view', lpe)
            elif type == 'UVW':
                raw_output('uvw', lpe)
            elif type == 'DPDT':
                raw_output('dpdt', lpe)
            elif type == 'ENTITY_ID':
                raw_output('entity_id', lpe)
            elif type == 'MATERIAL_ID':
                raw_output('material_id', lpe)
            elif type == 'EMISSION_ID':
                raw_output('emission_id', lpe)
            elif type == 'DISPLACE_ID':
                raw_output('displace_id', lpe)
            elif type == 'DEPTH':
                raw_output('depth', lpe)
            elif type == 'TIME':
                raw_output('t', lpe)
            elif type == 'SAMPLES':
                raw_output('s', lpe)
            elif type == 'FEEDBACK':
                raw_output('feedback', lpe)

        # Actual function body
        if not rl2.separate_files:
            w.write("(output")
            w.goIn()
            w.write(":name 'image'")

        if rl.use_pass_combined:
            export_channel('SPECTRAL')

        if rl.use_pass_z:
            export_channel('DEPTH')
        if rl.use_pass_normal:
            export_channel('NORMAL')
        if rl.use_pass_vector:
            export_channel('DPDT')
        if rl.use_pass_uv:
            export_channel('UVW')
        if rl.use_pass_object_index:
            export_channel('ENTITY_INDEX')
        if rl.use_pass_material_index:
            export_channel('MATERIAL_INDEX')
        if rl2.aov_emission_index:
            export_channel('EMISSION_INDEX')
        if rl2.aov_displace_index:
            export_channel('DISPLACE_INDEX')
        if rl2.aov_ng:
            export_channel('NORMALG')
        if rl2.aov_nx:
            export_channel('TANGENT')
        if rl2.aov_ny:
            export_channel('BITANGENT')
        if rl2.aov_p:
            export_channel('POSITION')
        if rl2.aov_t:
            export_channel('TIME')
        if rl2.aov_samples:
            export_channel('SAMPLES')
        if rl2.aov_feedback:
            export_channel('FEEDBACK')

        for lpe in rl2.lpes:
            export_channel(lpe.channel, lpe.expression)

        if not rl2.separate_files:
            w.goOut()
            w.write(")")

        if rl2.raw_spectral:
            w.write("(output_spectral")
            w.goIn()
            w.write(":name 'spectral'")
            w.goOut()
            w.write(")")

    # Block
    objs = renderable_objects(scene)

    w.write("(scene")
    w.goIn()

    export_scene()
    w.write("; Settings")
    export_settings(exporter, pr,scene)
    w.write("; Outputs")
    export_outputs()
    w.write("; Default Materials")
    export_default_materials(exporter)
    w.write("; Camera")
    export_camera(exporter, scene.camera)
    if(exporter.world):
        w.write("; Background")
        export_world(exporter, exporter.world)
    w.write("; Lights")
    for light in objs:
        if light.type == 'LAMP':
            export_light(exporter, light)
    w.write("; Meshes")
    for obj in objs:
        if is_allowed_mesh(obj):
            export_mesh(exporter, obj)
    w.write("; Particle Systems")
    for obj in objs:
        for ps in obj.particle_systems:
            if ps == obj.particle_systems.active:
                allowed = True
                for mod in obj.modifiers:
                    if mod.type == 'PARTICLE_SYSTEM' and mod.show_render is False:
                        allowed = False

                if allowed:
                    ps.set_resolution(scene, obj, 'RENDER')
                    export_particlesystem(exporter, obj, ps)
                    ps.set_resolution(scene, obj, 'PREVIEW')
    w.write("; Materials")
    # Ignore hide_render
    for obj in bpy.data.objects:
        if is_allowed_mesh(obj):
            for m in obj.data.materials:
                export_material(exporter, m)

    w.goOut()
    w.write(")")