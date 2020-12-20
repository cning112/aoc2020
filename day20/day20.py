from functools import lru_cache
from functools import lru_cache
from typing import List, Dict, Optional, Tuple

import numpy as np
from scipy import ndimage

Tile = np.ndarray


def load(filename: str) -> Dict[int, Tile]:
    ans = {}
    buff = []
    with open(filename) as f:
        for line in f:
            line = line.strip()
            if line.startswith("Tile"):
                id_ = int(line[5:-1])
            elif not line:
                ans[id_] = np.array(buff)
                buff = []
            else:
                buff.append(list(line))

    if buff:
        ans[id_] = np.array(buff)
    return ans


def variants(tile: Tile) -> List[Tile]:
    return [np.rot90(x, k) for x in [tile, np.fliplr(tile)] for k in range(4)]


def dfs(tiles: Dict[int, Tile]) -> List[List[Tuple[int, Tile]]]:
    M = N = int(len(tiles) ** 0.5)

    @lru_cache(None)
    def _variants(tid):
        return variants(tiles[tid])

    in_grid = set()
    grid: List[List[Optional[Tuple[int, Tile]]]] = [[None] * N for _ in range(M)]

    def dfs_(idx):
        if idx == len(tiles):
            return True

        i0, j0 = divmod(idx, N)

        for tid in tiles.keys() - in_grid:
            in_grid.add(tid)

            top = grid[i0 - 1][j0][1][-1, :] if i0 > 0 else None
            left = grid[i0][j0 - 1][1][:, -1] if j0 > 0 else None

            for variant in _variants(tid):
                # check top
                if top is not None and not np.array_equal(top, variant[0, :]):
                    continue

                # check left
                if left is not None and not np.array_equal(left, variant[:, 0]):
                    continue

                grid[i0][j0] = (tid, variant)

                found = dfs_(idx + 1)
                if found:
                    return found
                else:
                    grid[i0][j0] = None

            in_grid.discard(tid)
        return

    dfs_(0)

    return grid


def part1(grid):
    return grid[0][0][0] * grid[0][-1][0] * grid[-1][0][0] * grid[-1][-1][0]


def part2(grid: List[List[Tuple[int, Tile]]], monster: str):
    image = np.vstack([np.hstack([g[1][1:-1, 1:-1] for g in row]) for row in grid])
    image[image == "#"] = 1
    image[image == "."] = 0
    image = image.astype(int)

    monster = np.array([list(l) for l in monster.strip("\n").splitlines()])
    monster[monster != "#"] = 0
    monster[monster == "#"] = 1
    monster = monster.astype(int)

    target = np.count_nonzero(monster == 1)

    # find monster
    found = np.zeros(image.shape, dtype=int)

    for m in variants(monster):
        # monster is 3x20, the correlation center is at (1, 10)
        corr = ndimage.correlate(image, m, mode="constant", cval=0)

        ly, lx = m.shape
        cx, cy = lx // 2, ly // 2

        indices = np.nonzero(corr == target)
        for i, j in zip(*indices):
            this_found = np.zeros(image.shape, dtype=int)
            this_found[i - cy : i - cy + ly, j - cx : j - cx + lx] = m
            found += this_found

    roughness = np.where(found >= 1, 0, image)

    return roughness.ravel().sum()


if __name__ == "__main__":
    monster = """
                  # 
#    ##    ##    ###
 #  #  #  #  #  #   
"""

    tiles = load("test.txt")
    grid = dfs(tiles)
    assert part1(grid) == 20899048083289
    assert part2(grid, monster) == 273

    tiles = load("input.txt")
    grid = dfs(tiles)
    print("part 1 answer: ", part1(grid))
    print("part 2 answer: ", part2(grid, monster))
