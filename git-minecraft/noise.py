from opensimplex.internals import _noise2, _noise3, _init
from settings import SEED
from numba import njit

perm, perm_grad_index3 = _init(seed=SEED)

@njit(cache=True)  # 提高代码执行速度
def noise2(x, y):
    return _noise2(x, y, perm)


@njit(cache=True)  # 提高代码执行速度
def noise3(x, y, z):
    return _noise3(x, y, z, perm, perm_grad_index3)
