from .spectral import write_spectral_color, write_spectral_temp
from .texture import export_texture
import mathutils
import bpy


def _export_color(exporter, name, node, required,
                  factor=1, asLight=False):
    if required or node.r > 0 or node.g > 0 or node.b > 0:
        return "'%s'" % write_spectral_color(exporter, name,
                                             factor *
                                             mathutils.Color(node[:3]),
                                             asLight=asLight)

    if required:
        return "''"
    else:
        return ""


def _export_tree(exporter, name, node, required,
                 factor=1, asLight=False):
    # TODO: Support node trees
    if required:
        return "''"
    else:
        return ""


def export_node(exporter, name, node, required,
                factor=1, asLight=False):
    qual_name = exporter.register_unique_name('NODE', name + "_node")

    if isinstance(node, bpy.types.NodeTree):
        return _export_tree(exporter, qual_name, node, required, factor, asLight)
    else:
        return _export_color(exporter, qual_name, node, required, factor, asLight)
