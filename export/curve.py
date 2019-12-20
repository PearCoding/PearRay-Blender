import collections
import bpy
import mathutils
from .entity import inline_entity_matrix


def export_curve_spline(exporter, obj, index, start):
    w = exporter.w

    spline = obj.data.splines[index]

    wfactor = 2*(obj.data.bevel_depth + obj.data.extrude)
    if wfactor <= 0:
        wfactor = 0.01

    w.write("(entity")
    w.goIn()

    w.write(":name '%s_%i_%i'" % (obj.name, index, start))
    w.write(":type 'curve'")
    w.write(":material '%s'" % obj.data.materials[spline.material_index].name)

    next = spline.bezier_points[start+1] if start + 1 < len(spline.bezier_points) else spline.bezier_points[0]

    points = [spline.bezier_points[start].co, spline.bezier_points[start].handle_right, next.handle_left, next.co]
    w.write(":degree %i" % (len(points)-1))
    w.write(":points [%s]" % ",".join(",".join(str(f) for f in p) for p in points))
    w.write(":width [%f, %f]" % (wfactor*spline.bezier_points[0].radius, wfactor*spline.bezier_points[-1].radius))
    inline_entity_matrix(exporter, obj)

    w.goOut()
    w.write(")")


def conv_to_curve(obj):
    return obj
    # TODO: Not working as intended!
    override = bpy.context.copy()
    override['selected_bases'] = obj
    override['selected_editable_bases'] = obj
    override['active_object'] = obj
    print(override)
    print(bpy.ops.object.convert(override, target='CURVE', keep_original=False))
    print(dir(bpy.context))
    print(bpy.context.scene.objects.active)
    return bpy.context.scene.objects.active


def export_curve(exporter, obj):
    if obj.type == 'FONT':
        obj = conv_to_curve(obj)

    for i in range(len(obj.data.splines)):
        if obj.data.splines[i].type != 'BEZIER':
            print("PearRay can only export bezier splines!")
            continue
        max = len(obj.data.splines[i].bezier_points) if obj.data.splines[i].use_cyclic_u else len(
            obj.data.splines[i].bezier_points)-1
        for j in range(max):
            export_curve_spline(exporter, obj, i, j)

    # Uncomment this when we are sure conv_to_curve works
    # if obj.type == 'FONT':
    #    bpy.data.objects.remove(obj)
