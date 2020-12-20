from typing import List, Tuple, Dict, Optional
from collections import Counter, defaultdict
import re


def spoken(starting: List[int], end: int) -> int:
    history = defaultdict(list)
    for i, v in enumerate(starting):
        history[v].append(i)

    prev = starting[-1]

    for i in range(len(starting), end):
        if len(history[prev]) == 1:
            s = 0
        else:
            s = history[prev][-1] - history[prev][-2]

        history[s].append(i)
        prev = s

    return prev


if __name__ == "__main__":

    # test:
    for text, expected in [
        ("0,3,6", 436),
        ("1,3,2", 1),
        ("2,1,3", 10),
        ("1,2,3", 27),
        ("2,3,1", 78),
        ("3,2,1", 438),
        ("3,1,2", 1836),
    ]:
        notes = text.strip().split(",")
        actual = spoken(list(map(int, notes)), 2020)
        assert actual == expected, f"wrong answer 1: {actual} for {text}"

    # for text, expected in [
    #     ("0,3,6", 175594),
    #     ("1,3,2", 2578),
    #     ("2,1,3", 3544142),
    #     ("1,2,3", 261214),
    #     ("2,3,1", 6895259),
    #     ("3,2,1", 18),
    #     ("3,1,2", 362),
    # ]:
    #     notes = text.strip().split(",")
    #     actual = spoken(list(map(int, notes)), 30000000)
    #     assert actual == expected, f"wrong answer 2: {actual} for {text}"

    text = "6,19,0,5,7,13,1"
    notes = text.strip().split(",")
    ans = spoken(list(map(int, notes)), 2020)
    print(f"part 1 answer: {ans}")

    ans = spoken(list(map(int, notes)), 30000000)
    print(f"part 2 answer: {ans}")
