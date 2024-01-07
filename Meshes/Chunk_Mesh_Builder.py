from Constants import * # 导入常量
from numba import uint8, njit
# 使用Numba的装饰器njit进行函数优化，提高性能

# 使用Numba进行编译优化
@njit
def get_ao(local_pos, world_pos, world_blocks, plane, block_id):
    x, y, z = local_pos  # 获取本地坐标
    wx, wy, wz = world_pos   # 获取世界坐标

    # 根据不同平面进行周围方块的判断
    # Y平面
    if plane == 'Y':

        a = is_void((x, y, z - 1), (wx, wy, wz - 1), world_blocks, block_id)
        b = is_void((x - 1, y, z -1),(wx -1, wy, wz - 1), world_blocks, block_id)
        c = is_void((x - 1, y, z), (wx - 1, wy, wz), world_blocks, block_id)
        d = is_void((x - 1, y, z + 1), (wx - 1, wy, wz + 1), world_blocks, block_id)
        e = is_void((x, y, z + 1), (wx, wy, wz + 1), world_blocks, block_id)
        f = is_void((x + 1, y, z + 1), (wx + 1, wy, wz + 1), world_blocks, block_id)
        g = is_void((x + 1, y, z), (wx + 1, wy, wz), world_blocks, block_id)
        h = is_void((x + 1, y, z - 1), (wx + 1, wy, wz - 1), world_blocks, block_id)

    if plane == 'X':
        a = is_void((x, y, z - 1), (wx, wy, wz - 1), world_blocks, block_id)
        b = is_void((x, y - 1, z - 1), (wx, wy - 1, wz - 1), world_blocks, block_id)
        c = is_void((x, y - 1, z), (wx, wy - 1, wz), world_blocks, block_id)
        d = is_void((x, y - 1, z + 1), (wx, wy - 1, wz + 1), world_blocks, block_id)
        e = is_void((x, y, z + 1), (wx, wy, wz + 1), world_blocks, block_id)
        f = is_void((x, y + 1, z + 1), (wx, wy + 1, wz + 1), world_blocks, block_id)
        g = is_void((x, y + 1, z), (wx, wy + 1, wz), world_blocks, block_id)
        h = is_void((x, y + 1, z - 1), (wx, wy + 1, wz - 1), world_blocks, block_id)

    if plane == 'Z':
        a = is_void((x - 1, y    , z), (wx - 1, wy    , wz), world_blocks, block_id)
        b = is_void((x - 1, y - 1, z), (wx - 1, wy - 1, wz), world_blocks, block_id)
        c = is_void((x    , y - 1, z), (wx    , wy - 1, wz), world_blocks, block_id)
        d = is_void((x + 1, y - 1, z), (wx + 1, wy - 1, wz), world_blocks, block_id)
        e = is_void((x + 1, y    , z), (wx + 1, wy    , wz), world_blocks, block_id)
        f = is_void((x + 1, y + 1, z), (wx + 1, wy + 1, wz), world_blocks, block_id)
        g = is_void((x    , y + 1, z), (wx    , wy + 1, wz), world_blocks, block_id)
        h = is_void((x - 1, y + 1, z), (wx - 1, wy + 1, wz), world_blocks, block_id)

    ao = (a + b + c), (g + h + a), (e + f + g), (c + d + e)
    return ao

# pack_data函数将坐标、方块ID等数据打包成一个整数以进行高效处理
@njit
def pack_data(x, y, z, block_id, face_id, ao_id, flip_id):
    # x: 6bit y: 6bit z:6bit block_id: 8bit face_id: 3bit ao_id: 2bit flip_id: 1bit
    # 将各数据位数存储
    a, b, c, d, e, f, g = x, y, z, block_id, face_id, ao_id, flip_id

    # 各数据位数长度
    b_bit, c_bit, d_bit, e_bit, f_bit, g_bit = 6, 6, 8, 3, 2, 1
    fg_bit = f_bit + g_bit
    efg_bit = e_bit +fg_bit
    defg_bit = d_bit + efg_bit
    cdefg_bit = c_bit + defg_bit
    bcdefg_bit = b_bit + cdefg_bit

    # 整合数据并返回
    packed_data = (
        a << bcdefg_bit |
        b << cdefg_bit |
        c << defg_bit |
        d << efg_bit |
        e << fg_bit |
        f << g_bit | g
    )
    return packed_data

