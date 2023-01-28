import bpy
from .draw import * # Draw methods
from .main import UsesClasses
from .keymaps import register_keymaps

addon_keymaps = []

# Addon Info
bl_info = {
    "name": "Texturize Material",
    "author": "daniel.hramkov@gmail.com",
    "description": "Create multi-object material into one single texture material.",
    "blender": (3, 0, 0),
    "version": (0, 0, 2),
}


def unregister_keymaps():
    for km, kmi in addon_keymaps:
        km.keymap_items.remove(kmi)
    addon_keymaps.clear()

     
# Register Classes 
def register():
    for useClass in UsesClasses:
        bpy.utils.register_class(useClass)
    register_keymaps(addon_keymaps)

def unregister():
    unregister_keymaps()
    for useClass in UsesClasses:
        bpy.utils.unregister_class(useClass)

    
if __name__ == "__main__":
    unregister()


