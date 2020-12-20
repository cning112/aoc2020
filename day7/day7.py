from collections import defaultdict
from functools import reduce
from itertools import chain
from typing import List, Tuple, Dict, Set

import pytest
import re


def parse_rule(rule: str) -> Tuple[str, List[Tuple[int, str]]]:
    m = re.search(r"^(.*) bags contain ((?=\d+ (?=.*?) bags?[,\.]\s?)+)", rule)
    f, s = rule.split("contain")
    k = re.match(r"^(.*?) bags", f).group(1)
    vs = re.findall(r"(\d+) (.*?) bags?", s)
    return k, [(int(v[0]), v[1]) for v in vs]


def parents(rules: Dict[str, List[Tuple[int, str]]], target_child: str) -> Set[str]:
    rev = defaultdict(list)
    for p, cs in rules.items():
        for _, c in cs:
            rev[c].append(p)

    ans = set()
    to_search = rev[target_child]
    while to_search:
        next_search = []
        for s in to_search:
            ans.add(s)
            next_search.extend(rev[s])
        to_search = next_search
    return ans


def count_children(rules, parent: str) -> int:
    ans = 0
    search = [(1, parent)]
    while search:
        np, p = search.pop()
        ans += np
        for nc, c in rules[p]:
            search.append((nc * np, c))

    return ans - 1  # exclude the parent bag


if __name__ == "__main__":
    rules = {}
    with open("input.txt") as f:
        for line in f:
            k, v = parse_rule(line.strip())
            rules[k] = v

    ps = parents(rules, "shiny gold")
    print("part 1: bag colors ", len(ps))

    print("part 2: number of children bags ", count_children(rules, "shiny gold"))
