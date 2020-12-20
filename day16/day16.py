import bisect
from typing import List, Tuple, Dict, Optional
from collections import Counter, defaultdict
import re


def invalid_numbers(lines):
    lines = iter(lines)

    rules = []
    while True:
        line = next(lines)
        if not line:
            break
        numbers = re.findall(r"\d+", line.split(":")[-1])
        for i in range(0, len(numbers), 2):
            rules.append((int(numbers[i]), int(numbers[i + 1])))

    rules.sort()
    cleaned_rules = []
    for c, d in rules:
        if not cleaned_rules:
            cleaned_rules.append((c, d))
        else:
            a, b = cleaned_rules[-1]
            if c <= b:
                cleaned_rules[-1] = (a, d)
            else:
                cleaned_rules.append((c, d))
    rules = cleaned_rules
    starts = [x[0] for x in rules]

    next(lines)
    my_ticket = next(lines)

    next(lines)
    next(lines)

    invalid = []
    for line in lines:
        for v in line.split(","):
            v = int(v)
            i = bisect.bisect_right(starts, v) - 1
            if i < 0 or v > rules[i][1]:
                invalid.append(v)

    return sum(invalid)


def part2(lines):
    lines = iter(lines)

    line = next(lines)
    rules = defaultdict(set)
    while line:
        f, v = line.split(':')
        v = re.findall(r"\d+", v)
        for i in range(0, len(v), 2):
            rules[f] |= set(range(int(v[i]), int(v[i+1]) + 1))
        line = next(lines)

    line = next(lines)
    tickets = [list(map(int, next(lines).split(',')))]

    invalid_sum = 0

    line = next(lines)
    line = next(lines)
    for line in lines:
        vs = [int(x) for x in line.split(',')]
        is_valid = True

        for v in vs:
            if all(v not in s for s in rules.values()):
                invalid_sum += v
                is_valid = False

        if is_valid:
            tickets.append(vs)

    print('invalid number sum: ', invalid_sum)

    # find out fields
    possible_fields = [set() for _ in range(len(tickets[0]))]
    for i, field_values in enumerate(zip(*tickets)):
        field_values = set(field_values)
        for field, ranges in rules.items():
            if field_values.issubset(ranges):
                possible_fields[i].add(field)

    def dfs(i_start, curr):
        if i_start == len(possible_fields):
            return curr

        possible = possible_fields[i_start] -set(curr)
        for f in possible:
            curr.append(f)
            found = dfs(i_start+1, curr)
            if found:
                return found
            curr.pop()

    correct_fields =dfs(0, [])

    mult = 1
    for f, v in zip(correct_fields, tickets[0]):
        if f.startswith('departure'):
            mult *= v
    print('multiply six values: ', mult)

    return invalid_sum, mult


if __name__ == "__main__":

    # test
    notes = """
class: 1-3 or 5-7
row: 6-11 or 33-44
seat: 13-40 or 45-50

your ticket:
7,1,14

nearby tickets:
7,3,47
40,4,50
55,2,20
38,6,12
"""
    lines = notes.strip().splitlines()
    ans1 = invalid_numbers(lines)
    assert ans1 == 71, f"wrong answer {ans1}"

    with open("input.txt") as f:
        lines = f.read().strip().splitlines()
        ans = part2(lines)
