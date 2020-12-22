from collections import deque
from itertools import islice
from typing import List, Tuple, Deque


def load(text: List[str]) -> Tuple[List[int], List[int]]:
    idx = next(i for i in range(len(text)) if text[i] == "")

    p1 = [int(x) for x in text[1:idx]]
    p2 = [int(x) for x in text[idx + 2 :]]
    return p1, p2


def part1(cards: Tuple[List[str], List[str]]) -> int:
    p1, p2 = cards
    p1, p2 = deque(p1), deque(p2)

    while p1 and p2:
        c1 = p1.popleft()
        c2 = p2.popleft()
        if c1 > c2:
            p1.append(c1)
            p1.append(c2)
        else:
            p2.append(c2)
            p2.append(c1)

    p = p1 or p2
    return sum(a * b for a, b in enumerate(reversed(p), 1))


def check_p1_win(cards: Tuple[List[int], List[int]]) -> Tuple[bool, Deque]:
    p1, p2 = cards
    p1, p2 = deque(p1), deque(p2)

    records = set()

    while p1 and p2:
        if (pattern := (tuple(p1), tuple(p2))) in records:
            return True, []
        else:
            records.add(pattern)

        c1 = p1.popleft()
        c2 = p2.popleft()

        if c1 <= len(p1) and c2 <= len(p2):
            p1_win, _ = check_p1_win((islice(p1, 0, c1), islice(p2, 0, c2)))
        else:
            p1_win = c1 > c2

        if p1_win:
            p1.append(c1)
            p1.append(c2)
        else:
            p2.append(c2)
            p2.append(c1)

    return bool(p1), p1 or p2


def part2(cards: Tuple[List[int], List[int]]) -> int:
    _, p = check_p1_win(cards)
    ans = sum(a * b for a, b in enumerate(reversed(p), 1))
    return ans


if __name__ == "__main__":
    # test
    text = """
Player 1:
9
2
6
3
1

Player 2:
5
8
4
7
10""".strip().splitlines()
    cards = load(text)
    assert part1(cards) == 306
    assert part2(cards) == 291

    with open("input.txt") as f:
        cards = load(f.read().splitlines())
        print("part 1 answer:", part1(cards))
        print("part 2 answer:", part2(cards))
