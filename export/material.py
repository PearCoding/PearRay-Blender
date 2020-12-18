from .spectral import write_spectral_color
from .node import export_node
import bpy


def _extract_material_bsdf(material):
    if material.node_tree is None:
        return None

    output = material.node_tree.nodes.get("Material Output")
    if output is None:
        return None

    surface = output.inputs.get("Surface")
    if surface is None or not surface.is_linked:
        return None

    return surface.links[0].from_node


def _export_diffuse_bsdf(exporter, bsdf, export_name):
    color_soc = bsdf.inputs["Color"]
    roughness_soc = bsdf.inputs["Roughness"]

    color_name = export_node(exporter, color_soc)

    roughness_name = None

    if roughness_soc.is_linked:
        roughness_name = export_node(exporter, roughness_soc)

    exporter.w.write("(material")
    exporter.w.goIn()

    exporter.w.write(":name '%s'" % export_name)

    if roughness_name is not None:
        exporter.w.write(":type 'orennayar'")
    else:
        exporter.w.write(":type 'diffuse'")

    exporter.w.write(":albedo %s" % color_name)
    if roughness_name is not None:
        exporter.w.write(":roughness %s" % roughness_name)

    exporter.w.goOut()
    exporter.w.write(")")


def _export_glass_bsdf(exporter, bsdf, export_name):
    color = export_node(exporter, bsdf.inputs["Color"])
    roughness = export_node(exporter, bsdf.inputs["Roughness"])
    ior = export_node(exporter, bsdf.inputs["IOR"])

    exporter.w.write("(material")
    exporter.w.goIn()

    exporter.w.write(":name '%s'" % export_name)
    exporter.w.write(":type 'dielectric'")

    exporter.w.write(":specularity %s" % color)
    exporter.w.write(":roughness %s" % roughness)
    exporter.w.write(":index %s" % ior)

    exporter.w.goOut()
    exporter.w.write(")")


def _export_glossy_bsdf(exporter, bsdf, export_name):
    # A simple principled shader
    base_color = export_node(exporter, bsdf.inputs["Color"])
    roughness = export_node(exporter, bsdf.inputs["Roughness"])

    exporter.w.write("(material")
    exporter.w.goIn()

    exporter.w.write(":name '%s'" % export_name)
    exporter.w.write(":type 'principled'")

    exporter.w.write(":base_color %s" % base_color)
    exporter.w.write(":roughness %s" % roughness)
    exporter.w.write(":specular 1")

    exporter.w.goOut()
    exporter.w.write(")")


def _export_principled_bsdf(exporter, bsdf, export_name):
    base_color    = export_node(exporter, bsdf.inputs["Base Color"])
    roughness     = export_node(exporter, bsdf.inputs["Roughness"])
    subsurface    = export_node(exporter, bsdf.inputs["Subsurface"])
    metallic      = export_node(exporter, bsdf.inputs["Metallic"])
    specular      = export_node(exporter, bsdf.inputs["Specular"])
    specular_tint = export_node(exporter, bsdf.inputs["Specular Tint"])
    transmission  = export_node(exporter, bsdf.inputs["Transmission"])
    anisotropic   = export_node(exporter, bsdf.inputs["Anisotropic"])
    # anisotropic_rotation = export_node(exporter, bsdf.inputs["Anisotropic Rotation"])
    sheen         = export_node(exporter, bsdf.inputs["Sheen"])
    sheen_tint    = export_node(exporter, bsdf.inputs["Sheen Tint"])
    clearcoat     = export_node(exporter, bsdf.inputs["Clearcoat"])

    exporter.w.write("(material")
    exporter.w.goIn()

    exporter.w.write(":name '%s'" % export_name)
    exporter.w.write(":type 'principled'")

    exporter.w.write(":base_color %s" % base_color)
    exporter.w.write(":roughness %s" % roughness)
    exporter.w.write(":flatness %s" % subsurface)
    exporter.w.write(":metallic %s" % metallic)
    exporter.w.write(":anisotropic %s" % anisotropic)
    exporter.w.write(":specular %s" % specular)
    exporter.w.write(":specular_tint %s" % specular_tint)
    exporter.w.write(":specular_transmission %s" % transmission)
    exporter.w.write(":sheen %s" % sheen)
    exporter.w.write(":sheen_tint %s" % sheen_tint)
    exporter.w.write(":clearcoat %s" % clearcoat)
    # exporter.w.write(":clearcoat_gloss %s" % clearcoat_gloss)

    exporter.w.goOut()
    exporter.w.write(")")


