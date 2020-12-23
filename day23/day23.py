import time
from collections import deque
from itertools import islice, cycle, chain
from typing import List, Tuple, Deque
import numpy as np

N_PICK = 3


def move(seq: str, steps: int) -> str:
    N = len(seq)
    for _ in range(steps):

        # always have the current cup the first one in seq
        curr = int(seq[0])
        picked = seq[1 : N_PICK + 1]
        dest = next(
            x
            for x in chain(range(curr - 1, 0, -1), range(N, curr, -1))
            if str(x) not in picked
        )
        dest_idx = next(i for i, x in enumerate(seq) if x == str(dest))

        # new seq
        seq = f"{seq[N_PICK+1:dest_idx]}{dest}{picked}{seq[dest_idx+1:]}{curr}"

    return seq


def part1(seq: str) -> str:
    index = next(i for i, x in enumerate(seq) if x == "1")
    seq = seq[index + 1 :] + seq[:index]
    return seq


def big_move_np(seq: List[int], steps: int) -> List[int]:
    """
    approx. 9000 seconds!
    """

    N = len(seq)

    seq = np.array(seq)

    def move_cups(s: np.ndarray, curr_idx, dest_idx) -> int:
        """ return next curr_idx """
        reserve = list(s[curr_idx + 1 : curr_idx + 1 + N_PICK])

        if dest_idx < curr_idx:
            s[dest_idx + 1 + N_PICK : curr_idx + 1 + N_PICK] = s[
                dest_idx + 1 : curr_idx + 1
            ]
            ans = curr_idx + 4
        else:
            s[curr_idx + 1 : dest_idx + 1 - N_PICK] = s[
                curr_idx + 1 + N_PICK : dest_idx + 1
            ]
            dest_idx -= N_PICK
            ans = curr_idx + 1

        s[dest_idx + 1 : dest_idx + 1 + N_PICK] = reserve

        return ans

    prev_t = None
    curr_idx = 0
    for cnt in range(steps):
        if curr_idx > N - N_PICK - 1:
            seq = np.roll(seq, N - curr_idx)
            curr_idx = 0

        curr = seq[curr_idx]
        picked = set(seq[curr_idx + 1 : curr_idx + 1 + N_PICK])

        dest = next(
            d
            for d in chain(range(curr - 1, 0, -1), range(N, curr, -1))
            if d not in picked
        )
        dest_idx = np.nonzero(seq == dest)[0][0]

        curr_idx = move_cups(seq, curr_idx, dest_idx)

    return list(seq)


def part2(seq: List[int]) -> int:
    index = next(i for i, x in enumerate(seq) if x == 1)
    i1 = (index + 1) % len(seq)
    i2 = (index + 2) % len(seq)
    return seq[i1] * seq[i2]


if __name__ == "__main__":
    # test
    text = "389125467"
    final_10 = move(text, 10)
    final_100 = move(text, 100)
    assert part1(final_10) == "92658374"
    assert part1(final_100) == "67384529"

    # big_seq = list(map(int, list(text))) + list(range(len(text)+1, 1_000_001))
    # final_10m = big_move_np(big_seq, 10_000_000)
    # assert part2(final_10m) == 149245887792

    # input
    text = "789465123"
    final_100 = move(text, 100)
    print("part 1 answer:", part1(final_100))

    seq = list(map(int, list(text))) + list(range(len(text) + 1, 1_000_001))
    final_10m = big_move_np(seq, 10_000_000)
    print("part 2 answer:", part2(final_10m))
