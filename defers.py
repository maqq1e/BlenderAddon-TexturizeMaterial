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
    bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)
    
    # Create Original Objects Empty
    bpy.ops.object.empty_add(type='PLAIN_AXES', align='WORLD', location=(0,0,0), scale=(0.5, 0.5, 0.5))
    org_emp = bpy.context.active_object
    # Make Orgininal Object Empty Hide
    bpy.ops.object.hide_view_set(unselected=False)
    # Assign Orgininal Object Empty to Main Empty
    org_emp.parent = merged_object

    bpy.ops.object.select_all(action='DESELECT')
    # Assign all original objects into original objects empty - and hide it
    for obj in original_objects:
        obj_matrix = obj.matrix_world.copy()
        obj.parent = org_emp
        obj.matrix_world = obj_matrix
        obj.hide_viewport = True


    merged_object['isEdit'] = False
    merged_object['original'] = original_objects

def unmerge_selected_objects():
    selected_object = bpy.context.active_object

    original_objects = selected_object['original']

    selected_object.hide_viewport = True

    for obj in original_objects:
        obj.hide_viewport = False
        obj.select_set(True)
    
def get_merged_object():
    selected_object = bpy.context.active_object
    emt_obj = selected_object.parent
    merged_object = emt_obj.parent

    for org_obj in emt_obj.children:
        org_obj.hide_viewport = True
    
    merged_object.hide_viewport = False

