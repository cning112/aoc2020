from collections import defaultdict
from functools import reduce
from itertools import chain
from typing import List, Tuple, Dict, Set

import pytest
import re


def find_first_anomaly(numbers: List[int], preamble_len: int):
    from collections import defaultdict, Counter

    # init
    cnt = Counter(numbers[:preamble_len])

    # check
    for i in range(preamble_len, len(numbers)):
        v = numbers[i]
        for k in cnt:
            if (v - k == k and cnt[k] > 1) or (v - k != k and cnt[v - k]):
                break
        else:
            return v

        cnt[v] += 1
        if cnt[numbers[i - preamble_len]] > 1:
            cnt[numbers[i - preamble_len]] -= 1
        else:
            del cnt[numbers[i - preamble_len]]


def find_contiguous_sum(numbers: List[int], target: int):
    i = j = s = 0
    while s != target:
        if s < target:
            s += numbers[j]
            j += 1
        else:
            s -= numbers[i]
            i += 1
    return numbers[i:j]


if __name__ == "__main__":
    with open("input.txt") as f:
        numbers = [int(x) for x in f.read().splitlines()]

    first_anomaly = find_first_anomaly(numbers, 25)
    print("part 1: first number", first_anomaly)

    ns = find_contiguous_sum(numbers, first_anomaly)
    print("part 2: min + max", min(ns) + max(ns))
