import bpy
import tempfile


def export_image(exporter, image):
    path = ''
    if image.source in {'GENERATED', 'FILE'}:
        if image.source == 'GENERATED':
            path = exporter.create_file(name_hint=image.name + ".png")
            image.save_render(path, exporter.scene)
        elif image.source == 'FILE':
            if image.packed_file:
                path = exporter.create_file(name_hint=image.name)
                image.save_render(path, exporter.scene)
            else:
                path = image.filepath

    return bpy.path.resolve_ncase(bpy.path.abspath(path)).replace("\\", "\\\\")


def export_texture(exporter, texture):
    if not texture:
        return ''

    if texture.type != 'IMAGE':
        return ''

    if texture.name in exporter.instances['NODE']:
        return texture.name

    name = exporter.register_unique_name('NODE', texture.name)
    img_name = export_image(exporter, texture.image)

    exporter.w.write("(texture")
    exporter.w.goIn()

    exporter.w.write(":name '%s'" % name)
    exporter.w.write(":type 'color'")
    exporter.w.write(":file '%s'" % img_name)

    exporter.w.goOut()
    exporter.w.write(")")

    return name
