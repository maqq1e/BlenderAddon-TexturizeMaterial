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

    bpy.ops.object.select_all(action='DESELECT')

    merged_object.select_set(True)
    bpy.context.view_layer.objects.active = merged_object
    

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

def delete_merged_object():
    selected_object = bpy.context.active_object
    merged_object = None


    if(selected_object.parent == None):
        merged_object = selected_object
    else:  
        merged_object = selected_object.parent.parent

    for mrg_child in merged_object.children:
        if(mrg_child.type == 'EMPTY'):
            for org_obj in mrg_child.children:
                org_obj.hide_viewport = False
                org_obj.location = org_obj.location + merged_object.location
                result_rotation = [a + b for a, b in zip(org_obj.rotation_euler, merged_object.rotation_euler)]
                org_obj.rotation_euler = result_rotation
        else:
            return {'Have no empty children in delete_merged_object'}
        bpy.data.objects.remove(mrg_child)
        
    bpy.data.objects.remove(merged_object)
    
def assign_imageTexture_into_shader(res):
    selected_object = bpy.context.active_object

    # get the reference to the materials of the object
    materials = selected_object.data.materials

    # create a new image
    image = bpy.data.images.new(selected_object.name, width=res, height=res)

    # fill the image with a solid color
    pixels = [0.0, 0.0, 0.0, 1.0] * (res * res)
    image.pixels = pixels

    for mat in materials:
        # get the reference to the shader editor for the material
        shader_editor = mat.node_tree

        # create a new image texture node
        img_tex_node = shader_editor.nodes.new(type="ShaderNodeTexImage")

        # specify the image file to use for the texture
        img_tex_node.image = image

def generate_uv():
    selected_object = bpy.context.active_object
    uv = selected_object.data.uv_layers

    bpy.ops.object.mode_set(mode='OBJECT')
    selected_object.select_set(True)    
    bpy.context.view_layer.objects.active = selected_object
    bpy.ops.object.mode_set(mode='EDIT')

    if len(uv) == 2:
        select_uv(1)
        try:
            bpy.ops.uvpackmaster2.uv_pack()
        except bpy.ops.uvpackmaster2:
            bpy.ops.uv.pack_islands(margin=0.1)

    if len(uv) == 1:
        # Unwrap the UVs
        bpy.ops.mesh.uv_texture_add()
        bpy.ops.uv.smart_project()
        bpy.ops.object.mode_set(mode='OBJECT')

    
    bpy.ops.object.mode_set(mode='OBJECT')
    
def select_uv(uv_num = 1):

    selected_object = bpy.context.active_object
    uv = selected_object.data.uv_layers

    # Get the second UV map
    uv_map = uv[uv_num]

    # Select all UVs in the second UV map
    for _uv in uv_map.data:
        _uv.select = True
    
    # Make the second UV map active
    uv.active = uv_map

    
def bake_to_texture(TYPE = 'ALL'):
    bpy.context.scene.render.engine = 'CYCLES'
    bpy.context.scene.cycles.device = 'GPU'

    if TYPE == 'ALL':
        # Set settings
        bpy.context.scene.cycles.bake_type = 'COMBINED'
        bpy.context.scene.render.bake.use_pass_direct = True
        bpy.context.scene.render.bake.use_pass_indirect = True
        bpy.context.scene.render.bake.use_pass_diffuse = True
        bpy.context.scene.render.bake.use_pass_glossy = True
        bpy.context.scene.render.bake.use_pass_transmission = True
        bpy.context.scene.render.bake.use_pass_emit = True

        bpy.ops.object.bake(type='COMBINED')
        
    