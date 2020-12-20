from functools import lru_cache
from itertools import product, chain, starmap
from typing import List, Dict, Tuple, Iterable, Union


def build_rules(line: str):
    id_, content = line.split(":")
    rules = []
    for p in content.strip().split("|"):
        if '"' in p:
            rules.append(p.strip('"'))
        else:
            rules.append([int(x) for x in p.split()])
    return {int(id_): rules}


def build_candidates(rules: Dict):
    @lru_cache(None)
    def helper(id_):
        rule = rules[id_]
        if isinstance(rule[0], str):
            return {rule[0]}
        else:
            return set(
                (
                    "".join(x)
                    for x in chain.from_iterable(
                        map(lambda lst: product(*[helper(c) for c in lst]), rule)
                    )
                )
            )

    return {k: helper(k) for k in rules}


def check(text, start, rule_id, rules: Dict) -> Iterable[int]:
    """ return index that text[start: index] matches the given rule """
    if start >= len(text):
        yield start
        return

    for r in rules[rule_id]:
        if isinstance(r, str):
            if text[start] == r:
                yield start + 1
        else:
            starts = [start]
            next_starts = []
            for child_id in r:
                next_starts = []
                for s in starts:
                    ends = check(text, s, child_id, rules)
                    ends = [x for x in ends if x != s]
                    next_starts.extend(ends)

                if not next_starts:
                    break
                else:
                    starts = next_starts

            yield from next_starts


def match_rule(text, rule_id, rules) -> bool:
    return any(e == len(text) for e in check(text, 0, rule_id, rules))

def load(text: str) -> Tuple[Dict, List[str]]:
    lines = text.strip().splitlines()
    i = 0

    rules = {}
    while lines[i]:
        rules.update(build_rules(lines[i]))
        i += 1

    messages = lines[i + 1 :]
    return rules, messages


def part_1(texts: List[str], rules: Dict) -> int:
    candidates = build_candidates(rules)
    return sum(1 for t in texts if t in candidates[0])


if __name__ == "__main__":

    # test
    notes = """
0: 4 1 5
1: 2 3 | 3 2
2: 4 4 | 5 5
3: 4 5 | 5 4
4: "a"
5: "b"

ababbb
bababa
abbbab
aaabbb
aaaabbb"""
    rules, messages = load(notes)
    assert part_1(messages, rules) == 2

    notes = """
42: 9 14 | 10 1
9: 14 27 | 1 26
10: 23 14 | 28 1
1: "a"
11: 42 31
5: 1 14 | 15 1
19: 14 1 | 14 14
12: 24 14 | 19 1
16: 15 1 | 14 14
31: 14 17 | 1 13
6: 14 14 | 1 14
2: 1 24 | 14 4
0: 8 11
13: 14 3 | 1 12
15: 1 | 14
17: 14 2 | 1 7
23: 25 1 | 22 14
28: 16 1
4: 1 1
20: 14 14 | 1 15
3: 5 14 | 16 1
27: 1 6 | 14 18
14: "b"
21: 14 1 | 1 14
25: 1 1 | 1 14
22: 14 14
8: 42
26: 14 22 | 1 20
18: 15 15
7: 14 5 | 1 21
24: 14 1

abbbbbabbbaaaababbaabbbbabababbbabbbbbbabaaaa
bbabbbbaabaabba
babbbbaabbbbbabbbbbbaabaaabaaa
aaabbbbbbaaaabaababaabababbabaaabbababababaaa
bbbbbbbaaaabbbbaaabbabaaa
bbbababbbbaaaaaaaabbababaaababaabab
ababaaaaaabaaab
ababaaaaabbbaba
baabbaaaabbaaaababbaababb
abbbbabbbbaaaababbbbbbaaaababb
aaaaabbaabaaaaababaa
aaaabbaaaabbaaa
aaaabbaabbaaaaaaabbbabbbaaabbaabaaa
babaaabbbaaabaababbaabababaaab
aabbbbbaabbbaaaaaabbbbbababaaaaabbaaabba"""
    rules, messages = load(notes)
    rules.update(build_rules('8: 42 | 42 8'))
    rules.update(build_rules('11: 42 31 | 42 11 31'))
    ans2 = sum(1 for m in messages if match_rule(m, 0, rules))
    assert ans2 == 12,  f"wrong {ans2}"

    with open('input.txt') as f:
        rules, messages = load(f.read())

        # part1
        print('part 1 answer: ', part_1(messages, rules))

        # part2
        rules.update(build_rules('8: 42 | 42 8'))
        rules.update(build_rules('11: 42 31 | 42 11 31'))
        ans2 = sum(1 for m in messages if match_rule(m, 0, rules))
        print('part 2 answer: ', ans2)
