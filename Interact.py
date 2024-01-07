from Constants import *
from Meshes.Chunk_Mesh_Builder import get_chunk_index
from Meshes.Cube_Mesh import CubeMesh

# 有限射线长度 (Ray Casting)
MAX_RAY_DIST = 6

def get_block(chunks, block_world_pos):
    chunk_x, chunk_y, chunk_z = chunk_pos = block_world_pos / CHUNK_SIZE

    if 0 <= chunk_x < WORLD_W and 0 <= chunk_y < WORLD_H and 0 <= chunk_z < WORLD_D:
        chunk_index = chunk_x + WORLD_W * chunk_z + WORLD_AREA * chunk_y
        chunk = chunks[chunk_index]

        local_x, local_y, local_z = block_local_pos = block_world_pos - chunk_pos * CHUNK_SIZE

        block_index = local_x + CHUNK_SIZE * local_z + CHUNK_AREA * local_y
        block_id = chunk.blocks[block_index]

        return block_id, block_index, block_local_pos, chunk
    
    return 0, 0, 0, 0


class BlockHandler:
    def __init__(self, world):
        self.app = world.app  # Engine
        self.chunks = world.chunks

        # 目标方块
        self.chunk = None
        self.block_id = None
        self.block_index = None
        self.block_local_pos = None
        self.block_world_pos = None
        self.block_normal = None
        self.new_block_id = DIRT  # 默认

    # 算法主体：从起点到终点逐步前进一个方块，直到与方块相交
    def ray_cast(self):

        def init_ray(cord2, cord1):
            sign = glm.sign(cord2 - cord1)
            delta = min(sign / (cord2 - cord1), 10000000.0) if sign != 0 else 10000000.0
            max = delta * (1.0 - glm.fract(cord1)) if sign > 0 else delta * glm.fract(cord1)
            return sign, delta, max

        # start
        x1, y1, z1 = self.app.player.position
        # end
        x2, y2, z2 = self.app.player.position + self.app.player.forward * MAX_RAY_DIST

        current_block_pos = glm.ivec3(x1, y1, z1)
        self.block_id = 0
        self.block_normal = glm.ivec3(0)
        step_dir = -1

        sign_x, delta_x, max_x = init_ray(x2, x1)
        sign_y, delta_y, max_y = init_ray(y2, y1)
        sign_z, delta_z, max_z = init_ray(z2, z1)

        while not (max_x > 1.0 and max_y > 1.0 and max_z > 1.0):

            result = get_block(self.chunks, current_block_pos)
            if result[0]:
                self.block_id, self.block_index, self.block_local_pos, self.chunk = result
                self.block_world_pos = current_block_pos

                if step_dir == 0:
                    self.block_normal.x = -sign_x
                elif step_dir == 1:
                    self.block_normal.y = -sign_y
                else:
                    self.block_normal.z = -sign_z
                return True

            if max_x < max_y:
                if max_x < max_z:
                    current_block_pos.x += sign_x
                    max_x += delta_x
                    step_dir = 0
                else:
                    current_block_pos.z += sign_z
                    max_z += delta_z
                    step_dir = 2
            else:
                if max_y < max_z:
                    current_block_pos.y += sign_y
                    max_y += delta_y
                    step_dir = 1
                else:
                    current_block_pos.z += sign_z
                    max_z += delta_z
                    step_dir = 2
        return False
    
    # 放置
    def add_block(self, pg, sounds):
        if self.block_id:
            # 取法线方向的相邻方块
            result = get_block(self.chunks, self.block_world_pos + self.block_normal)

            # 是空方块时进行
            if not result[0]:
                _, block_index, _, chunk = result
                chunk.blocks[block_index] = self.new_block_id
                chunk.mesh.rebuild()
                chunk.transparent_mesh.rebuild()

                sound = self.get_sound(self.new_block_id, sounds)
                pg.mixer.Sound.play(sound)

                if chunk.is_empty:
                    chunk.is_empty = False

    # 破坏
    def remove_block(self, pg, sounds):
        if self.block_index == None:
            return
        if self.chunk.blocks[self.block_index] == 0 or self.chunk.blocks[self.block_index] == WATER:
            return
        
        sound = self.get_sound(self.chunk.blocks[self.block_index], sounds)
        pg.mixer.Sound.play(sound)

        block = get_block(self.chunks, self.block_world_pos)
        self.new_block_id = block[0]
        self.chunk.blocks[self.block_index] = 0
        self.chunk.mesh.rebuild()
        self.chunk.transparent_mesh.rebuild()
        self.rebuild_adjacent_chunks()
        self.block_index = None

    def set_block_id(self, id):
        self.new_block_id = id;
        if self.new_block_id < 1:
            self.new_block_id = NUM_BLOCKS
        if self.new_block_id > NUM_BLOCKS:
            self.new_block_id = 1

    def update(self):
        self.ray_cast()

    def get_sound(self, block_id, sounds):
        if RED_TULIP <= block_id <= TALL_GRASS:
            return sounds["Grass"]
        return sounds["Block"]

    def rebuild_adj_chunk(self, adj_block_pos):
        index = get_chunk_index(adj_block_pos)
        if index != -1:
            self.chunks[index].mesh.rebuild()
            self.chunks[index].transparent_mesh.rebuild()

    def rebuild_adjacent_chunks(self):
        lx, ly, lz = self.block_local_pos
        wx, wy, wz = self.block_world_pos

        if lx == 0:
            self.rebuild_adj_chunk((wx - 1, wy, wz))
        elif lx == CHUNK_SIZE - 1:
            self.rebuild_adj_chunk((wx + 1, wy, wz))

        if ly == 0:
            self.rebuild_adj_chunk((wx, wy - 1, wz))
        elif ly == CHUNK_SIZE - 1:
            self.rebuild_adj_chunk((wx, wy + 1, wz))

        if lz == 0:
            self.rebuild_adj_chunk((wx, wy, wz - 1))
        elif lz == CHUNK_SIZE - 1:
            self.rebuild_adj_chunk((wx, wy, wz + 1))


class BlockMarker:
    def __init__(self, block_handler):
        self.app = block_handler.app
        self.handler = block_handler
        self.position = glm.vec3(0)
        self.m_model = self.get_model_matrix()
        self.mesh = CubeMesh(self.app)

    def update(self):
        if self.handler.block_id:
            self.position = self.handler.block_world_pos

    def set_uniform(self):
        self.mesh.program['m_model'].write(self.get_model_matrix())

    def get_model_matrix(self):
        m_model = glm.translate(glm.mat4(), glm.vec3(self.position))
        return m_model

    def render(self):
        if self.handler.block_id:
            self.set_uniform()
            self.mesh.render()