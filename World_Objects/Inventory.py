from Settings import *
from World_Objects.Icon import Icon
from Meshes.Inventory_Mesh import InventoryMesh

class Inventory:
    def __init__(self, voxel_handler):
        self.app = voxel_handler.app
        self.handler = voxel_handler
        self.block_icons = []
        self.inventory_mesh = InventoryMesh(self.app)
        self.init_icons()
        self.visible = False

    def init_icons(self):
        for i in range(1, NUM_BLOCKS + 1):
            self.block_icons.append(Icon(self.handler, voxel_id=i, vertical=0))

    def update(self):
        pass

    def set_uniform(self):
        pass

    def toggle_visible(self):
        self.visible = 1 - self.visible;

    def render(self):
        if self.visible:
            self.set_uniform()
            for icon in self.block_icons:
                icon.render()
            self.inventory_mesh.render()