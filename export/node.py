from .spectral import write_spectral_color
from .texture import export_texture
import mathutils
import bpy


def _export_default(exporter, name, socket, factor=1, asLight=False):
    default_value = getattr(socket, "default_value")
    if default_value is None:
        print("Socket %s has no default value" % socket.name)
        return "0"
    else:
        try: # Try color
            return write_spectral_color(default_value, factor=factor, asLight=asLight)
        except Exception:
            return "%f" % (default_value*factor)


def _export_node(exporter, name, node, factor=1, asLight=False):
    # TODO: Support node trees
    return "''"


def export_node(exporter, socket, factor=1, asLight=False):
    qual_name = exporter.register_unique_name(
        'NODE', socket.name + "_node")

    if socket.is_linked:
        return _export_node(exporter, qual_name, socket.links[0].from_node, factor, asLight)
    else:
        return _export_default(exporter, qual_name, socket, factor, asLight)
