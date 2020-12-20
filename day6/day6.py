from functools import reduce
from itertools import chain
from typing import List

import pytest


def count_any_in_group(lines: List[str]) -> int:
    if not lines:
        return 0

    uniq = {x for x in chain(*lines)}
    uniq -= {'\n'}
    return len(uniq)


def count_all_in_group(lines: List[str]) -> int:
    if not lines:
        return 0

    shared = reduce(lambda a, b: a & b, map(set, lines))
    shared -= {'\n'}
    return len(shared)


if __name__ == "__main__":
    with open("input.txt") as f:
        lines = []
        ans_1 = ans_2 = 0
        for line in f:
            if line == "\n":
                ans_1 += count_any_in_group(lines)
                ans_2 += count_all_in_group(lines)
                lines = []
            else:
                lines.append(line)

        ans_1 += count_any_in_group(lines)
        ans_2 += count_all_in_group(lines)

    print("part 1: sum of any 'yes' counts is", ans_1)
    print("part 2: sum of shared 'yes' counts is", ans_2)
