import re
from typing import Tuple

pat = re.compile(r"(\d+)-(\d+) (\w): (.*)")


def parse(line: str) -> Tuple[str, str, int, int]:
    m = pat.match(line)
    return m.group(4), m.group(3), int(m.group(1)), int(m.group(2))


def part_1():
    ans = 0
    with open('input.txt') as f:
        for line in f:
            pwd, char, x, y = parse(line)
            cnt = sum(1 for c in pwd if c == char)
            if x <= cnt <= y:
                ans += 1
    print('part 1: valid password:', ans)


def part_2():
    ans = 0
    with open('input.txt') as f:
        for line in f:
            pwd, char, i, j = parse(line)
            a = pwd[i-1] == char
            b = pwd[j-1] == char
            ans += a ^ b

    print('part 2: valid password:', ans)


if __name__ == '__main__':
    part_1()
    part_2()
