import bpy
import mathutils
from math import degrees, radians


def is_renderable(scene, ob):
    return (ob.is_visible(scene) and not ob.hide_render)


def renderable_objects(scene):
    return [ob for ob in bpy.data.objects if is_renderable(scene, ob)]


def is_allowed_mesh(ob):
    return (not ob.type in {'META', 'FONT', 'ARMATURE', 'LATTICE', 'EMPTY', 'CAMERA', 'LAMP', 'SPEAKER'})


def make_unique_name(l, name):
    test_name = name
    i = 1
    while test_name in l:
        test_name = "%s_%i" % (name, i)
        i = i + 1
    return test_name


def write_ini(scene, filename):
    file = open(filename, "w")

    s = scene.pearray
    file.write("[renderer]\n")
    file.write("debug=%s\n" % s.debug_mode.lower())
    file.write("incremental=%i\n" % int(s.incremental))
    file.write("max=%i\n" % s.max_ray_depth)

    file.write("[threads]\n")
    threads = 0
    if scene.render.threads_mode == 'FIXED':
        threads = scene.render.threads
    file.write("count=%i\n" % threads)
    file.write("tile_x=%i\n" % scene.render.tile_x)
    file.write("tile_y=%i\n" % scene.render.tile_y)

    file.write("[pixelsampler]\n")
    file.write("mode=%s\n" % s.pixel_sampler_mode.lower())
    file.write("max=%i\n" % s.max_pixel_samples)

    file.write("[globalillumination]\n")
    file.write("diffuse_bounces=%i\n" % s.max_diffuse_bounces)
    file.write("light_samples=%i\n" % s.max_light_samples)
    file.write("bidirect=%i\n" % int(s.use_bidirect))

    file.write("[photon]\n")
    file.write("count=%i\n" % s.photon_count)
    file.write("radius=%f\n" % s.photon_gather_radius)
    file.write("max=%i\n" % s.photon_max_gather_count)
    file.write("max_diffuse_bounces=%i\n" % s.photon_max_diffuse_bounces)
    file.write("min_specular_bounces=%i\n" % s.photon_min_specular_bounces)
    file.write("gathering_mode=%s\n" % s.photon_gathering_mode.lower())
    file.write("squeeze=%f\n" % s.photon_squeeze)
    
    file.close()


