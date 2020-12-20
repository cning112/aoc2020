import operator
import re
from functools import reduce
from typing import List

import numpy as np
from scipy import ndimage

ops = {"*": operator.mul, "+": operator.add}


def same_precedence(line: str) -> int:
    stack = []
    for c in list(line):
        if c == " ":
            continue

        if c == "(" or c == ")":
            stack.append(c)
        elif c in ops:
            stack.append(c)
        else:
            stack.append(int(c))

        while len(stack) >= 3:
            if stack[-1] == ")":
                assert stack[-3] == "("
                stack.pop()
                v = stack.pop()
                stack.pop()
                stack.append(v)
            elif stack[-2] in ops and isinstance(stack[-1], int):
                b = stack.pop()
                op = stack.pop()
                a = stack.pop()
                stack.append(ops[op](a, b))
            else:
                break

    assert len(stack) == 1
    return stack.pop()


def diff_precedence(line: str) -> int:
    chars = [x for x in list(line) if x != " "]
    level = 0
    stack = []
    buff = []
    for i, c in enumerate(chars):
        if level == 0:
            if c == "(":
                level += 1
            else:
                stack.append(c)
        else:
            if c == "(":
                level += 1
                buff.append(c)
            elif c == ")":
                level -= 1

                if level == 0:
                    stack.append(diff_precedence("".join(buff)))
                    buff.clear()

                buff.append(c)
            else:
                buff.append(c)

        while len(stack) >= 3 and stack[-2] == "+":
            b = stack.pop()
            stack.pop()
            a = stack.pop()
            stack.append(int(a) + int(b))

    while len(stack) >= 3:
        b = stack.pop()
        op = stack.pop()
        a = stack.pop()
        stack.append(ops[op](int(a), int(b)))

    return stack.pop()


def part1(lines) -> int:
    return sum(same_precedence(l) for l in lines)


if __name__ == "__main__":

    # test
    tests = [
        ("1 + (2 * 3) + (4 * (5 + 6))", 51, 51),
        ("1 + 2 * 3 + 4 * 5 + 6", 71, 231),
        ('2 * 3 + (4 * 5)', 26, 46, ),
        ('5 + (8 * 3 + 9 + 3 * 4 * 3)', 437, 1445),
        ("5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4))", 12240, 669060),
        ("((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2", 13632, 23340),
    ]
    for line, expected_1, expected_2 in tests:
        print(line)
        actual_1 = same_precedence(line)
        actual_2 = diff_precedence(line)
        assert actual_1 == expected_1, f"1. Expected {expected_1}, got {actual_1}"
        assert actual_2 == expected_2, f"2. Expected {expected_2}, got {actual_2}"

    with open("input.txt") as f:
        lines = f.read().splitlines()
        ans1 = part1(lines)
        print("part 1 answer", ans1)

        ans2 = sum(diff_precedence(line) for line in lines)
        print("part 2 answer", ans2)
