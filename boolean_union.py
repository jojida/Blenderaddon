bl_info = {
    "name": "Boolean Union",
    "author": "Your Name",
    "version": (1, 0),
    "blender": (2, 80, 0),
    "location": "View3D > Object > Object Context Menu",
    "description": "Perform a boolean union operation between selected objects.",
    "category": "Object",
}

import bpy


class OBJECT_OT_boolean_union(bpy.types.Operator):
    bl_idname = "object.boolean_union"
    bl_label = "Boolean Union"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return (
            context.object is not None
            and context.object.type == 'MESH'
            and len(context.selected_objects) > 1
        )

    def execute(self, context):
        active_obj = context.object
        selected_objects = context.selected_objects

        for obj in selected_objects:
            if obj != active_obj:
                bpy.context.view_layer.objects.active = obj
                bpy.ops.object.modifier_add(type='BOOLEAN')
                bpy.context.object.modifiers["Boolean"].operation = 'UNION'
                bpy.context.object.modifiers["Boolean"].operand_type = 'OBJECT'
                bpy.context.object.modifiers["Boolean"].object = active_obj

        bpy.context.view_layer.objects.active = active_obj

        return {'FINISHED'}


def menu_func(self, context):
    self.layout.operator(OBJECT_OT_boolean_union.bl_idname, text="Boolean Union")

def register():
    bpy.utils.register_class(OBJECT_OT_boolean_union)
    bpy.types.VIEW3D_MT_object_context_menu.append(menu_func)


def unregister():
    bpy.utils.unregister_class(OBJECT_OT_boolean_union)
    bpy.types.VIEW3D_MT_object_context_menu.remove(menu_func)


if __name__ == "__main__":
    register()
