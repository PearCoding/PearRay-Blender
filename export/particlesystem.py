import collections
import bpy
import mathutils

from .entity import inline_entity_uniform
from .mesh import export_mesh_only, export_mesh_material_part


def export_particlesystem_object(exporter, parent, ps):
    w = exporter.w

    if not ps.settings.type == 'HAIR':
        print("Particle system %s not supported! Currently only particle systems of type 'HAIR' supported!" % ps.name)
        return

    disp_obj = ps.settings.dupli_object

    if not disp_obj.type in {'MESH', 'SURFACE'}:
        print("Particle system %s not supported! Invalid display object %s given!" % (ps.name, disp_obj.name))
        return

    mesh_name = export_mesh_only(exporter, disp_obj)

    if not mesh_name:
        return

    parent_m = mathutils.Matrix.Identity(4)
    if ps.parent:
        parent_m = ps.parent.matrix_world.inverted()
    elif not ps.is_global_hair:
        parent_m = parent.matrix_world

    ident = mathutils.Matrix.Identity(4)

    sf = ps.settings.hair_length
    oaf = mathutils.Vector(ps.settings.object_align_factor)
    if not oaf.length_squared == 0:
        sf *= oaf.length

    counter = 0
    for particle in ps.particles:
        co = parent_m*particle.hair_keys[0].co

        s = particle.size*sf
        if s <= 0:
            continue

        w.write("(entity")
        w.goIn()

        w.write(":name '%s_part_%d'" % (ps.name, counter))
        w.write(":type 'mesh'")

        export_mesh_material_part(exporter, disp_obj)

        w.write(":mesh '%s'" % mesh_name)
        inline_entity_uniform(exporter, co, particle.rotation, s, ident)

        w.goOut()
        w.write(")")
        counter += 1


def export_particlesystem_path(exporter, parent, ps):
    w = exporter.w

    if not ps.settings.type == 'HAIR':
        print("Particle system %s not supported! Currently only particle systems of type 'HAIR' supported!" % ps.name)
        return

    # TODO: Get the real material
    mat_name = parent.data.materials[0].name

    parent_m = mathutils.Matrix.Identity(4)
    if ps.parent:
        parent_m = ps.parent.matrix_world.inverted()
    elif not ps.is_global_hair:
        parent_m = parent.matrix_world

    ident = mathutils.Matrix.Identity(4)

    # TODO Set size reasonable...
    sf = ps.settings.particle_size*ps.settings.hair_length
    oaf = mathutils.Vector(ps.settings.object_align_factor)
    if not oaf.length_squared == 0:
        sf *= oaf.length

    particle_count = len(ps.particles)*ps.settings.child_nbr
    degree = ps.settings.hair_step
    for i in range(particle_count):
        w.write("(entity")
        w.goIn()

        w.write(":name '%s_hair_%d'" % (ps.name, i))
        w.write(":type 'curve'")
        w.write(":material '%s'" % mat_name)
        w.write(":degree %i" % degree)

        w.write(":points [%s]" % ",".join(",".join(str(f) for f in parent_m*ps.co_hair(parent, i, k)) for k in range(degree+1)))
        w.write(":width [%f, %f]" % (sf,sf))

        w.goOut()
        w.write(")")


def export_particlesystem(exporter, parent, ps):
    if ps.settings.render_type == 'OBJECT':
        export_particlesystem_object(exporter, parent, ps)
    elif ps.settings.render_type == 'PATH':
        export_particlesystem_path(exporter, parent, ps)
    elif ps.settings.render_type == 'NONE':
        return
    else:
        print("Particle system %s not supported! Only display of objects is supported!" % ps.name)
        return