# 用于计算给定世界空间中的块索引
@njit # 导入njit装饰器，用于编译NumPy函数以获得更高的性能
def get_chunk_index(world_block_pos):  # 接受一个包含世界空间中位置的三维元组world_block_pos
    wx, wy, wz = world_block_pos  # 使用元组分解将位置分解为wx、wy和wz

    # 使用整数除法将位置坐标映射到块索引的各个部分
    cx = wx // CHUNK_SIZE
    cy = wy // CHUNK_SIZE
    cz = wz // CHUNK_SIZE

    # 使用条件检查来确保映射后的索引在有效范围内。如果索引不在有效范围内，函数将返回-1。
    if not (0 <= cx < WORLD_W and 0 <= cy < WORLD_H and 0 <= cz < WORLD_D):
        return -1

    # 返回计算出的块索引
    index = cx + WORLD_W * cz + WORLD_AREA * cy
    return index

# 判断方块是否为空气或透明，用于渲染的逻辑中进行了多种类型方块的判断
@njit
def is_void(local_block_pos, world_block_pos, world_blocks, block_id):
   chunk_index = get_chunk_index(world_block_pos)
   if chunk_index == -1:
       return False
   chunk_blocks = world_blocks[chunk_index]

   x, y, z = local_block_pos
   block_index = x % CHUNK_SIZE + z % CHUNK_SIZE * CHUNK_SIZE + y % CHUNK_SIZE * CHUNK_AREA

    # Transparent Single Blocks
   if block_id != WATER and chunk_blocks[block_index] == WATER:
       return True
   if block_id != GLASS and chunk_blocks[block_index] == GLASS:
       return True

   if chunk_blocks[block_index] == LEAVES:
       return True
   if chunk_blocks[block_index] == RED_TULIP:
       return True
   if chunk_blocks[block_index] == WHITE_TULIP:
       return True
   if chunk_blocks[block_index] == PINK_TULIP:
       return True
   if chunk_blocks[block_index] == PEONY:
       return True
   if chunk_blocks[block_index] == ORANGE_TULIP:
       return True
   if chunk_blocks[block_index] == RED_MUSHROOM:
       return True
   if chunk_blocks[block_index] == DANDELION:
       return True
   if chunk_blocks[block_index] == SHORT_GRASS:
       return True
   if chunk_blocks[block_index] == TALL_GRASS:
       return True
   if chunk_blocks[block_index]:
       return False

   return True

# add_data函数将顶点数据添加到顶点数组中
@njit
def add_data(vertex_data, index, *vertices):
    for vertex in vertices:
        vertex_data[index] = vertex # 将顶点数据添加到顶点数组中
        index += 1
    return index

