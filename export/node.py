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


def _export_image_texture(exporter, socket):
    qual_name = exporter.register_unique_name(
        'NODE', socket.name + "_node")

    img_name = export_image(exporter, socket.image)

    exporter.w.write("(texture")
    exporter.w.goIn()

    exporter.w.write(":name '%s'" % qual_name)
    exporter.w.write(":type 'color'")
    exporter.w.write(":file '%s'" % img_name)

    if socket.extension == "EXTEND":
        exporter.w.write(":wrap 'clamp'")
    elif socket.extension == "CLIP":
        exporter.w.write(":wrap 'black'")
    else:
        exporter.w.write(":wrap 'periodic'")

    if socket.interpolation == "Closest":
        exporter.w.write(":interpolation 'closest'")
    elif socket.interpolation == "Cubic":
        exporter.w.write(":interpolation 'bicubic'")
    else:
        exporter.w.write(":interpolation 'blinear'")

    exporter.w.goOut()
    exporter.w.write(")")

    return "'%s'" % qual_name


def _export_node(exporter, node, factor=1, asLight=False):
    if isinstance(node, bpy.types.ShaderNodeTexImage):
        return _export_image_texture(exporter, node)
    else:
        print("Shader Node '%s' is not supported" % node.name)
        return "''"


def export_node(exporter, socket, factor=1, asLight=False):
    if socket.is_linked:
        return _export_node(exporter, socket.links[0].from_node, factor, asLight)
    else:
        return _export_default(exporter, socket, factor, asLight)
