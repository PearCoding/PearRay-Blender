import bpy
from .camera import export_camera
from .curve import export_curve
from .light import export_light
from .material import export_default_materials, export_material
from .mesh import export_mesh
from .particlesystem import export_particlesystem
from .primitive import export_primitive
from .spectral import write_spectral_color
from .settings import export_settings
from .world import export_world


def renderable_instances(dpsgraph):
    for inst in dpsgraph.object_instances:
        if inst.show_self:
            yield inst


def is_allowed_mesh(inst):
    if inst.object.type == 'MESH':
        return not inst.object.data.pearray.is_primitive
    else:
        return (inst.object.type in {'MESH', 'SURFACE'})


def is_allowed_curve(inst):
    return (inst.object.type in {'CURVE', 'FONT'})


def write_scene(exporter, pr):
    w = exporter.w
    scene = exporter.scene

    res_x = exporter.render.resolution_x * \
        exporter.render.resolution_percentage * 0.01
    res_y = exporter.render.resolution_y * \
        exporter.render.resolution_percentage * 0.01

    # Exporters
    def export_scene():
        w.write(":name '_from_blender'")
        w.write(":render_width %i" % res_x)
        w.write(":render_height %i" % res_y)
        w.write(":camera '%s'" % scene.camera.name)

    def export_outputs():
        rl = scene.view_layers[0]
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
                else:
                    w.write(":color 'srgb'")
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

    # Extract information
    has_light = False
    has_curve = False
    has_mesh = False
    for obj in renderable_instances(exporter.depsgraph):
        if obj.object.type == 'LIGHT':
            has_light = True
        elif obj.object.type == 'MESH':
            has_mesh = True
        elif is_allowed_curve(obj):
            has_curve = True

    # Write entries
    w.write("(scene")
    w.goIn()

    export_scene()
    w.write("; Settings")
    export_settings(exporter, pr, scene)
    w.write("; Outputs")
    export_outputs()
    w.write("; Default Materials")
    export_default_materials(exporter)
    w.write("; Camera")
    export_camera(exporter, scene.camera)
    if exporter.world:
        w.write("; Background")
        export_world(exporter, exporter.world)
    
    if has_light:
        w.write("; Lights")
        for light in renderable_instances(exporter.depsgraph):
            if light.object.type == 'LIGHT':
                export_light(
                    exporter, light.instance_object if light.is_instance else light.object)

    if has_curve:
        w.write("; Curves")
        for inst in renderable_instances(exporter.depsgraph):
            if is_allowed_curve(inst):
                export_curve(
                    exporter, inst.instance_object if inst.is_instance else inst.object)

    # w.write("; Particle Systems")
    # TODO
    
    if len(bpy.data.materials) > 0:
        w.write("; Materials")
        for m in bpy.data.materials:
            export_material(exporter, m)

    if has_mesh:
        w.write("; Primitives")
        for inst in renderable_instances(exporter.depsgraph):
            if inst.object.type == 'MESH':
                if inst.object.data.pearray.is_primitive:
                    export_primitive(
                        exporter, inst.instance_object if inst.is_instance else inst.object)

        # Make meshes last as they are often the largest entries
        w.write("; Meshes")
        for inst in renderable_instances(exporter.depsgraph):
            if is_allowed_mesh(inst):
                export_mesh(exporter, inst)

    w.goOut()
    w.write(")")
