def draw_bakeToButton(self, context):
    '''Bake into Texture and Combine Meshes into Ones Button'''
    layout = self.layout
    layout.operator("object.create_copy_in_new_collection", text="Bake Into Texture")