# build_chunk_mesh函数根据方块数据构建块的网格，用于渲染世界
@njit
def build_chunk_mesh(chunk_blocks, format_size, chunk_pos, world_blocks, transparent=False):
    vertex_data = np.empty(CHUNK_VOL * 18 * format_size, dtype='uint32')
    index = 0

    for x in range(CHUNK_SIZE):
        for y in range(CHUNK_SIZE):
            for z in range(CHUNK_SIZE):
                block_id = chunk_blocks[x + CHUNK_SIZE * z + CHUNK_AREA * y]

                if not block_id:   # 如果块为空，则跳过
                    continue

                if not transparent:
                     # 根据块ID判断是否为透明块，若是则跳过
                    if block_id == WATER:
                        continue
                    if block_id == LEAVES:
                        continue
                    if block_id == GLASS:
                        continue
                    if block_id == RED_TULIP:
                        continue
                    if block_id == WHITE_TULIP:
                        continue
                    if block_id == PINK_TULIP:
                        continue
                    if block_id == PEONY:
                        continue
                    if block_id == ORANGE_TULIP:
                        continue
                    if block_id == RED_MUSHROOM:
                        continue
                    if block_id == DANDELION:
                        continue
                    if block_id == SHORT_GRASS:
                        continue
                    if block_id == TALL_GRASS:
                        continue

                  # 根据块ID判断是否为可渲染的透明块，若不是则跳过
                if transparent:
                    can_render = False

                    if block_id == WATER:
                        can_render = True
                    if block_id == LEAVES:
                        can_render = True
                    if block_id == GLASS:
                        can_render = True
                    if block_id == RED_TULIP:
                        can_render = True
                    if block_id == WHITE_TULIP:
                        can_render = True
                    if block_id == PINK_TULIP:
                        can_render = True
                    if block_id == ORANGE_TULIP:
                        can_render = True
                    if block_id == PEONY:
                        can_render = True
                    if block_id == RED_MUSHROOM:
                        can_render = True
                    if block_id == SHORT_GRASS:
                        can_render = True
                    if block_id == TALL_GRASS:
                        can_render = True
                    if block_id == DANDELION:
                        can_render = True

                    if can_render != True:
                        continue

                # 方块的世界坐标
                cx, cy, cz = chunk_pos
                wx = x + cx * CHUNK_SIZE
                wz = z + cz * CHUNK_SIZE
                wy = y + cy * CHUNK_SIZE

                # billboard
                if RED_TULIP <= block_id <= TALL_GRASS:
                    # diagonal 1
                    ao = get_ao((x + 1, y, z), (wx + 1, wy, wz), world_blocks, 'X', block_id)
                    flip_id = ao[1] + ao[3] > ao[0] + ao[2]

                    v0 = pack_data(x, y    , z    , block_id, 2, ao[0], flip_id)
                    v1 = pack_data(x, y + 1, z    , block_id, 2, ao[1], flip_id)
                    v2 = pack_data(x + 1, y + 1, z + 1, block_id, 2, ao[2], flip_id)
                    v3 = pack_data(x + 1, y    , z + 1, block_id, 2, ao[3], flip_id)

                    if flip_id:
                        index = add_data(vertex_data, index, v3, v0, v1, v3, v1, v2)
                    else:
                        index = add_data(vertex_data, index, v0, v1, v2, v0, v2, v3)

                    # diagonal 2
                    ao = get_ao((x + 1, y, z), (wx + 1, wy, wz), world_blocks, 'X', block_id)
                    flip_id = ao[1] + ao[3] > ao[0] + ao[2]

                    v0 = pack_data(x + 1, y    , z + 1    , block_id, 2, ao[0], flip_id)
                    v1 = pack_data(x + 1, y + 1, z + 1    , block_id, 2, ao[1], flip_id)
                    v2 = pack_data(x, y + 1, z, block_id, 2, ao[2], flip_id)
                    v3 = pack_data(x, y    , z, block_id, 2, ao[3], flip_id)

                    if flip_id:
                        index = add_data(vertex_data, index, v3, v0, v1, v3, v1, v2)
                    else:
                        index = add_data(vertex_data, index, v0, v1, v2, v0, v2, v3)

                    # diagonal 3
                    ao = get_ao((x + 1, y, z), (wx + 1, wy, wz), world_blocks, 'X', block_id)
                    flip_id = ao[1] + ao[3] > ao[0] + ao[2]

                    v0 = pack_data(x + 1, y    , z    , block_id, 2, ao[0], flip_id)
                    v1 = pack_data(x + 1, y + 1, z    , block_id, 2, ao[1], flip_id)
                    v2 = pack_data(x, y + 1, z + 1, block_id, 2, ao[2], flip_id)
                    v3 = pack_data(x, y    , z + 1, block_id, 2, ao[3], flip_id)

                    if flip_id:
                        index = add_data(vertex_data, index, v3, v0, v1, v3, v1, v2)
                    else:
                        index = add_data(vertex_data, index, v0, v1, v2, v0, v2, v3)

                    # diagonal 4
                    ao = get_ao((x + 1, y, z), (wx + 1, wy, wz), world_blocks, 'X', block_id)
                    flip_id = ao[1] + ao[3] > ao[0] + ao[2]

                    v0 = pack_data(x, y, z + 1    , block_id, 2, ao[0], flip_id)
                    v1 = pack_data(x, y + 1, z + 1   , block_id, 2, ao[1], flip_id)
                    v2 = pack_data(x + 1, y + 1, z, block_id, 2, ao[2], flip_id)
                    v3 = pack_data(x + 1,y, z, block_id, 2, ao[3], flip_id)

                    if flip_id:
                        index = add_data(vertex_data, index, v3, v0, v1, v3, v1, v2)
                    else:
                        index = add_data(vertex_data, index, v0, v1, v2, v0, v2, v3)

                    continue

                # 顶面
                if is_void((x, y + 1, z), (wx, wy + 1, wz), world_blocks, block_id):
                    # get ao values
                    ao = get_ao((x, y + 1, z), (wx, wy + 1, wz), world_blocks,'Y', block_id)
                    flip_id = ao[1] + ao[3] > ao[0] + ao[2]

                    # format: x, y, z, block_id, face_id, ao_id
                    v0 = pack_data(x    , y + 1, z    , block_id, 0, ao[0], flip_id)
                    v1 = pack_data(x + 1, y + 1, z    , block_id, 0, ao[1], flip_id)
                    v2 = pack_data(x + 1, y + 1, z + 1, block_id, 0, ao[2], flip_id)
                    v3 = pack_data(x    , y + 1, z + 1, block_id, 0, ao[3], flip_id)

                    if flip_id:
                        index = add_data(vertex_data, index, v1, v0, v3, v1, v3, v2)
                    else:
                        index = add_data(vertex_data, index, v0, v3, v2, v0, v2, v1)

                # 底面
                if is_void((x, y - 1, z), (wx, wy - 1, wz), world_blocks, block_id):
                    ao = get_ao((x, y - 1, z), (wx, wy - 1, wz), world_blocks,'Y', block_id)
                    flip_id = ao[1] + ao[3] > ao[0] + ao[2]

                    v0 = pack_data(x    , y, z    , block_id, 1, ao[0], flip_id)
                    v1 = pack_data(x + 1, y, z    , block_id, 1, ao[1], flip_id)
                    v2 = pack_data(x + 1, y, z + 1, block_id, 1, ao[2], flip_id)
                    v3 = pack_data(x    , y, z + 1, block_id, 1, ao[3], flip_id)

                    if flip_id:
                        index = add_data(vertex_data, index, v1, v3, v0, v1, v2, v3)
                    else:
                        index = add_data(vertex_data, index, v0, v2, v3, v0, v1, v2)

                # 右面
                if is_void((x + 1, y, z), (wx + 1, wy, wz), world_blocks, block_id):
                    ao = get_ao((x + 1, y, z), (wx + 1, wy, wz), world_blocks, 'X', block_id)
                    flip_id = ao[1] + ao[3] > ao[0] + ao[2]

                    v0 = pack_data(x + 1, y    , z    , block_id, 2, ao[0], flip_id)
                    v1 = pack_data(x + 1, y + 1, z    , block_id, 2, ao[1], flip_id)
                    v2 = pack_data(x + 1, y + 1, z + 1, block_id, 2, ao[2], flip_id)
                    v3 = pack_data(x + 1, y    , z + 1, block_id, 2, ao[3], flip_id)

                    if flip_id:
                        index = add_data(vertex_data, index, v3, v0, v1, v3, v1, v2)
                    else:
                        index = add_data(vertex_data, index, v0, v1, v2, v0, v2, v3)

                # 左面
                if is_void((x - 1, y, z), (wx - 1, wy, wz), world_blocks, block_id):
                    ao = get_ao((x - 1, y, z), (wx - 1, wy, wz), world_blocks, 'X', block_id)
                    flip_id = ao[1] + ao[3] > ao[0] + ao[2]

                    v0 = pack_data(x, y    , z    , block_id, 3, ao[0], flip_id)
                    v1 = pack_data(x, y + 1, z    , block_id, 3, ao[1], flip_id)
                    v2 = pack_data(x, y + 1, z + 1, block_id, 3, ao[2], flip_id)
                    v3 = pack_data(x, y    , z + 1, block_id, 3, ao[3], flip_id)

                    if flip_id:
                        index = add_data(vertex_data, index, v3, v1, v0, v3, v2, v1)
                    else:
                        index = add_data(vertex_data, index, v0, v2, v1, v0, v3, v2)

                # 后面
                if is_void((x, y, z - 1), (wx, wy, wz - 1), world_blocks, block_id):
                    ao = get_ao((x, y, z - 1), (wx, wy, wz - 1), world_blocks, 'Z', block_id)
                    flip_id = ao[1] + ao[3] > ao[0] + ao[2]

                    v0 = pack_data(x,     y,     z, block_id, 4, ao[0], flip_id)
                    v1 = pack_data(x,     y + 1, z, block_id, 4, ao[1], flip_id)
                    v2 = pack_data(x + 1, y + 1, z, block_id, 4, ao[2], flip_id)
                    v3 = pack_data(x + 1, y,     z, block_id, 4, ao[3], flip_id)

                    if flip_id:
                        index = add_data(vertex_data, index, v3, v0, v1, v3, v1, v2)
                    else:
                        index = add_data(vertex_data, index, v0, v1, v2, v0, v2, v3)

                # 前面
                if is_void((x, y, z + 1), (wx, wy, wz + 1), world_blocks, block_id):
                    ao = get_ao((x, y, z + 1), (wx, wy, wz + 1), world_blocks, 'Z', block_id)
                    flip_id = ao[1] + ao[3] > ao[0] + ao[2]

                    v0 = pack_data(x    , y    , z + 1, block_id, 5, ao[0], flip_id)
                    v1 = pack_data(x    , y + 1, z + 1, block_id, 5, ao[1], flip_id)
                    v2 = pack_data(x + 1, y + 1, z + 1, block_id, 5, ao[2], flip_id)
                    v3 = pack_data(x + 1, y    , z + 1, block_id, 5, ao[3], flip_id)

                    if flip_id:
                        index = add_data(vertex_data, index, v3, v1, v0, v3, v2, v1)
                    else:
                        index = add_data(vertex_data, index, v0, v2, v1, v0, v3, v2)

    return vertex_data[:index + 1]  # 返回构建好的顶点数据数组
