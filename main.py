import bpy
from .defers import *
from .globvar import *


class OBJECT_OT_TexturizeMaterial(bpy.types.Operator):
    """Bake Objects Material Into Texture"""
    bl_idname = "object.make_objects_baked"
    bl_label = "Bake Material Object into Texture"
    
    def execute(self, context):
        
        #_sourced_ = setup_scene_folders()
        
        merge_selected_objects()
               
        


        return {'FINISHED'}

class OBJECT_OT_select_group(bpy.types.Operator):
    """Select Group"""
    bl_idname = "object.select_group"
    bl_label = "Select Group"
    

    def execute(self, context):                
        bpy.ops.object.select_grouped(type='PARENT')
        
        return {'FINISHED'}






class AddonControlMenu(bpy.types.Menu):
    '''Menu of Addon'''
    bl_label = "Custom Popup"
    bl_idname = "OBJECT_MT_custom_menu"

    def draw(self, context):
        layout = self.layout

        layout.operator("object.make_objects_baked")

class addonControlMenuCall(bpy.types.Operator):
    bl_idname = "wm.call_menu_example"
    bl_label = "Open the custom menu"

    def execute(self, context):
        bpy.ops.wm.call_menu(name=AddonControlMenu.bl_idname)
        return {'FINISHED'}




UsesClasses = [
    OBJECT_OT_TexturizeMaterial,
    OBJECT_OT_select_group,
    AddonControlMenu, addonControlMenuCall
]

