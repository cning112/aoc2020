from collections import defaultdict, Counter
from functools import reduce
from itertools import chain, accumulate
from typing import List


def multiply_one_three(jolts: List[int]):
    jolts = jolts.copy()

    # source input
    jolts.append(0)

    jolts = sorted(jolts)

    cnt = Counter(b - a for a, b in zip(jolts, jolts[1:]))

    # final to the 3-jolt higher built-in adapter
    cnt[3] += 1

    assert max(cnt.keys()) <= 3
    assert min(cnt.keys()) >= 1

    return cnt[1] * cnt[3]


def count_arrangements(jolts: List[int]) -> int:
    jolts = jolts.copy()

    jolts.append(0)
    jolts.append(max(jolts) + 3)
    jolts = sorted(jolts)

    dp = [0] * len(jolts)
    dp[0] = 1
    for i in range(1, len(jolts)):
        curr = jolts[i]
        j = i - 1
        while j >= 0 and jolts[j] + 3 >= curr:
            dp[i] += dp[j]
            j -= 1

    return dp[-1]

if __name__ == "__main__":
    # example 1
    with open("example_1.txt") as f:
        jolts = [int(x) for x in f.read().splitlines()]
        assert multiply_one_three(jolts) == 35
        assert count_arrangements(jolts) == 8

    # example 2
    with open("example_2.txt") as f:
        jolts = [int(x) for x in f.read().splitlines()]
        assert multiply_one_three(jolts) == 220
        assert count_arrangements(jolts) == 19208

    with open("input.txt") as f:
        jolts = [int(x) for x in f.read().splitlines()]
        print('part 1: answer', multiply_one_three(jolts))
        print('part 2: answer', count_arrangements(jolts))