def generate_scene(name, scene, filename):
    import datetime

    # PearRay uses a Y Up vector, but Blender uses a Z Up vector.
    # Here we change it :)
    M_WORLD = mathutils.Matrix([(-1,0,0,0), (0,0,-1,0), (0,1,0,0), (0,0,0,1)])
    CAM_UNIT_F = 0.1 # Why do I need this? -> TODO: PearRay should be implemented with millimeters in mind!
    LIGHT_POW_F = 10

    file = open(filename, "w")
    file.write("; generated by pearray exporter v0.2 with blender %s\n" % bpy.app.version_string)
    file.write("; at %s\n" % datetime.datetime.now())

    render = scene.render
    world = scene.world

    res_x = render.resolution_x * render.resolution_percentage * 0.01
    res_y = render.resolution_y * render.resolution_percentage * 0.01

    mesh_instances = []
    material_instances = []
    spec_instances = []
    MISSING_MAT = ''

    # Utils
    def write_spectral(spec_name, color):
        new_name = make_unique_name(spec_instances, spec_name)
        spec_instances.append(new_name)

        file.write("(spectrum\n")
        file.write(":name '%s'\n" % spec_name)
        file.write(":data (rgb %f %f %f)\n" % color[:])
        file.write(")\n")

        return new_name

    def inline_entity_matrix(obj):
        matrix = M_WORLD * obj.matrix_world
        trans, rot, scale = matrix.decompose()

        file.write(":position [%f,%f,%f]\n" % tuple(trans))
        file.write(":rotation [%f,%f,%f,%f]\n" % (rot.x, rot.y, rot.z, rot.w))
        file.write(":scale [%f,%f,%f]\n" % tuple(scale))

    # Exporters
    def export_scene():
        file.write(":name '%s'\n" % name)
        file.write(":renderWidth %i\n" % res_x)
        file.write(":renderHeight %i\n" % res_y)
        file.write(":camera '%s'\n" % scene.camera.name)
    
    def export_camera():
        camera = scene.camera
        matrix = M_WORLD * camera.matrix_world

        file.write("(entity\n")
        file.write(":name '%s'\n" % camera.name)
        file.write(":type 'camera'\n")
            
        aspectW = 1
        aspectH = 1
        if render.resolution_x > render.resolution_y:
            aspectW = render.resolution_x / render.resolution_y
        else:
            aspectH = render.resolution_y / render.resolution_x
        
        aspectW = aspectW * CAM_UNIT_F
        aspectH = aspectH * CAM_UNIT_F

        if camera.data.type == 'ORTHO':
            file.write(":projection 'orthogonal'\n" )
            file.write(":width %f\n" % (camera.data.ortho_scale * aspectW))
            file.write(":height %f\n" % (camera.data.ortho_scale * aspectH))
        else:
            sw = camera.data.sensor_width
            sh = camera.data.sensor_height
            if camera.data.sensor_fit == 'AUTO':
                if sw > sh:
                    sh = sw
                else:
                    sw = sh
            elif camera.data.sensor_fit == 'HORIZONTAL':
                sh = sw
            else:
                sw = sh
            
            file.write(":width %f\n" % (sw * aspectW))
            file.write(":height %f\n" % (sh * aspectH))

        file.write(":lookAt [%f,%f,%f]\n" % tuple([e for e in matrix.to_3x3().to_euler()]))
        file.write(":zoom %f\n" % camera.data.pearray.zoom)
        file.write(":fstop %f\n" % camera.data.pearray.fstop)
        file.write(":apertureRadius %f\n" % camera.data.pearray.apertureRadius)
        inline_entity_matrix(camera)
        file.write(")\n")

    def export_background():# TODO: Add texture support
        background_mat_n = make_unique_name(material_instances, '_blender_world_background')
        if world:
            if not world.use_sky_blend:
                file.write(":background '%s'\n" % background_mat_n)
                background_spec_n = write_spectral("%s_spec" % background_mat_n, world.horizon_color)
                file.write("(material\n")
                file.write(":name '%s'\n" % background_mat_n)
                file.write(":type 'light'\n")
                file.write(":emission '%s'\n" % background_spec_n)
                file.write(")\n")

    # Materials [TODO: More!]
    def inline_material_diffuse(material):
        file.write(":type 'diffuse'\n")
        file.write(":albedo '%s_diff_col'\n" % material.name)


    def inline_material_mirror(material):
        file.write(":type 'mirror'\n")
        file.write(":specularity '%s_spec_col'\n" % material.name)
        file.write(":index %f\n" % 1.55)#TODO


    def inline_material_glass(material):
        file.write(":type 'glass'\n")
        file.write(":specularity '%s_spec_col'\n" % material.name)
        file.write(":index %f\n" % material.raytrace_transparency.ior)


    def inline_material_oren_nayar(material):
        file.write(":type 'orennayar'\n")
        file.write(":albedo '%s_diff_col'\n" % material.name)
        file.write(":roughness %f\n" % material.roughness)


    def export_material(material):
        if not material or not material.use_raytrace:
            return
        
        if material.name in material_instances:
            return

        material_instances.append(material.name)

        write_spectral("%s_diff_col" % material.name, material.diffuse_intensity * material.diffuse_color)
        if material.emit > 0:
            write_spectral("%s_emit_col" % material.name, material.emit * material.diffuse_color)
        write_spectral("%s_spec_col" % material.name, material.specular_intensity * material.specular_color)

        file.write("(material\n")
        file.write(":name '%s'\n" % material.name)

        if material.use_shadeless or material.use_only_shadow:
            file.write(":shadeable false\n")

        if material.emit > 0:
            file.write(":emission '%s_emit_col'\n" % material.name)
        
        if material.diffuse_shader == 'OREN_NAYAR':
            inline_material_oren_nayar(material)
        else:
            #if material.alpha > 0:
            #    inline_material_glass(material)
            #elif material.raytrace_mirror.use:
            #    inline_material_mirror(material)
            #else:
                inline_material_diffuse(material)
        file.write(")\n")

    
    def export_default_materials():
        missing_mat = make_unique_name(material_instances, "missing_mat")
        material_instances.append(missing_mat)

        missing_spec_n = write_spectral("%s_spec" % missing_mat, (10,7,8))

        file.write("(material\n")
        file.write(":name '%s'\n" % missing_mat)
        file.write(":type 'diffuse'\n")
        file.write(":emission '%s'\n" % missing_spec_n)
        file.write(")\n")

        return missing_mat


    # Lights
    def export_pointlight(light):
        light_data = light.data
        file.write("; Light %s\n" % light.name)
        color = tuple([c * light_data.energy * LIGHT_POW_F for c in light_data.color])
        light_spec_n = write_spectral(light.name + "_spec", color)

        light_mat_n = make_unique_name(material_instances, light.name + "_mat")
        material_instances.append(light_mat_n)

        file.write("(material\n")
        file.write(":name '%s'\n" % light_mat_n)
        file.write(":type 'diffuse'\n")
        file.write(":emission '%s'\n" % light_spec_n)
        file.write(")\n")

        file.write("(entity\n")
        file.write(":name '%s'\n" % light.name)
        file.write(":type 'sphere'\n")
        file.write(":radius 0.01\n")# Really?
        inline_entity_matrix(light)
        file.write(")\n")
    
    def export_arealight(light):
        light_data = light.data
        file.write("; Light %s\n" % light.name)
        color = tuple([c * light_data.energy * LIGHT_POW_F for c in light_data.color])
        light_spec_n = write_spectral(light.name + "_spec", color)

        light_mat_n = make_unique_name(material_instances, light.name + "_mat")
        material_instances.append(light_mat_n)

        file.write("(material\n")
        file.write(":name '%s'\n" % light_mat_n)
        file.write(":type 'diffuse'\n")
        file.write(":emission '%s'\n" % light_spec_n)
        file.write(")\n")

        file.write("(entity\n")
        file.write(":name '%s'\n" % light.name)
        file.write(":type 'plane'\n")
        file.write(":xAxis %f\n" % light_data.size)
        file.write(":yAxis %f\n" % light_data.size_y)
        inline_entity_matrix(light)
        file.write(")\n")

    def export_light(light):
        if light.data.type == 'POINT':
            export_pointlight(light)# Interpret as spherical area light
        elif light.data.type == 'AREA':
            export_arealight(light)
        else:
            print("PearRay does not support lights of type '%s'" % light.data.type)

    # Meshes
    def export_trimesh(name, mesh):
        faces = mesh.tessfaces[:]
        faces_verts = [f.vertices[:] for f in faces]
        faces_norms = [f.normal[:] for f in faces]
        faces_colors = mesh.tessface_vertex_colors[:]
        faces_uv = mesh.tessface_uv_textures[:]

        verts = mesh.vertices
        verts_normals = [v.normal[:] for v in verts]

        #if len(faces_uv) > 0:
        #    if mesh.uv_textures.active and faces_uv.active.data:
        #        uv_layer = faces_uv.active.data
        #else:
        #    uv_layer = None

        file.write("(mesh\n")
        file.write(":name '%s'\n" % name)
        file.write(":type 'triangles'\n")

        file.write("(attribute\n")
        file.write(":type 'p'")
        for v in verts:
            file.write(", [%f, %f, %f]" % v.co[:])
        file.write("\n)\n")

        if len(verts_normals) > 0:
            file.write("(attribute\n")
            file.write(":type 'n'")
            for n in verts_normals:
                file.write(", [%f, %f, %f]" % n)
            file.write("\n)\n")

        # TODO: Add UVs, Colors etc.

        file.write("(faces ")
        for fi, f in enumerate(faces):
            fv = faces_verts[fi]
            if len(fv) == 4:# Cube
                indices = (0, 1, 2), (0, 2, 3)
            else:# Triangle
                indices = ((0, 1, 2),)
            
            for i1, i2, i3 in indices:
                file.write(", %i, %i, %i" % (fv[i1], fv[i2], fv[i3]))
        file.write("\n)\n")

        file.write(")\n")


    def export_mesh(obj):
        # Check if in instance list
        if not obj.data.name in mesh_instances:
            try:
                mesh = obj.to_mesh(scene, True, 'RENDER', calc_tessface=True)
            except:
                print("Couldn't export %s as mesh" % obj.name)
                return
            export_trimesh(obj.data.name, mesh)
            bpy.data.meshes.remove(mesh)

        mesh_instances.append(obj.data.name)

        file.write("(entity\n")
        file.write(":name '%s'\n" % obj.name)
        file.write(":type 'mesh'\n")

        if len(obj.data.materials) >= 1 and obj.data.materials[0]:
            file.write(":material '%s'\n" % obj.data.materials[0].name)
        else:
            file.write(":material '%s'\n" % MISSING_MAT)
            print("Mesh %s has no material!" % obj.name)
           
        file.write(":mesh '%s'\n" % obj.data.name)
        inline_entity_matrix(obj)
        file.write(")\n")

    # Block
    objs = renderable_objects(scene)

    file.write("(scene\n")
    export_scene()
    file.write("; Default Materials\n")
    MISSING_MAT = export_default_materials()
    file.write("; Camera\n")
    export_camera()
    file.write("; Background\n")
    export_background()
    file.write("; Lights\n")
    for light in objs:
        if light.type == 'LAMP':
            export_light(light)
    file.write("; Meshes\n")
    for obj in objs:
        if is_allowed_mesh(obj):
            export_mesh(obj)
    file.write("; Materials\n")
    for obj in objs:
        if is_allowed_mesh(obj):
            for m in obj.data.materials:
                export_material(m)
    export_material(None)
    file.write(")\n")
    file.close()