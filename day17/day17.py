from typing import List

import numpy as np
from scipy import ndimage


def conway_3d(init: List[str], cycles=6) -> int:
    n_pad = cycles + 1  # extra layer to avoid checking index < 0 or index >= length
    m, n, z = len(init), len(init[0]), 1
    M = m + 2 * n_pad
    N = n + 2 * n_pad
    Z = z + 2 * n_pad

    space = [[[0] * Z for _ in range(N)] for _ in range(M)]

    # init
    k = n_pad
    for i, row in enumerate(init, n_pad):
        for j, v in enumerate(row, n_pad):
            space[i][j][k] = 1 if v == "#" else 0

    # 1 -> 0: 2
    # 1 -> 1: 1
    # 0 -> 0: 0
    # 0 -> 1: -1

    def count(i0, j0, k0):
        cnt = 0
        for i in range(i0 - 1, i0 + 2):
            for j in range(j0 - 1, j0 + 2):
                for k in range(k0 - 1, k0 + 2):
                    if i == i0 and j == j0 and k == k0:
                        continue

                    cnt += space[i][j][k] >= 1
                    if cnt > 3:
                        return cnt
        return cnt

    for i_cycle in range(1, cycles + 1):
        for i in range(n_pad - i_cycle, n_pad + m + i_cycle):
            for j in range(n_pad - i_cycle, n_pad + n + i_cycle):
                for k in range(n_pad - i_cycle, n_pad + 1 + i_cycle):
                    curr = space[i][j][k]
                    n_neighbor = count(i, j, k)
                    if curr == 1:
                        if n_neighbor < 2 or n_neighbor > 3:
                            space[i][j][k] = 2
                    else:
                        if n_neighbor == 3:
                            space[i][j][k] = -1

        for k in range(n_pad - i_cycle, n_pad + 1 + i_cycle):
            # print('z=', k - n_pad)
            for i in range(n_pad - i_cycle, n_pad + m + i_cycle):
                for j in range(n_pad - i_cycle, n_pad + n + i_cycle):
                    curr = space[i][j][k]
                    next_ = 1 if curr == -1 or curr == 1 else 0
                    space[i][j][k] = next_
                    # print(next_, ',', sep='', end='')
                # print()

    return sum(1 for x in space for y in x for z in y if z)


def conway_4d(init: List[str], cycles=6, dim=4) -> int:
    shape = np.array([len(init), len(init[0])])
    shape = np.pad(shape, (dim - shape.size, 0), constant_values=1)

    space = np.array([list(l) for l in init])
    space = (space == "#").astype(int)
    space = np.reshape(space, shape)
    space = np.pad(space, cycles)

    kernel = np.array([0])
    kernel = np.reshape(kernel, np.ones(dim, dtype=int))
    kernel = np.pad(kernel, 1, constant_values=1)

    for _ in range(cycles):
        count = ndimage.correlate(space, kernel, mode="constant", cval=0)

        c2 = count == 2
        c3 = count == 3
        c23 = np.logical_or(c2, c3)

        # 1 -> 1
        c11 = np.logical_and(space == 1, c23)
        # 0 -> 1
        c01 = np.logical_and(space == 0, c3)

        space = np.logical_or(c11, c01).astype(int)

    return np.count_nonzero(space == 1)


if __name__ == "__main__":

    # test
    notes = """
.#.
..#
###
"""
    lines = notes.strip().splitlines()
    ans1 = conway_3d(lines, cycles=6)
    ans12 = conway_4d(lines, cycles=6, dim=3)
    ans2 = conway_4d(lines, cycles=6, dim=4)
    assert ans1 == 112, f"wrong answer {ans1}"
    assert ans12 == 112, f"wrong answer {ans1}"
    assert ans2 == 848, f"wrong answer {ans2}"

    notes = """
###..#..
.#######
#####...
#..##.#.
###..##.
##...#..
..#...#.
.#....##
"""
    lines = notes.strip().splitlines()
    ans1 = conway_3d(lines, cycles=6)
    print("part 1 answer", ans1)

    ans2 = conway_4d(lines, cycles=6, dim=4)
    print("part 2 answer", ans2)
