import bpy

from . import primitives


def menu_func(self, context):
    self.layout.separator()
    self.layout.menu(primitives.OBJECT_MT_AddPrimitives.bl_idname)


def register():
    bpy.types.INFO_MT_add.append(menu_func)


def unregister():
    bpy.types.INFO_MT_add.remove(menu_func)