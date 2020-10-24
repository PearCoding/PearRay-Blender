from .spectral import write_spectral_color
from .texture import export_image
import mathutils
import bpy


def _export_default(exporter, socket, factor=1, asLight=False):
    default_value = getattr(socket, "default_value")
    if default_value is None:
        print("Socket %s has no default value" % socket.name)
        return "0"
    else:
        try:  # Try color
            return write_spectral_color(default_value, factor=factor, asLight=asLight)
        except Exception:
            return "%f" % (default_value*factor)


def _export_scalar_value(exporter, node):
    return "%f" % (node.outputs[0].default_value)


def _export_scalar_clamp(exporter, node):
    clamp_type = node.clamp_type  # TODO: ???

    val = export_node(exporter, node.inputs[0])
    minv = export_node(exporter, node.inputs[1])
    maxv = export_node(exporter, node.inputs[2])

    return "(min %f (max %f %f))" % (minv, maxv, val)


def _export_scalar_maprange(exporter, node):
    val = export_node(exporter, node.inputs[0])
    from_min = export_node(exporter, node.inputs[1])
    from_max = export_node(exporter, node.inputs[2])
    to_min = export_node(exporter, node.inputs[3])
    to_max = export_node(exporter, node.inputs[4])

    ops = ""
    if node.interpolation_type == "LINEAR":
        from_range = "(sub %s %s)" % (from_max, from_min)
        to_range = "(sub %s %s)" % (to_max, to_min)
        to_unit = "(div (sub %s %s) %s)" % (val, from_min, from_range)
        ops = "(add (mul %s %s) %s)" % (to_unit, to_range, to_min)
    else:
        print("Not supported interpolation type %s for node '%s'" %
              (node.interpolation_type, node.name))
        return "0"

    if node.clamp:
        return "(min %s (max %s %s))" % (to_min, to_max, ops)
    else:
        return ops


def _export_scalar_math(exporter, node):
    # TODO: LESS_THAN, GREATER_THAN, SIGN, COMPARE, SMOOTH_MIN, SMOOTH_MAX, TRUNC, FRACT, MODULO, WRAP
    # NOT SUPPORTED: SNAP, PINGPONG
    ops = ""
    if node.operation == "ADD":
        ops = "(add %s %s)" % (export_node(
            exporter, node.inputs[0]), export_node(exporter, node.inputs[1]))
    elif node.operation == "SUBTRACT":
        ops = "(sub %s %s)" % (export_node(
            exporter, node.inputs[0]), export_node(exporter, node.inputs[1]))
    elif node.operation == "MULTIPLY":
        ops = "(mul %s %s)" % (export_node(
            exporter, node.inputs[0]), export_node(exporter, node.inputs[1]))
    elif node.operation == "DIVIDE":
        ops = "(div %s %s)" % (export_node(
            exporter, node.inputs[0]), export_node(exporter, node.inputs[1]))
    elif node.operation == "MULTIPLY_ADD":
        ops = "(add (mul %s %s) %s)" % (export_node(exporter, node.inputs[0]), export_node(
            exporter, node.inputs[1]), export_node(exporter, node.inputs[2]))
    elif node.operation == "POWER":
        ops = "(pow %s %s)" % (export_node(
            exporter, node.inputs[0]), export_node(exporter, node.inputs[1]))
    elif node.operation == "LOGARITHM":
        ops = "(log %s)" % (export_node(exporter, node.inputs[0]))
    elif node.operation == "SQRT":
        ops = "(sqrt %s)" % (export_node(exporter, node.inputs[0]))
    elif node.operation == "INVERSE_SQRT":
        ops = "(div 1 (sqrt %s))" % (export_node(exporter, node.inputs[0]))
    elif node.operation == "ABSOLUTE":
        ops = "(abs %s)" % (export_node(exporter, node.inputs[0]))
    elif node.operation == "EXPONENT":
        ops = "(exp %s)" % (export_node(exporter, node.inputs[0]))
    elif node.operation == "MINIMUM":
        ops = "(min %s %s)" % (export_node(
            exporter, node.inputs[0]), export_node(exporter, node.inputs[1]))
    elif node.operation == "MAXIMUM":
        ops = "(max %s %s)" % (export_node(
            exporter, node.inputs[0]), export_node(exporter, node.inputs[1]))
    elif node.operation == "ROUND":
        ops = "(round %s)" % (export_node(exporter, node.inputs[0]))
    elif node.operation == "FLOOR":
        ops = "(floor %s)" % (export_node(exporter, node.inputs[0]))
    elif node.operation == "CEIL":
        ops = "(ceil %s)" % (export_node(exporter, node.inputs[0]))
    elif node.operation == "SINE":
        ops = "(sin %s)" % (export_node(exporter, node.inputs[0]))
    elif node.operation == "COSINE":
        ops = "(cos %s)" % (export_node(exporter, node.inputs[0]))
    elif node.operation == "TANGENT":
        ops = "(tan %s)" % (export_node(exporter, node.inputs[0]))
    elif node.operation == "ARCSINE":
        ops = "(asin %s)" % (export_node(exporter, node.inputs[0]))
    elif node.operation == "ARCCOSINE":
        ops = "(acos %s)" % (export_node(exporter, node.inputs[0]))
    elif node.operation == "ARCTANGENT":
        ops = "(atan %s)" % (export_node(exporter, node.inputs[0]))
    elif node.operation == "SINH":
        ops = "(sinh %s)" % (export_node(exporter, node.inputs[0]))
    elif node.operation == "COSH":
        ops = "(cosh %s)" % (export_node(exporter, node.inputs[0]))
    elif node.operation == "TANH":
        ops = "(tanh %s)" % (export_node(exporter, node.inputs[0]))
    elif node.operation == "ARCTAN2":
        ops = "(atan2 %s %s)" % (export_node(
            exporter, node.inputs[0]), export_node(exporter, node.inputs[1]))
    elif node.operation == "RADIANS":
        ops = "(mul 0.01745329251 %s)" % (
            export_node(exporter, node.inputs[0]))
    elif node.operation == "DEGREES":
        ops = "(mul 57.2957795131 %s)" % (
            export_node(exporter, node.inputs[0]))
    else:
        print("Not supported math operation %s for node '%s'" %
              (node.operation, node.name))
        return "0"

    if node.use_clamp:
        return "(min 1 (max 0 %s))" % ops
    else:
        return ops


