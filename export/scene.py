import bpy
from .camera import export_camera as export_camera
from .light import export_light as export_light
from .material import export_default_materials as export_default_materials
from .material import export_material as export_material 
from .mesh import export_mesh as export_mesh
from .spectral import write_spectral_color


def is_renderable(scene, ob):
    return (ob.is_visible(scene) and not ob.hide_render)


def renderable_objects(scene):
    return [ob for ob in bpy.data.objects if is_renderable(scene, ob)]


def is_allowed_mesh(ob):
    return (not ob.type in {'META', 'FONT', 'ARMATURE', 'LATTICE', 'EMPTY', 'CAMERA', 'LAMP', 'SPEAKER'})


def write_scene(exporter):
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
    
    def export_background():# TODO: Add texture support
        background_mat_n = exporter.register_unique_name('MATERIAL', '_blender_world_background')

        if exporter.world:
            color = exporter.world.horizon_color
            if color.r > 0 or color.g > 0 or color.b > 0:
                w.write(":background '%s'" % background_mat_n)
                background_spec_n = write_spectral_color(exporter, "%s_spec" % background_mat_n, color)
                w.write("(material")
                w.goIn()

                w.write(":name '%s'" % background_mat_n)
                w.write(":type 'light'")
                w.write(":emission '%s'" % background_spec_n)

                w.goOut()
                w.write(")")

    # Block
    objs = renderable_objects(scene)

    w.write("(scene")
    w.goIn()

    export_scene()
    w.write("; Default Materials")
    export_default_materials(exporter)
    w.write("; Camera")
    export_camera(exporter, scene.camera)
    w.write("; Background")
    export_background()
    w.write("; Lights")
    for light in objs:
        if light.type == 'LAMP':
            export_light(exporter, light)
    w.write("; Meshes")
    for obj in objs:
        if is_allowed_mesh(obj):
            export_mesh(exporter, obj)
    w.write("; Materials")
    for obj in objs:
        if is_allowed_mesh(obj):
            for m in obj.data.materials:
                export_material(exporter, m)

    w.goOut()
    w.write(")")