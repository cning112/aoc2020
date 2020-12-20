from collections import defaultdict, Counter
from functools import reduce
from itertools import chain, accumulate
from typing import List, Tuple

directions = ["N", "E", "S", "W", "N"]
to_left = dict(zip(directions[1:], directions))
to_right = dict(zip(directions, directions[1:]))


def location(instructions: List[str]) -> Tuple[int, int]:
    # initially facing east
    x = y = 0
    direction = facing = "E"
    for ins in instructions:
        action, steps = ins[0], int(ins[1:])

        if action == "L":
            n = steps // 90
            while n:
                direction = facing = to_left[facing]
                n -= 1
            steps = 0
        elif action == "R":
            n = steps // 90
            while n:
                direction = facing = to_right[facing]
                n -= 1
            steps = 0
        elif action == "F":
            direction = facing
        else:
            direction = action

        if direction == "E":
            x += steps
        elif direction == "S":
            y -= steps
        elif direction == "W":
            x -= steps
        elif direction == "N":
            y += steps
        else:
            raise

    return x, y


def use_waypoint(instructions: List[str]) -> Tuple[int, int]:
    x = y = 0
    wx, wy = (10, 1)

    for ins in instructions:
        action, steps = ins[0], int(ins[1:])

        if action == "L":
            n = steps // 90
            while n:
                wx, wy = -wy, wx
                n -= 1
        elif action == "R":
            n = steps // 90
            while n:
                wx, wy = wy, -wx
                n -= 1
        elif action == "N":
            wy += steps
        elif action == "E":
            wx += steps
        elif action == "S":
            wy -= steps
        elif action == "W":
            wx -= steps
        else:
            x += steps * wx
            y += steps * wy
    return x, y


if __name__ == "__main__":
    # test:
    instructions = """
F10
N3
F7
R90
F11
""".strip().splitlines()
    ans1 = location(instructions)
    ans2 = use_waypoint(instructions)
    assert ans1 == (17, -8), f"wrong answer: {ans1}"
    assert ans2 == (214, -72), f"wrong answer: {ans2}"

    with open("input.txt") as f:
        instructions = f.read().splitlines()
        ans1 = location(instructions)
        print("part 1 answer: ", abs(ans1[0]) + abs(ans1[1]))

        ans2 = use_waypoint(instructions)
        print("part 2 answer: ", abs(ans2[0]) + abs(ans2[1]))
