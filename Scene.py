from Settings import *
from World import World
from World_Objects.Voxel_Marker import VoxelMarker
from World_Objects.Crosshair import Crosshair
from Meshes.Quad_Mesh import QuadMesh
from World_Objects.Hotbar import Hotbar
from World_Objects.Inventory import Inventory
from World_Objects.Hand import Hand
from World_Objects.Clouds import Clouds
from Meshes.Underwater_Mesh import UnderwaterMesh


class Scene:
    def __init__(self, app):
        self.app = app
        self.world = World(self.app)
        self.voxel_marker = VoxelMarker(self.world.voxel_handler)
        self.quad_mesh = QuadMesh(self.app)
        self.hotbar = Hotbar(self.world.voxel_handler)
        self.inventory = Inventory(self.world.voxel_handler)
        self.underwater = UnderwaterMesh(self.app)
        self.clouds = Clouds(self.app)
        self.hand = Hand(self.world.voxel_handler)
        self.initpos = 0

    def update(self):

        player_pos = glm.ivec3(int(self.app.player.position.x),int(self.app.player.position.y), int(self.app.player.position.z))
        voxel_id = self.get_voxel_id(player_pos)
        # print("VOXEL:",voxel_id)
        # 水下后处理, 将画面填满水
        if voxel_id[0] == WATER:
            self.app.player.underwater = True
        else:
            self.app.player.underwater = False

        player_pos = glm.ivec3(int(self.app.player.position.x),int(self.app.player.position.y - 2), int(self.app.player.position.z))
        voxel_id = self.get_voxel_id(player_pos)
        if voxel_id[0] == VOID or voxel_id[0] >= 45:
            # print(int(self.app.player.position.y), WORLD_H * CHUNK_SIZE - 1)
            # 初始化位置在当前坐标的地上 而不是在空中
            if int(self.app.player.position.y) == WORLD_H * CHUNK_SIZE and self.initpos == 0:
                while self.get_voxel_id(glm.ivec3(int(self.app.player.position.x),int(self.app.player.position.y - 2), int(self.app.player.position.z)))[0] == VOID:
                    self.app.player.position.y = self.app.player.position.y - 1
                # self.app.player.position.x = self.app.player.position.x - 2
                self.initpos = 1
            else:
                self.app.player.position.y = self.app.player.position.y - 0.02 * 0.98  # 伪重力
        if voxel_id[0] == WATER:
            self.app.player.position.y = self.app.player.position.y - 0.003
        # elif self.app.player.position.y != int(self.app.player.position.y+1):
        #     self.app.player.position.y = int(self.app.player.position.y+1)


        self.world.update()
        self.voxel_marker.update()
        self.hotbar.update()
        self.inventory.update()

        self.clouds.update()
        # self.hand.update()

    def render(self):
        self.world.render()
        self.clouds.render()
        self.voxel_marker.render()
        self.underwater.render(self.app.player)
        self.inventory.render()
        self.quad_mesh.render()
        self.hotbar.render()
        self.hand.render()


    def get_voxel_id(self, voxel_world_pos):
        cx, cy, cz = chunk_pos = voxel_world_pos / CHUNK_SIZE

        if 0 <= cx < WORLD_W and 0 <= cy < WORLD_H and 0 <= cz < WORLD_D:
            chunk_index = int(cx + WORLD_W * cz + WORLD_AREA * cy)
            chunk = self.world.chunks[chunk_index]

            lx, ly, lz = voxel_local_pos = voxel_world_pos - chunk_pos * CHUNK_SIZE

            voxel_index = lx + CHUNK_SIZE * lz + CHUNK_AREA * ly
            voxel_id = chunk.voxels[voxel_index]

            return voxel_id, voxel_index, voxel_local_pos, chunk
        return 0, 0, 0, 0


