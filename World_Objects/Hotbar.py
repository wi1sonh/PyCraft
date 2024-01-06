from Settings import *
from Meshes.Hotbar_Mesh import HotBarMesh
from Meshes.HotbarSelect_Mesh import Select
from Meshes.Hotbar_Icon_Mesh import HotBarIconMesh

class Hotbar:
    def __init__(self, voxel_handler):
        self.app = voxel_handler.app
        self.handler = voxel_handler
        self.hotbar_mesh = HotBarMesh(self.app)

        self.hotbarselect1 = Select(self.app)
        self.hotbarselect2 = Select(self.app, x=0.09)
        self.hotbarselect3 = Select(self.app, x=0.18)
        self.hotbarselect4 = Select(self.app, x=0.27)
        self.hotbarselect5 = Select(self.app, x=0.36)
        self.hotbarselect6 = Select(self.app, x=0.45)
        self.hotbarselect7 = Select(self.app, x=0.54)
        self.hotbarselect8 = Select(self.app, x=0.63)
        self.hotbarselect9 = Select(self.app, x=0.72)

        self.hotbar_icon1 = HotBarIconMesh(self.app)
        self.hotbar_icon2 = HotBarIconMesh(self.app, x=0.09)
        self.hotbar_icon3 = HotBarIconMesh(self.app, x=0.18)
        self.hotbar_icon4 = HotBarIconMesh(self.app, x=0.27)
        self.hotbar_icon5 = HotBarIconMesh(self.app, x=0.36)
        self.hotbar_icon6 = HotBarIconMesh(self.app, x=0.45)
        self.hotbar_icon7 = HotBarIconMesh(self.app, x=0.54)
        self.hotbar_icon8 = HotBarIconMesh(self.app, x=0.63)
        self.hotbar_icon9 = HotBarIconMesh(self.app, x=0.72)

        self.select = 1

        self.last1 = 1
        self.last2 = 2
        self.last3 = 3
        self.last4 = 4
        self.last5 = 5
        self.last6 = 6
        self.last7 = 7
        self.last8 = 8
        self.last9 = 9

    def update(self):
        pass

    def render(self):
        # print(self.handler.select)

        if self.select == 1:
            self.hotbar_icon1.program['voxel_id'] = self.handler.new_voxel_id
            self.last1 = self.handler.new_voxel_id
        else:
            self.hotbar_icon1.program['voxel_id'] = self.last1
        self.hotbar_icon1.render()
        if self.select == 1:
            self.hotbarselect1.render()


        if self.select == 2:
            self.hotbar_icon2.program['voxel_id'] = self.handler.new_voxel_id
            self.last2 = self.handler.new_voxel_id
        else:
            self.hotbar_icon2.program['voxel_id'] = self.last2
        self.hotbar_icon2.render()
        if self.select == 2:
            self.hotbarselect2.render()

        if self.select == 3:
            self.hotbar_icon3.program['voxel_id'] = self.handler.new_voxel_id
            self.last3 = self.handler.new_voxel_id
        else:
            self.hotbar_icon3.program['voxel_id'] = self.last3
        self.hotbar_icon3.render()
        if self.select == 3:
            self.hotbarselect3.render()

        if self.select == 4:
            self.hotbar_icon4.program['voxel_id'] = self.handler.new_voxel_id
            self.last4 = self.handler.new_voxel_id
        else:
            self.hotbar_icon4.program['voxel_id'] = self.last4
        self.hotbar_icon4.render()
        if self.select == 4:
            self.hotbarselect4.render()

        if self.select == 5:
            self.hotbar_icon5.program['voxel_id'] = self.handler.new_voxel_id
            self.last5 = self.handler.new_voxel_id
        else:
            self.hotbar_icon5.program['voxel_id'] = self.last5
        self.hotbar_icon5.render()
        if self.select == 5:
            self.hotbarselect5.render()

        if self.select == 6:
            self.hotbar_icon6.program['voxel_id'] = self.handler.new_voxel_id
            self.last6 = self.handler.new_voxel_id
        else:
            self.hotbar_icon6.program['voxel_id'] = self.last6
        self.hotbar_icon6.render()
        if self.select == 6:
            self.hotbarselect6.render()

        if self.select == 7:
            self.hotbar_icon7.program['voxel_id'] = self.handler.new_voxel_id
            self.last7 = self.handler.new_voxel_id
        else:
            self.hotbar_icon7.program['voxel_id'] = self.last7
        self.hotbar_icon7.render()
        if self.select == 7:
            self.hotbarselect7.render()

        if self.select == 8:
            self.hotbar_icon8.program['voxel_id'] = self.handler.new_voxel_id
            self.last8 = self.handler.new_voxel_id
        else:
            self.hotbar_icon8.program['voxel_id'] = self.last8
        self.hotbar_icon8.render()
        if self.select == 8:
            self.hotbarselect8.render()

        if self.select == 9:
            self.hotbar_icon9.program['voxel_id'] = self.handler.new_voxel_id
            self.last9 = self.handler.new_voxel_id
        else:
            self.hotbar_icon9.program['voxel_id'] = self.last9
        self.hotbar_icon9.render()
        if self.select == 9:
            self.hotbarselect9.render()

        self.hotbar_mesh.render()

