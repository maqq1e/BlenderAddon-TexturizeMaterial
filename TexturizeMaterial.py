import bpy

bl_info = {
    "name": "Texturize Material",
    "author": "daniel.hramkov@gmail.com",
    "description": "Create multi-object material into one single texture material.",
    "blender": (3, 0, 0),
    "version": (0, 0, 1),
}


# Temporary paths
SOURCED_COL = "_sourced_"

PREFAB_COL = "PREFAB"


def setup_scene_folders():
        
    _sourced_ = bpy.data.collections.get(SOURCED_COL)
    
    # Create collection if not exist
    if ( _sourced_ == None):
        _sourced_ = bpy.data.collections.new(name=SOURCED_COL)
        bpy.context.scene.collection.children.link(_sourced_)
        _sourced_.hide_viewport = True
        
    prefab_coolection = bpy.data.collections.get(PREFAB_COL)        
    
    # Create collection if not exist 
    if( prefab_coolection == None):
        prefab_coolection = bpy.data.collections.new(name=PREFAB_COL)
        bpy.context.scene.collection.children.link(prefab_coolection)
    
    return _sourced_
    


def merge_selected_objects(_sourced_):
    
    _sourced_.hide_viewport = False
        
    # Get selected objects
    original_objects = bpy.context.selected_objects
        
    # Move all original_objects to this new source collection
    index = bpy.data.collections.find(SOURCED_COL) + 1
    bpy.ops.object.move_to_collection(collection_index=index)
    
    # Dublicate objects in scene
    bpy.ops.object.duplicate(linked=False)      
    # Merge the copies into one mesh
    bpy.ops.object.join()
    # Select this joited object
    new_obj = bpy.context.active_object
    # Rename it
    dot_index = new_obj.name.index('.')
    new_obj.name = new_obj.name[:dot_index] + '_bkd'
    
    # Move it into PREFAB collection
    index = bpy.data.collections.find(PREFAB_COL) + 1
    bpy.ops.object.move_to_collection(collection_index=index)
    
    # Add a property to the new mesh that contains the list of original selected objects
    new_obj["original_objects"] = original_objects
    
    _sourced_.hide_viewport = True


class OBJECT_OT_TexturizeMaterial(bpy.types.Operator):
    """Bake Objects Material Into Texture"""
    bl_idname = "object.create_copy_in_new_collection"
    bl_label = "Bake Material Object into Texture"
    
    def execute(self, context):
        
        _sourced_ = setup_scene_folders()
        
        merge_selected_objects(_sourced_)
               
        
        return {'FINISHED'}

def draw_TexturizeMaterial(self, context):
    layout = self.layout
    layout.operator("object.create_copy_in_new_collection", text="Bake Into Texture")


class OBJECT_OT_select_group(bpy.types.Operator):
    """Select Group"""
    bl_idname = "object.select_group"
    bl_label = "Select Group"
    

    def execute(self, context):
        selected_object = bpy.context.active_object
        
        try:
            _k = selected_object["edited"]
        except KeyError:
            return {'FINISHED'}
        
        bpy.ops.object.select_grouped(type='PARENT')
        bpy.ops.object.select_grouped(type='CHILDREN_RECURSIVE')

        
        return {'FINISHED'}

def register():
    bpy.utils.register_class(OBJECT_OT_create_cube)

def unregister():
    bpy.utils.unregister_class(OBJECT_OT_create_cube)



UsesClasses = [
    OBJECT_OT_TexturizeMaterial,
    OBJECT_OT_select_group,
]



    
# assign a hotkey to the operator
addon_keymaps = []
def register_keymaps():
    wm = bpy.context.window_manager
    kc = wm.keyconfigs.addon
    if kc:
        km = kc.keymaps.new(name="Object Mode", space_type='EMPTY')
        kmi = km.keymap_items.new(OBJECT_OT_select_group.bl_idname, 'LEFTMOUSE', 'PRESS', shift=False, ctrl=True)
        addon_keymaps.append((km, kmi))

def unregister_keymaps():
    for km, kmi in addon_keymaps:
        km.keymap_items.remove(kmi)
    addon_keymaps.clear()
    
    


def register():
    for useClass in UsesClasses:
        bpy.utils.register_class(useClass)
    bpy.types.VIEW3D_MT_object_context_menu.append(draw_TexturizeMaterial)

def unregister():
    bpy.types.VIEW3D_MT_object_context_menu.remove(draw_TexturizeMaterial)
    for useClass in UsesClasses:
        bpy.utils.unregister_class(useClass)


if __name__ == "__main__":
    register()
    register_keymaps()






