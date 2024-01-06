from Noise import noise2, noise3
from Settings import *
from numba import njit
from random import random


@njit
def get_height(x, z):
    # island mask
    island = 1 / (pow(0.0025 * math.hypot(x - CENTER_XZ, z - CENTER_XZ), 20) + 0.0001)
    island = min(island, 1)

    # amplitude
    a1 = CENTER_Y
    a2, a4, a8 = a1 * 0.5, a1 * 0.25, a1 * 0.125

    # frequency
    f1 = 0.005
    f2, f4, f8 = f1 * 2, f1 *4, f1 * 8

    if noise2(0.1 * x, 0.1 * z) < 0:
        a1 /= 1.07

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
def set_voxel_id(voxels, x, y, z, wx, wy, wz, world_height):
    voxel_id = 0

    if wy < world_height - 1:
        # create caves
        if (noise3(wx * 0.09, wy * 0.09, wz * 0.09) > 0 and noise2(wx * 0.1, wz * 0.1) * 3 + 3 < wy < world_height - 10):
            voxel_id = 0
        else:
            voxel_id = STONE
    elif wy == world_height - 1:
        rng = int(7 * random())
        ry = wy - rng
        if SNOW_LVL <= ry < world_height:
            voxel_id = SNOWY_GRASS

        elif STONE_LVL <= ry < SNOW_LVL:
            voxel_id = STONE

        elif DIRT_LVL <= ry < STONE_LVL:
            voxel_id = DIRT

        elif GRASS_LVL <= ry < DIRT_LVL:
            voxel_id = GRASS

        else:
            voxel_id = SAND

    # setting ID
    voxels[get_index(x, y, z)] = voxel_id

    # place tree
    if wy < DIRT_LVL:
        place_tree(voxels, x, y, z, voxel_id)

    if wy < DIRT_LVL:
        place_pumpkins(voxels, x, y, z, voxel_id)

    if wy < DIRT_LVL:
        place_melons(voxels, x, y, z, voxel_id)

    if wy < DIRT_LVL:
        place_flowers(voxels, x, y, z, voxel_id)

    if wy < DIRT_LVL:
        place_shrubs(voxels, x, y, z, voxel_id)

    # place water
    if wy < WATER_LVL:
        water_height = WATER_LVL - wy
        for iy in range(1, water_height):
            voxels[get_index(x, y + iy, z)] = WATER

@njit
def place_pumpkins(voxels, x, y, z, voxel_id):
    rnd = random()
    if voxel_id != GRASS or rnd > PUMPKIN_PROBABILITY:
        return None
    if voxels[get_index(x, y + 1, z)] != VOID:
        return None

    # dirt under the tree
    voxels[get_index(x, y, z)] = DIRT

    # pumpkin
    voxels[get_index(x, y + 1, z)] = PUMPKIN

@njit
def place_melons(voxels, x, y, z, voxel_id):
    rnd = random()
    if voxel_id != GRASS or rnd > PUMPKIN_PROBABILITY:
        return None
    if voxels[get_index(x, y + 1, z)] != VOID:
        return None

    # dirt under the tree
    voxels[get_index(x, y, z)] = DIRT

    # melon
    voxels[get_index(x, y + 1, z)] = MELON

@njit
def place_shrubs(voxels, x, y, z, voxel_id):
    rnd = random()
    if voxel_id != GRASS or rnd > SHRUB_PROBABILITY:
        return None
    if voxels[get_index(x, y + 1, z)] != VOID:
        return None

    # dirt under the tree
    voxels[get_index(x, y, z)] = GRASS

    grass_type = SHORT_GRASS
    rnd = math.ceil(random() * 10)
    if rnd < 4:
        grass_type = TALL_GRASS

    # grass
    voxels[get_index(x, y + 1, z)] = grass_type

@njit
def place_flowers(voxels, x, y, z, voxel_id):
    rnd = random()
    if voxel_id != GRASS or rnd > FLOWER_PROBABILITY:
        return None
    if voxels[get_index(x, y + 1, z)] != VOID:
        return None

    # dirt under the tree
    voxels[get_index(x, y, z)] = GRASS

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

    # flower
    voxels[get_index(x, y + 1, z)] = flower_type


@njit
def place_tree(voxels, x, y, z, voxel_id):
    rnd = random()
    if voxel_id != GRASS or rnd > TREE_PROBABILITY:
        return None
    if y + TREE_HEIGHT >= CHUNK_SIZE:
        return None
    if x - TREE_H_WIDTH < 0 or x + TREE_H_WIDTH >= CHUNK_SIZE:
        return None
    if z - TREE_H_WIDTH < 0 or z + TREE_H_WIDTH >= CHUNK_SIZE:
        return None

    # dirt under the tree
    voxels[get_index(x, y, z)] = DIRT

    # leaves
    m = 0
    for n, iy in enumerate(range(TREE_H_HEIGHT, TREE_HEIGHT - 1)):
        k = iy % 2
        rng = int(random() * 2)
        for ix in range(-TREE_H_WIDTH + m, TREE_H_WIDTH - m * rng):
            for iz in range(-TREE_H_WIDTH + m * rng, TREE_H_WIDTH - m):
                if (ix + iz) % 4:
                    voxels[get_index(x + ix + k, y + iy, z + iz + k)] = LEAVES
        m += 1 if n > 0 else 3 if n > 1 else 0

    # tree trunk
    tree_type = random()
    for iy in range(1, TREE_HEIGHT - 2):
        if tree_type > 0.5:
            voxels[get_index(x, y + iy, z)] = OAK_WOOD
        elif tree_type <= 0.5:
            voxels[get_index(x, y + iy, z)] = BIRCH_WOOD

    # top
    voxels[get_index(x, y + TREE_HEIGHT - 2, z)] = LEAVES
