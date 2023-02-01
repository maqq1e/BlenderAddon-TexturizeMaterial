import bpy
from .defers import *
from .globvar import *


class BakeAndMerge(bpy.types.Operator):
    """Bake Objects Material Into Texture"""
    bl_idname = "object.make_objects_baked"
    bl_label = "Bake and Merge"
    
    def execute(self, context):
        
        merge_selected_objects()
        

        return {'FINISHED'}

class EditOriginal(bpy.types.Operator):
    """Edit Original Objects"""
    bl_idname = "object.edit_original"
    bl_label = "Edit Original"
    
    def execute(self, context):
        
        unmerge_selected_objects()
        

        return {'FINISHED'}

class GetPreview(bpy.types.Operator):
    """Preview Baked Object"""
    bl_idname = "object.preview_object"
    bl_label = "Preview"
    
    def execute(self, context):
        
        get_merged_object()
        

        return {'FINISHED'}



class SelectGroup(bpy.types.Operator):
    """Select Group"""
    bl_idname = "object.select_group"
    bl_label = "Select Group"
    

    def execute(self, context):                
        bpy.ops.object.select_grouped(type='PARENT')
        
        return {'FINISHED'}






class AddonControlMenu(bpy.types.Menu):
    '''Menu of Addon'''
    bl_label = "Bake Objects"
    bl_idname = "OBJECT_MT_custom_menu"

    def draw(self, context):
        layout = self.layout

        active_object = bpy.context.active_object

        
        if(active_object.parent != None):
            layout.operator("object.preview_object", icon="RENDER_RESULT")
            return {'FINISHED'}

        try:
            if(active_object['isEdit']):
                return {'Need to be rebake'}
            else:
                layout.operator("object.edit_original", icon="MODIFIER")
        except KeyError:
            layout.operator("object.make_objects_baked", icon="EXPERIMENTAL")
            return {'FINISHED'}


class addonControlMenuCall(bpy.types.Operator):
    bl_idname = "wm.call_menu_example"
    bl_label = "Open the custom menu"

    def execute(self, context):
        bpy.ops.wm.call_menu(name=AddonControlMenu.bl_idname)
        return {'FINISHED'}




UsesClasses = [
    BakeAndMerge,
    EditOriginal,
    GetPreview,
    SelectGroup,
    AddonControlMenu, addonControlMenuCall,
]

