import bpy


class WorldButtonsPanel():
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "world"
    # COMPAT_ENGINES must be defined in each subclass, external engines can add themselves here

    @classmethod
    def poll(cls, context):
        rd = context.scene.render
        return context.world and (rd.engine in cls.COMPAT_ENGINES)


class WORLD_PT_pr_preview(WorldButtonsPanel, bpy.types.Panel):
    bl_label = "Preview"
    COMPAT_ENGINES = {'PEARRAY_RENDER'}

    def draw(self, context):
        self.layout.template_preview(context.world)


class WORLD_PT_pr_background(WorldButtonsPanel, bpy.types.Panel):
    bl_label = "Background"
    COMPAT_ENGINES = {'PEARRAY_RENDER'}

    def draw(self, context):
        layout = self.layout

        world = context.world

        layout.prop(world.pearray, 'split_background')

        col = layout.column(align=True)
        col.label(text="Background:")
        col.prop(world, "color", text="")

        col = layout.column(align=True)
        col.label(text="Radiance:")
        col.enabled = world.pearray.split_background
        col.prop(world.pearray, "radiance_color", text="")

        layout.prop(world.pearray, 'radiance_factor')


register, unregister = bpy.utils.register_classes_factory([
    WORLD_PT_pr_preview,
    WORLD_PT_pr_background,
])
