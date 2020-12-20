from collections import defaultdict, Counter
from functools import reduce
from itertools import chain, accumulate
from typing import List

def neighbors_v1(g, i, j, M, N):
    for x in [-1, 0, 1]:
        if 0 <= i + x < M:
            for y in [-1, 0, 1]:
                if 0 <= j + y < N and not x == y == 0:
                    yield g[i + x][j + y]


def neighbors_v2(g, i, j, M, N):
    for x in [-1, 0, 1]:
        if 0 <= i + x < M:
            for y in [-1, 0, 1]:
                if x == y == 0:
                    continue
                if 0 <= j + y < N:
                    ii = i + x
                    jj = j + y
                    while 0<=ii<M and 0 <= jj < N:
                        if g[ii][jj] == ".":
                            ii += x
                            jj += y
                        else:
                            yield g[ii][jj]
                            break
                    else:
                        yield '.'


def occupied_when_stable(grid, tolerance, neighbor_func):
    M, N = len(grid), len(grid[0])

    stable = False
    while not stable:
        stable = True
        new_grid = [[x for x in row] for row in grid]
        for i in range(M):
            for j in range(N):
                curr = grid[i][j]
                if curr == ".":
                    continue

                occupied = 0
                for nb in neighbor_func(grid, i, j, M, N):
                    if nb == "#":
                        if curr == "L":
                            break
                        occupied += 1
                else:
                    if occupied >= tolerance and curr == "#":
                        new_grid[i][j] = "L"
                        stable = False
                    elif occupied == 0 and curr == "L":
                        new_grid[i][j] = "#"
                        stable = False
        grid = new_grid

    return sum(1 for row in grid for x in row if x == "#")


if __name__ == "__main__":
    # test:
    grid = [list(x) for x in """
.......#.
...#.....
.#.......
.........
..#L....#
....#....
.........
#........
...#.....
""".strip().splitlines()]
    nb = neighbors_v2(grid, 4, 3, len(grid), len(grid[0]))
    assert sum(1 for x in nb if x == '#') == 8

    grid = [list(x) for x in """
.............
.L.L.#.#.#.#.
.............
    """.strip().splitlines()]
    nb = neighbors_v2(grid, 1, 1, len(grid), len(grid[0]))
    assert sum(1 for x in nb if x == 'L') == 1
    assert sum(1 for x in nb if x == '#') == 0

    grid = [list(x) for x in """
.##.##.
#.#.#.#
##...##
...L...
##...##
#.#.#.#
.##.##.
        """.strip().splitlines()]
    nb = neighbors_v2(grid, 3, 3, len(grid), len(grid[0]))
    assert sum(1 for x in nb if x == '#') == 0

    # example 1
    with open("example_1.txt") as f:
        grid = [list(x) for x in f.read().splitlines()]

        ans_1 = occupied_when_stable(grid, 4, neighbors_v1)
        assert ans_1 == 37, f"ans: {ans_1}"

        ans_2 = occupied_when_stable(grid, 5, neighbors_v2)
        assert ans_2 == 26, f"ans: {ans_2}"

    with open("input.txt") as f:
        grid = [list(x) for x in f.read().splitlines()]

        ans_1 = occupied_when_stable(grid, 4, neighbors_v1)
        print("part 1 ans: ", ans_1)

        ans_2 = occupied_when_stable(grid, 5, neighbors_v2)
        print("part 2 ans: ", ans_2)
