import bpy
import tempfile


def export_image(exporter, image):
    path = ''
    if image.source in {'GENERATED', 'FILE'}:
        if image.source == 'GENERATED':
            path = exporter.create_file(name_hint=image.name + ".png")
            image.save_render(path, scene=exporter.scene)
        elif image.source == 'FILE':
            if image.packed_file:
                path = exporter.create_file(name_hint=image.name)
                image.save_render(path, scene=exporter.scene)
            else:
                path = image.filepath

    return bpy.path.resolve_ncase(bpy.path.abspath(path)).replace("\\", "\\\\")
