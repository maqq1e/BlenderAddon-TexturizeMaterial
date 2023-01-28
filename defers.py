import bpy

def setup_scene_folders():
    '''Return _sourced_ folder'''
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
    ''''''
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
