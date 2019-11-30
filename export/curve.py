import collections
import bpy
import mathutils
from .entity import inline_entity_matrix


def export_curve_spline(exporter, obj, index, start):
    w = exporter.w

    spline = obj.data.splines[index]

    wfactor = 2*(obj.data.bevel_depth + obj.data.extrude)
    if wfactor <= 0:
        return

    w.write("(entity")
    w.goIn()

    w.write(":name '%s_%i_%i'" % (obj.name, index, start))
    w.write(":type 'curve'")
    w.write(":material '%s'" % obj.data.materials[spline.material_index].name)

    points = [spline.bezier_points[start].co, spline.bezier_points[start].handle_right, spline.bezier_points[start+1].handle_left, spline.bezier_points[start+1].co]
    w.write(":degree %i" % (len(points)-1))
    w.write(":points [%s]" % ",".join(",".join(str(f) for f in p) for p in points))
    w.write(":width [%f, %f]" % (wfactor*spline.bezier_points[0].radius, wfactor*spline.bezier_points[-1].radius))

    w.goOut()
    w.write(")")


def export_curve(exporter, obj):
    for i in range(len(obj.data.splines)):
        if obj.data.splines[i].type != 'BEZIER':
            print("PearRay can only export bezier splines!")
            continue
        for j in range(len(obj.data.splines[i].bezier_points)-1):
            export_curve_spline(exporter, obj, i, j)