import collections
import bpy
import mathutils

from .entity import inline_entity_uniform
from .mesh import export_mesh_only, export_mesh_material_part

def export_particlesystem(exporter, parent, ps):
    w = exporter.w

    if not ps.settings.render_type == 'OBJECT':
        print("Particle system %s not supported! Only display of objects is supported!" % ps.name)
        return

    if not ps.settings.type == 'HAIR':
        print("Particle system %s not supported! Currently only particle systems of type 'HAIR' supported!" % ps.name)
        return

    disp_obj = ps.settings.dupli_object

    if not disp_obj.type in {'MESH', 'SURFACE'}:
        print("Particle system %s not supported! Invalid display object %s given!" % (ps.name, disp_obj.name))
        return

    mesh_name = export_mesh_only(exporter, disp_obj, False)

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
