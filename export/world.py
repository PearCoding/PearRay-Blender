from .node import export_node
import bpy


def _extract_world_bsdf(world):
    if world.node_tree is None:
        return None

    output = world.node_tree.nodes.get("World Output")
    if output is None:
        return None

    surface = output.inputs.get("Surface")
    if surface is None or not surface.is_linked:
        return None

    return surface.links[0].from_node


def export_world(exporter, world):
    bsdf = _extract_world_bsdf(world)
    if bsdf is None:
        return

    if isinstance(bsdf, bpy.types.ShaderNodeBackground):
        color_soc = bsdf.inputs["Color"]
        strength_soc = bsdf.inputs["Strength"]

        color_name = export_node(exporter, color_soc)
        strength_name = export_node(exporter, strength_soc)

        exporter.w.write("(light")
        exporter.w.goIn()

        exporter.w.write(":name '__world'")
        exporter.w.write(":type 'env'")

        if strength_soc.is_linked or strength_soc.default_value != 1:
            exporter.w.write(":radiance (smul (illuminant 'd65') (smul %s %s))" % (strength_name, color_name))
        else:
            exporter.w.write(":radiance (smul (illuminant 'd65') %s)" % color_name)

        exporter.w.goOut()
        exporter.w.write(")")
    else:
        print("Expected 'Background' bsdf for world shader")

