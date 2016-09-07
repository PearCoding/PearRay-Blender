import bpy


from bl_ui.properties_material import MaterialButtonsPanel


class MATERIAL_PT_context_material(MaterialButtonsPanel, bpy.types.Panel):
    bl_label = ""
    bl_options = {'HIDE_HEADER'}
    COMPAT_ENGINES = {'PEARRAY_RENDER'}

    @classmethod
    def poll(cls, context):
        # An exception, don't call the parent poll func because
        # this manages materials for all engine types

        engine = context.scene.render.engine
        return (context.material or context.object) and (engine in cls.COMPAT_ENGINES)

    def draw(self, context):
        layout = self.layout

        mat = context.material
        ob = context.object
        slot = context.material_slot
        space = context.space_data
        is_sortable = (len(ob.material_slots) > 1)

        if ob:
            rows = 1
            if is_sortable:
                rows = 4

            row = layout.row()

            row.template_list("MATERIAL_UL_matslots", "", ob, "material_slots", ob, "active_material_index", rows=rows)

            col = row.column(align=True)
            col.operator("object.material_slot_add", icon='ZOOMIN', text="")
            col.operator("object.material_slot_remove", icon='ZOOMOUT', text="")

            col.menu("MATERIAL_MT_specials", icon='DOWNARROW_HLT', text="")

            if is_sortable:
                col.separator()

                col.operator("object.material_slot_move", icon='TRIA_UP', text="").direction = 'UP'
                col.operator("object.material_slot_move", icon='TRIA_DOWN', text="").direction = 'DOWN'

            if ob.mode == 'EDIT':
                row = layout.row(align=True)
                row.operator("object.material_slot_assign", text="Assign")
                row.operator("object.material_slot_select", text="Select")
                row.operator("object.material_slot_deselect", text="Deselect")

        split = layout.split(percentage=0.65)

        if ob:
            split.template_ID(ob, "active_material", new="material.new")
            row = split.row()

            if slot:
                row.prop(slot, "link", text="")
            else:
                row.label()
        elif mat:
            split.template_ID(space, "pin_id")
            split.separator()


class MATERIAL_PT_preview(MaterialButtonsPanel, bpy.types.Panel):
    bl_label = "Preview"
    COMPAT_ENGINES = {'PEARRAY_RENDER'}

    def draw(self, context):
        self.layout.template_preview(context.material)


def color_template(mat, layout, name):
    sub_mat = mat
    if not hasattr(mat, name):
        sub_mat = mat.pearray
    
    split = layout.split()
    split.prop(mat.pearray, '%s_type' % name, text="")
    if getattr(mat.pearray, '%s_type' % name) == 'TEMP':
        split.prop(mat.pearray, '%s_temp' % name, text="")
    else:
        split.prop(sub_mat, name, text="")


class MATERIAL_PT_brdf(MaterialButtonsPanel, bpy.types.Panel):
    bl_label = "BRDF"
    COMPAT_ENGINES = {'PEARRAY_RENDER'}

    @classmethod
    def poll(cls, context):
        engine = context.scene.render.engine
        return context.material and (engine in cls.COMPAT_ENGINES)

    def draw(self, context):
        layout = self.layout

        mat = context.material
        type = mat.pearray.brdf

        split = layout.split()

        col = split.column()
        col.prop(mat.pearray, "brdf")

        split = col.split()
        col = split.column()
        col.prop(mat.pearray, "cast_shadows")
        col.prop(mat.pearray, "cast_self_shadows")

        col = split.column()
        col.prop(mat.pearray, "is_camera_visible")
        col.prop(mat.pearray, "is_shadeable")


class MATERIAL_PT_diffuse(MaterialButtonsPanel, bpy.types.Panel):
    bl_label = "Diffuse"
    COMPAT_ENGINES = {'PEARRAY_RENDER'}

    @classmethod
    def poll(cls, context):
        engine = context.scene.render.engine
        return context.material and (context.material.pearray.brdf in {'DIFFUSE', 'ORENNAYAR', 'WARD'}) and (engine in cls.COMPAT_ENGINES)

    def draw(self, context):
        layout = self.layout

        mat = context.material
        type = mat.pearray.brdf

        split = layout.split()

        col = split.column()
        color_template(mat, col, "diffuse_color")
        if type == 'ORENNAYAR':
            col.prop(mat, 'roughness')
        elif type == 'WARD':
            col2 = col.column(align=True)
            col2.prop(mat.pearray, 'roughnessX')
            col2.prop(mat.pearray, 'roughnessY')            


class MATERIAL_PT_grid(MaterialButtonsPanel, bpy.types.Panel):
    bl_label = "Grid"
    COMPAT_ENGINES = {'PEARRAY_RENDER'}

    @classmethod
    def poll(cls, context):
        engine = context.scene.render.engine
        return context.material and (context.material.pearray.brdf == 'GRID') and (engine in cls.COMPAT_ENGINES)

    def draw(self, context):
        layout = self.layout

        mat = context.material
        type = mat.pearray.brdf

        split = layout.split()

        col = split.column()


class MATERIAL_PT_specular(MaterialButtonsPanel, bpy.types.Panel):
    bl_label = "Specular"
    COMPAT_ENGINES = {'PEARRAY_RENDER'}

    @classmethod
    def poll(cls, context):
        engine = context.scene.render.engine
        return context.material and (context.material.pearray.brdf in {'GLASS', 'MIRROR', 'WARD'}) and (engine in cls.COMPAT_ENGINES)

    def draw(self, context):
        layout = self.layout

        mat = context.material
        type = mat.pearray.brdf

        split = layout.split()

        col = split.column()
        color_template(mat, col, "specular_color")
        if type == 'MIRROR' or type == 'GLASS':
            col.prop(mat, 'specular_ior')


class MATERIAL_PT_emission(MaterialButtonsPanel, bpy.types.Panel):
    bl_label = "Emission"
    COMPAT_ENGINES = {'PEARRAY_RENDER'}

    @classmethod
    def poll(cls, context):
        engine = context.scene.render.engine
        return context.material and (not context.material.pearray.brdf == 'GRID') and (engine in cls.COMPAT_ENGINES)

    def draw(self, context):
        layout = self.layout

        mat = context.material
        type = mat.pearray.brdf

        split = layout.split()

        col = split.column()
        color_template(mat, col, "emission_color")