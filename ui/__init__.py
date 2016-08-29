import bpy


from . import ui


def register():
    bpy.types.RENDER_PT_render.append(ui.draw_pearray_render)
    pass


def unregister():
    bpy.types.RENDER_PT_render.remove(ui.draw_pearray_render)
    pass