def _export_spectral_value(exporter, node, factor, asLight):
    return write_spectral_color(node.outputs[0].default_value, factor=factor, asLight=asLight)


def _export_spectral_math(exporter, node):
    # See https://docs.gimp.org/en/gimp-concepts-layer-modes.html
    # NOT SUPPORTED: HUE, SATURATION, COLOR, VALUE

    fac = export_node(exporter, node.inputs[0])
    col1 = export_node(exporter, node.inputs[1])  # Background (I)
    col2 = export_node(exporter, node.inputs[2])  # Foreground (M)

    ops = ""
    if node.blend_type == "MIX":
        ops = col2
    elif node.blend_type == "BURN":  # Only valid if between 0 1
        ops = "(sburn %s %s)" % (col1, col2)
    elif node.blend_type == "DARKEN":
        ops = "(smin %s %s)" % (col1, col2)
    elif node.blend_type == "LIGHTEN":
        ops = "(smax %s %s)" % (col1, col2)
    elif node.blend_type == "SCREEN":  # Only valid if between 0 1
        ops = "(sscreen %s %s)" % (col1, col2)
    elif node.blend_type == "DODGE":  # Only valid if between 0 1
        ops = "(sdodge %s %s)" % (col1, col2)
    elif node.blend_type == "OVERLAY":   # Only valid if between 0 1
        ops = "(soverlay %s %s)" % (col1, col2)
    elif node.blend_type == "SOFT_LIGHT":   # Only valid if between 0 1
        ops = "(ssoftlight %s %s)" % (col1, col2)
    elif node.blend_type == "LINEAR_LIGHT":  # Only valid if between 0 1
        ops = "(shardlight %s %s)" % (col1, col2)
    elif node.blend_type == "DIFFERENCE":
        ops = "(smax 0 (ssub %s %s))" % (col1, col2)
    elif node.blend_type == "ADD":
        ops = "(sadd %s %s)" % (col1, col2)
    elif node.blend_type == "SUBTRACT":
        ops = "(ssub %s %s)" % (col1, col2)
    elif node.blend_type == "MULTIPLY":
        ops = "(smul %s %s)" % (col1, col2)
    elif node.blend_type == "DIVIDE":
        ops = "(sdiv %s (sadd %s 1))" % (col1, col2)
    else:
        print("Not supported math operation %s for node '%s'" %
              (node.operation, node.name))
        return "0"

    if node.inputs[0].is_linked or node.inputs[0].default_value != 1:  # TODO: Prevent copying?
        ops = "(sblend %s %s %s)" % (fac, col1, ops)

    if node.use_clamp:
        return "(smin 1 (smax 0 %s))" % ops
    else:
        return ops


