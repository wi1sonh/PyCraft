from Noise import noise2, noise3
from Constants import *
from numba import njit
from random import random
from random import randint

# 树生成参数
TREE_PROBABILITY = 0.02
TREE_WIDTH, TREE_HEIGHT = 4, 8
TREE_H_WIDTH, TREE_H_HEIGHT = TREE_WIDTH // 2, TREE_HEIGHT // 2

# 地形生成概率
PUMPKIN_PROBABILITY  = 0.002
FLOWER_PROBABILITY   = 0.05
MUSHROOM_PROBABILITY = 0.01
SHRUB_PROBABILITY    = 0.3


@njit
def get_height(x, z):
    # 计算岛屿掩膜
    island = 1 / (pow(0.0025 * math.hypot(x - CENTER_XZ, z - CENTER_XZ), 20) + 0.0001)
    island = min(island, 1)

    # 振幅
    a1, a2, a4, a8 = CENTER_Y, CENTER_Y * 0.5, CENTER_Y * 0.25, CENTER_Y * 0.125

    # 频率
    f1, f2, f4, f8 = 0.005, 0.005 * 2, 0.005 *4, 0.005 * 8

    if noise2(0.1 * x, 0.1 * z) < 0:
        a1 /= 1.07

    # 通过振幅和频率生成地形，使得地形有起伏
    height = 0
    height += noise2(x * f1, z * f1) * a1 + a1
    height += noise2(x * f2, z * f2) * a2 - a2
    height += noise2(x * f4, z * f4) * a4 + a4
    height += noise2(x * f8, z * f8) * a8 - a8

    height = max(height, 1)
    height *= island

    return int(height)

@njit
def get_index(x, y, z):
    return x + CHUNK_SIZE * z + CHUNK_AREA * y

@njit
def set_block_id(blocks, x, y, z, wx, wy, wz, world_height):
    block_id = 0

    if wy < world_height - 1:
        # 创建洞穴
        if (noise3(wx * 0.09, wy * 0.09, wz * 0.09) > 0 and noise2(wx * 0.1, wz * 0.1) * 3 + 3 < wy < world_height - 10):
            block_id = 0
        else:
            block_id = STONE
    elif wy == world_height - 1:
        rng = int(7 * random())
        ry = wy - rng
        if SNOW_LVL <= ry < world_height:
            block_id = SNOWY_GRASS

        elif STONE_LVL <= ry < SNOW_LVL:
            block_id = STONE

        elif DIRT_LVL <= ry < STONE_LVL:
            block_id = DIRT

        elif GRASS_LVL <= ry < DIRT_LVL:
            block_id = GRASS

        else:
            block_id = SAND

    blocks[get_index(x, y, z)] = block_id

    # 放置树
    if wy < DIRT_LVL:
        place_tree(blocks, x, y, z, block_id)

    if wy < DIRT_LVL:
        place_pumpkins(blocks, x, y, z, block_id)

    if wy < DIRT_LVL:
        place_melons(blocks, x, y, z, block_id)

    if wy < DIRT_LVL:
        place_flowers(blocks, x, y, z, block_id)

    if wy < DIRT_LVL:
        place_shrubs(blocks, x, y, z, block_id)

    # 放置水
    if wy < SEA_LVL:
        water_height = SEA_LVL - wy
        for iy in range(1, water_height):
            blocks[get_index(x, y + iy, z)] = WATER

@njit
def place_pumpkins(blocks, x, y, z, block_id):
    rnd = random()
    if block_id != GRASS or rnd > PUMPKIN_PROBABILITY:
        return None
    if blocks[get_index(x, y + 1, z)] != VOID:
        return None

    blocks[get_index(x, y, z)] = DIRT

    # 南瓜
    blocks[get_index(x, y + 1, z)] = PUMPKIN

@njit
def place_melons(blocks, x, y, z, block_id):
    rnd = random()
    if block_id != GRASS or rnd > PUMPKIN_PROBABILITY:
        return None
    if blocks[get_index(x, y + 1, z)] != VOID:
        return None

    blocks[get_index(x, y, z)] = DIRT

    # 西瓜
    blocks[get_index(x, y + 1, z)] = MELON

@njit
def place_shrubs(blocks, x, y, z, block_id):
    rnd = random()
    if block_id != GRASS or rnd > SHRUB_PROBABILITY:
        return None
    if blocks[get_index(x, y + 1, z)] != VOID:
        return None

    blocks[get_index(x, y, z)] = GRASS

    grass_type = SHORT_GRASS
    rnd = math.ceil(random() * 10)
    if rnd < 4:
        grass_type = TALL_GRASS

    # 草
    blocks[get_index(x, y + 1, z)] = grass_type

@njit
def place_flowers(blocks, x, y, z, block_id):
    rnd = random()
    if block_id != GRASS or rnd > FLOWER_PROBABILITY:
        return None
    if blocks[get_index(x, y + 1, z)] != VOID:
        return None

    blocks[get_index(x, y, z)] = GRASS

    flower_type = RED_TULIP
    rnd = math.ceil(random() * 7);
    if rnd == 1:
        flower_type = RED_TULIP
    if rnd == 2:
        flower_type = WHITE_TULIP
    if rnd == 3:
        flower_type = PINK_TULIP
    if rnd == 4:
        flower_type = ORANGE_TULIP
    if rnd == 5:
        flower_type = PEONY
    if rnd == 6:
        flower_type = DANDELION
    if rnd == 7:
        flower_type = RED_MUSHROOM

    # 花
    blocks[get_index(x, y + 1, z)] = flower_type


@njit
def place_tree(blocks, x, y, z, block_id):
    rnd = random()
    if block_id != GRASS or rnd > TREE_PROBABILITY:
        return None
    if y + TREE_HEIGHT >= CHUNK_SIZE:
        return None
    if x - TREE_H_WIDTH < 0 or x + TREE_H_WIDTH >= CHUNK_SIZE:
        return None
    if z - TREE_H_WIDTH < 0 or z + TREE_H_WIDTH >= CHUNK_SIZE:
        return None

    # 树下面放土
    blocks[get_index(x, y, z)] = DIRT

    # 叶子
    tree_height=TREE_HEIGHT-randint(0,2)
    tree_h_height=tree_height//2
    m = 0
    for n, iy in enumerate(range(tree_h_height, tree_height - 1)):
        k = iy % 2
        rng = int(random() * 2)
        for ix in range(-TREE_H_WIDTH + m, TREE_H_WIDTH - m * rng):
            for iz in range(-TREE_H_WIDTH + m * rng, TREE_H_WIDTH - m):
                if (ix + iz) % 4:
                    blocks[get_index(x + ix + k, y + iy, z + iz + k)] = LEAVES
        m += 1 if n > 0 else 3 if n > 1 else 0

    # 树干
    tree_type = random()
    for iy in range(1, tree_height - 2):
        if tree_type > 0.5:
            blocks[get_index(x, y + iy, z)] = OAK_WOOD
        elif tree_type <= 0.5:
            blocks[get_index(x, y + iy, z)] = BIRCH_WOOD

    # top
    blocks[get_index(x, y + tree_height - 2, z)] = LEAVES
