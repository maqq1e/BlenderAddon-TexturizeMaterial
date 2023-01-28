import bpy
from .defers import *

# Temporary paths
SOURCED_COL = "_sourced_"

PREFAB_COL = "PREFAB"

class OBJECT_OT_TexturizeMaterial(bpy.types.Operator):
    """Bake Objects Material Into Texture"""
    bl_idname = "object.create_copy_in_new_collection"
    bl_label = "Bake Material Object into Texture"
    
    def execute(self, context):
        
        _sourced_ = setup_scene_folders()
        
        merge_selected_objects(_sourced_)
               
        
        return {'FINISHED'}

class OBJECT_OT_select_group(bpy.types.Operator):
    """Select Group"""
    bl_idname = "object.select_group"
    bl_label = "Select Group"
    

    def execute(self, context):
        selected_object = context.active_object
        
        try:
            _k = selected_object["edited"]
        except KeyError:
            return {'FINISHED'}
        
        bpy.ops.object.select_grouped(type='PARENT')
        bpy.ops.object.select_grouped(type='CHILDREN_RECURSIVE')
        
        return {'FINISHED'}


UsesClasses = [
    OBJECT_OT_TexturizeMaterial,
    OBJECT_OT_select_group,
]

