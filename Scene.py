from Constants import *
from World import World
from Interact import BlockMarker
from Flat.Crosshair import Crosshair
from Meshes.Quad_Mesh import QuadMesh
from Flat.Hotbar import Hotbar
from Flat.Inventory import Inventory
from Flat.Hand import Hand
from Clouds import Clouds
from Meshes.Underwater_Mesh import UnderwaterMesh


class Scene:
    def __init__(self, app):
        self.app = app
        self.world = World(self.app)
        self.block_marker = BlockMarker(self.world.block_handler)
        self.quad_mesh = QuadMesh(self.app)
        self.hotbar = Hotbar(self.world.block_handler)
        self.inventory = Inventory(self.world.block_handler)
        self.underwater = UnderwaterMesh(self.app)
        self.clouds = Clouds(self.app)
        self.hand = Hand(self.world.block_handler)
        self.initpos = 0

    def update(self):

        player_pos = glm.ivec3(int(self.app.player.position.x),int(self.app.player.position.y), int(self.app.player.position.z))
        block_id = self.get_block_id(player_pos)
        # print("VOXEL:",block_id)
        # 水下后处理, 将画面填满水
        if block_id[0] == WATER:
            self.app.player.underwater = True
        else:
            self.app.player.underwater = False

        player_pos = glm.ivec3(int(self.app.player.position.x),int(self.app.player.position.y - 2), int(self.app.player.position.z))
        block_id = self.get_block_id(player_pos)
        if block_id[0] == VOID or block_id[0] >= 45:
            # print(int(self.app.player.position.y), WORLD_H * CHUNK_SIZE - 1)
            # 初始化位置在当前坐标的地上 而不是在空中
            # if int(self.app.player.position.y) == WORLD_H * CHUNK_SIZE and self.initpos == 0:
            #     while self.get_block_id(glm.ivec3(int(self.app.player.position.x),int(self.app.player.position.y - 2), int(self.app.player.position.z)))[0] == VOID:
            #         self.app.player.position.y = self.app.player.position.y - 1
            #     # self.app.player.position.x = self.app.player.position.x - 2
            #     self.initpos = 1
            # else:
            self.app.player.position.y = self.app.player.position.y - 0.002 * 0.98  # 伪重力
        if block_id[0] == WATER:
            self.app.player.position.y = self.app.player.position.y - 0.003
        # elif self.app.player.position.y != int(self.app.player.position.y+1):
        #     self.app.player.position.y = int(self.app.player.position.y+1)


        self.world.update()
        self.block_marker.update()
        self.hotbar.update()
        self.inventory.update()

        self.clouds.update()
        # self.hand.update()

    def render(self):
        self.world.render()
        self.clouds.render()
        self.block_marker.render()
        self.underwater.render(self.app.player)
        self.inventory.render()
        self.quad_mesh.render()
        self.hotbar.render()
        self.hand.render()


    def get_block_id(self, block_world_pos):
        cx, cy, cz = chunk_pos = block_world_pos / CHUNK_SIZE

        if 0 <= cx < WORLD_W and 0 <= cy < WORLD_H and 0 <= cz < WORLD_D:
            chunk_index = int(cx + WORLD_W * cz + WORLD_AREA * cy)
            chunk = self.world.chunks[chunk_index]

            lx, ly, lz = block_local_pos = block_world_pos - chunk_pos * CHUNK_SIZE

            block_index = lx + CHUNK_SIZE * lz + CHUNK_AREA * ly
            block_id = chunk.blocks[block_index]

            return block_id, block_index, block_local_pos, chunk
        return 0, 0, 0, 0


