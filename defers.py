import bpy
from .globvar import *

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
    

# def merge_selected_objects(_sourced_):
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

def merge_selected_objects():
    # Get selected objects
    original_objects = bpy.context.selected_objects
    # Dublicate objects in scene
    bpy.ops.object.duplicate(linked=False)
    # Merge the copies into one mesh
    bpy.ops.object.join()
    # Select this joited object
    merged_object = bpy.context.active_object
    bpy.ops.object.origin_set(type='ORIGIN_CENTER_OF_VOLUME', center='MEDIAN')
    # Create Main Empty
    bpy.ops.object.empty_add(type='PLAIN_AXES', align='WORLD', location=merged_object.location, scale=(1, 1, 1))
    main_emp = bpy.context.active_object
    # Create Original Objects Empty
    bpy.ops.object.empty_add(type='PLAIN_AXES', align='WORLD', location=merged_object.location, scale=(0.5, 0.5, 0.5))
    org_emp = bpy.context.active_object
    # Assign Orgininal Object Empty to Main Empty
    org_emp.parent = main_emp
    # Assign merged object into Main Empty
    merged_object.parent = main_emp
    merged_object.location = (0, 0, 0)

    # Assign all original objects into original objects empty - and hide it
    for obj in original_objects:
        obj.parent = org_emp
        obj.hide_viewport = True
    # Make Orgininal Object Empty Hide
    org_emp.hide_viewport = True
    