def _export_spectral_gamma(exporter, node):
    color_node = export_node(exporter, node.inputs[0])
    gamma_node = export_node(exporter, node.inputs[1])
    return "(smul %s (exp %s))" % (color_node, gamma_node)


def _export_spectral_brightcontrast(exporter, node):
    color_node = export_node(exporter, node.inputs[0])
    bright_node = export_node(exporter, node.inputs[1])
    contrast_node = export_node(exporter, node.inputs[2])

    return "(sbrightnesscontrast %s %s %s)" % (color_node, bright_node, contrast_node)


def _export_spectral_invert(exporter, node):
    # Only valid if values between 0 and 1

    fac = export_node(exporter, node.inputs[0])
    col1 = export_node(exporter, node.inputs[1])

    if node.inputs[0].is_linked or node.inputs[0].default_value != 1:
        return "(sblend %s %s (ssub 1 %s))" % (fac, col1, col1)
    else:
        return "(ssub 1 %s)" % col1


def _export_blackbody(exporter, node):
    print("Warning: Blackbody node operates in radiance units!")
    temp_node = export_node(exporter, node.inputs["Temperature"])
    return "(blackbody %s)" % temp_node


def _export_wavelength(exporter, node):
    wvl_node = export_node(exporter, node.inputs["Wavelength"])
    return "(triangle_peak %s 1)" % wvl_node


def _export_image_texture(exporter, node):
    qual_name = exporter.register_unique_name(
        'NODE', node.name + "_node")

    img_name = export_image(exporter, node.image)

    exporter.w.write("(texture")
    exporter.w.goIn()

    exporter.w.write(":name '%s'" % qual_name)
    exporter.w.write(":type 'color'")
    exporter.w.write(":file '%s'" % img_name)

    if node.extension == "EXTEND":
        exporter.w.write(":wrap 'clamp'")
    elif node.extension == "CLIP":
        exporter.w.write(":wrap 'black'")
    else:
        exporter.w.write(":wrap 'periodic'")

    if node.interpolation == "Closest":
        exporter.w.write(":interpolation 'closest'")
    elif node.interpolation == "Cubic":
        exporter.w.write(":interpolation 'bicubic'")
    else:
        exporter.w.write(":interpolation 'bilinear'")

    exporter.w.goOut()
    exporter.w.write(")")

    return "'%s'" % qual_name


def _export_node(exporter, socket, node, factor, asLight):
    if isinstance(node, bpy.types.ShaderNodeTexImage):
        return _export_image_texture(exporter, node)
    elif isinstance(node, bpy.types.ShaderNodeMath):
        return _export_scalar_math(exporter, node)
    elif isinstance(node, bpy.types.ShaderNodeValue):
        return _export_scalar_value(exporter, node)
    elif isinstance(node, bpy.types.ShaderNodeClamp):
        return _export_scalar_clamp(exporter, node)
    elif isinstance(node, bpy.types.ShaderNodeMapRange):
        return _export_scalar_maprange(exporter, node)
    elif isinstance(node, bpy.types.ShaderNodeMixRGB):
        return _export_spectral_math(exporter, node)
    elif isinstance(node, bpy.types.ShaderNodeInvert):
        return _export_spectral_invert(exporter, node)
    elif isinstance(node, bpy.types.ShaderNodeRGB):
        return _export_spectral_value(exporter, node, factor, asLight)
    elif isinstance(node, bpy.types.ShaderNodeGamma):
        return _export_spectral_gamma(exporter, node)
    elif isinstance(node, bpy.types.ShaderNodeBrightContrast):
        return _export_spectral_brightcontrast(exporter, node)
    elif isinstance(node, bpy.types.ShaderNodeBlackbody):
        return _export_blackbody(exporter, node)
    elif isinstance(node, bpy.types.ShaderNodeWavelength):
        return _export_wavelength(exporter, node)
    else:
        print("Shader Node '%s' is not supported" % node.name)
        return "''"


def export_node(exporter, socket, factor=1, asLight=False):
    if socket.is_linked:
        return _export_node(exporter, socket, socket.links[0].from_node, factor, asLight)
    else:
        return _export_default(exporter, socket, factor, asLight)