def _export_add_bsdf(exporter, bsdf, export_name):
    mat1 = export_bsdf_inline(exporter, bsdf.inputs[0], export_name)
    mat2 = export_bsdf_inline(exporter, bsdf.inputs[1], export_name)

    if mat1 is None or mat2 is None:
        print("Mix BSDF %s has no valid bsdf input " % export_name)
        return

    exporter.w.write("(material")
    exporter.w.goIn()

    exporter.w.write(":name '%s'" % export_name)
    exporter.w.write(":type 'add'")

    exporter.w.write(":material1 '%s'" % mat1)
    exporter.w.write(":material2 '%s'" % mat2)

    exporter.w.goOut()
    exporter.w.write(")")


def _export_mix_bsdf(exporter, bsdf, export_name):
    mat1 = export_bsdf_inline(exporter, bsdf.inputs[1], export_name)
    mat2 = export_bsdf_inline(exporter, bsdf.inputs[2], export_name)
    factor = export_node(exporter, bsdf.inputs["Fac"])

    if mat1 is None or mat2 is None:
        print("Mix BSDF %s has no valid bsdf input " % export_name)
        return

    exporter.w.write("(material")
    exporter.w.goIn()

    exporter.w.write(":name '%s'" % export_name)
    exporter.w.write(":type 'blend'")

    exporter.w.write(":material1 '%s'" % mat1)
    exporter.w.write(":material2 '%s'" % mat2)
    exporter.w.write(":factor %s" % factor)

    exporter.w.goOut()
    exporter.w.write(")")


def export_bsdf(exporter, bsdf, prename):
    name = exporter.register_unique_name('MATERIAL', prename)
    if bsdf is None:
        print("Material %s has no valid BSDF!" % name)
        return exporter.MISSING_MAT
    elif isinstance(bsdf, bpy.types.ShaderNodeBsdfDiffuse):
        _export_diffuse_bsdf(exporter, bsdf, name)
    elif isinstance(bsdf, bpy.types.ShaderNodeBsdfGlass):
        _export_glass_bsdf(exporter, bsdf, name)
    elif isinstance(bsdf, bpy.types.ShaderNodeBsdfGlossy):
        _export_glossy_bsdf(exporter, bsdf, name)
    elif isinstance(bsdf, bpy.types.ShaderNodeBsdfPrincipled):
        _export_principled_bsdf(exporter, bsdf, name)
    elif isinstance(bsdf, bpy.types.ShaderNodeMixShader):
        _export_mix_bsdf(exporter, bsdf, name)
    elif isinstance(bsdf, bpy.types.ShaderNodeAddShader):
        _export_add_bsdf(exporter, bsdf, name)
    else:
        print("Material %s has a '%s' which is not supported " %
              (name, bsdf.name))
        return exporter.MISSING_MAT
    return name


def export_bsdf_inline(exporter, socket, prename):
    if not socket.is_linked:
        return None

    return export_bsdf(exporter, socket.links[0].from_node, prename)


def export_material(exporter, material):
    if not material:
        return

    if material.name in exporter.instances['MATERIAL']:
        return

    export_bsdf(exporter, _extract_material_bsdf(material), material.name)


def export_default_materials(exporter):
    exporter.MISSING_MAT = exporter.register_unique_name(
        'MATERIAL', "_missing_mat")

    missing_spec_n = write_spectral_color((1.0, 0.7, 0.8))

    exporter.w.write("(material")
    exporter.w.goIn()

    exporter.w.write(":name '%s'" % exporter.MISSING_MAT)
    exporter.w.write(":type 'diffuse'")
    exporter.w.write(":albedo %s" % missing_spec_n)

    exporter.w.goOut()
    exporter.w.write(")")
