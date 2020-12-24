import operator
from collections import defaultdict
from dataclasses import dataclass
from functools import reduce
from typing import List, Iterator, Dict

import numpy as np
from scipy import ndimage


@dataclass(frozen=True)
class Unit:
    x: int  # 1 per unit
    y: int  # sqrt(3) per unit

    def __add__(self, other):
        return Unit(self.x + other.x, self.y + other.y)


mapping = {
    "e": Unit(2, 0),
    "se": Unit(1, -1),
    "sw": Unit(-1, -1),
    "w": Unit(-2, 0),
    "nw": Unit(-1, 1),
    "ne": Unit(1, 1),
}


def parse(s: str) -> Iterator[str]:
    i = 0
    while i < len(s):
        if s[i] in mapping:
            yield s[i]
            i += 1
        else:
            yield s[i : i + 2]
            i += 2


def to_coord(s: str) -> Unit:
    vs = map(mapping.get, parse(s))
    return reduce(operator.add, vs)


def flip(lines: List[str]) -> Dict[Unit, int]:
    cnt = defaultdict(int)
    for line in lines:
        cnt[to_coord(line)] += 1
    return cnt


def part1(lines: List[str]) -> int:
    cnt = flip(lines)
    return sum(1 for c in cnt.values() if c & 1)


def part2(lines: List[str], days: int) -> int:
    init = flip(lines)

    black_idx = []
    x_min = y_min = float("inf")
    x_max = y_max = -float("inf")
    for v, c in init.items():
        x, y = v.x, v.y
        if y & 1:
            x -= 1

        x >>= 1

        if c & 1:  # black tile
            black_idx.append((y, x))

        x_min = min(x_min, x)
        y_min = min(y_min, y)
        x_max = max(x_max, x)
        y_max = max(y_max, y)

    # initialize with all white tiles
    array = np.zeros((y_max - y_min + 1, x_max - x_min + 1), dtype=int)

    # add black tiles with offset: the origin point is now moved to (-y_min, -x_min)
    black_idx = [(y - y_min, x - x_min) for y, x in black_idx]
    array[tuple(np.array(black_idx).T)] = 1

    # padding: the origin point is moved to (-y_min + days, -x_min + days)
    n_pad = (
        days + 1 if (days - y_min) & 1 else days
    )  # make sure the origin y is moved to an even-valued y
    array = np.pad(array, n_pad, mode="constant", constant_values=0)

    # y = 3:    0   1
    #          / \ / \
    # y = 2:  0   1   2
    #          \ / \ /
    # y = 1:    0   1
    #          / \ / \
    # y = 0:  0   1   2
    even_kernel = np.array([[1, 1, 0], [1, 0, 1], [1, 1, 0],])
    odd_kernel = np.array([[0, 1, 1], [1, 0, 1], [0, 1, 1],])

    for _ in range(days):
        cnt = np.zeros(array.shape)

        cnt[::2, :] = ndimage.correlate(array, even_kernel, mode="constant", cval=0)[
            ::2, :
        ]

        cnt[1::2, :] = ndimage.correlate(array, odd_kernel, mode="constant", cval=0)[
            1::2, :
        ]

        to_black = np.logical_and(array == 0, cnt == 2)
        to_white = np.logical_and(array == 1, np.logical_or(cnt == 0, cnt > 2))
        array = np.where(to_black, 1, array)
        array = np.where(to_white, 0, array)

    return np.count_nonzero(array == 1)


if __name__ == "__main__":
    # test
    with open("test.txt") as f:
        lines = f.read().splitlines()
        ans1 = part1(lines)
        assert ans1 == 10
        ans2 = part2(lines, 100)
        assert ans2 == 2208, f"wrong ans2 {ans2}"

    with open("input.txt") as f:
        lines = f.read().splitlines()
        ans1 = part1(lines)
        print("part 1 answer: ", ans1)
        ans2 = part2(lines, 100)
        print("part 2 answer: ", ans2)
