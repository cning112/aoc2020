from typing import List, Tuple, Dict, Optional
import re


def masked_value(mask: Optional[str], val: int):
    if mask is None:
        return val

    ans = 0
    for m, v in zip(mask, format(val, 'b').zfill(len(mask))):
        ans <<= 1
        if m == 'X':
            ans += int(v)
        elif m == '1':
            ans += 1
    return ans

def docking_program(lines: List[str]) -> int:
    effective = {}
    mask = None
    for i, line in enumerate(lines):
        if line.startswith('mask'):
            mask = line.split('=')[-1].strip()
        else:
            m = re.match(r"mem\[(\d+)\] = (\d*)", line)
            pos, val = m.group(1), m.group(2)
            effective[int(pos)] = (mask, int(val))

    mem = {k: masked_value(v[0], v[1]) for k, v in effective.items()}
    return sum(mem.values())


def floating_addresses(mask: Optional[str], addr: int) -> List[int]:
    if not mask:
        return addr

    # N = 1 << sum(1 for x in mask if x == "X")

    ans = [0]
    for m, v in zip(mask, format(addr, 'b').zfill(len(mask))):
        if m == 'X':
            ans = [a<<1 for a in ans]
            ans += [a+1 for a in ans]
        else:
            v = int(v) if m == '0' else 1
            for i in range(len(ans)):
                ans[i] = (ans[i] << 1) + v
    return ans


def docking_program_v2(lines: List[str]) -> int:
    mem = {}
    mask = None
    for i, line in enumerate(lines):
        if line.startswith('mask'):
            mask = line.split('=')[-1].strip()
        else:
            m = re.match(r"mem\[(\d+)\] = (\d*)", line)
            pos, val = int(m.group(1)), int(m.group(2))

            addresses = floating_addresses(mask, pos)

            for addr in addresses:
                mem[addr] = val

    return sum(mem.values())

if __name__ == "__main__":

    # test:
    notes = """
mask = XXXXXXXXXXXXXXXXXXXXXXXXXXXXX1XXXX0X
mem[8] = 11
mem[7] = 101
mem[8] = 0
""".strip().splitlines()

    ans1 = docking_program(notes)
    assert ans1 == 165, f"wrong answer: {ans1}"

    notes = """
mask = 000000000000000000000000000000X1001X
mem[42] = 100
mask = 00000000000000000000000000000000X0XX
mem[26] = 1
""".strip().splitlines()
    ans2 = docking_program_v2(notes)
    assert ans2 == 208, f"wrong answer: {ans2}"

    with open('input.txt') as f:
        lines = f.read().splitlines()

        ans = docking_program(lines)
        print('part 1 answer: ', ans)

        ans = docking_program_v2(lines)
        print('part 2 answer: ', ans)
