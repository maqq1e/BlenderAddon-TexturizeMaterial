import bpy
from .main import *

def assign_hotkey(
        addon_keymaps, 
        id_name, 
        HOTKEY, 
        CONTEXT = {'name':"Object Mode", 'space_type':'EMPTY'}, 
        EVENT = 'PRESS', 
        isShift = False, 
        isCtrl = False
    ):
    '''Add hotkey by class name.'''
    wm = bpy.context.window_manager
    kc = wm.keyconfigs.addon
    km = kc.keymaps.new(name = CONTEXT['name'], space_type = CONTEXT['space_type'])
    kmi = km.keymap_items.new(id_name, HOTKEY, EVENT, shift=isShift, ctrl=isCtrl)
    addon_keymaps.append((km, kmi))

def register_keymaps(_ak):
    assign_hotkey(_ak, SelectGroup.bl_idname, 'LEFTMOUSE', isCtrl = True, isShift = True)
    assign_hotkey(_ak, addonControlMenuCall.bl_idname, 'E', isShift = True)
