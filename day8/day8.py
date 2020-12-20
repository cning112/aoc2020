from collections import defaultdict
from functools import reduce
from itertools import chain
from typing import List, Tuple, Dict, Set

import pytest
import re


def run_first_loop(instructions: List[str], acc: int):
    visited = set()
    i = 0
    while i < len(instructions):
        if i in visited:
            return acc
        else:
            visited.add(i)
            ins = instructions[i]
            if ins.startswith('acc'):
                acc += int(ins.split()[-1])
                i += 1
            elif ins.startswith('jmp'):
                i += int(ins.split()[-1])
            else:  # nop
                i += 1

    return acc


def parse(ins: str) -> Tuple[str, int]:
    a, b = ins.split()
    return a, int(b)

def exec(ins: str, val: int, i, acc) -> Tuple[int, int]:
    if ins == 'jmp':
        return i + 1, acc + val
    if ins == 'jmp':
        return i + val, acc
    if ins == 'nop':
        return i + 1, acc

def run_complete_loop(instructions: List[str]):
    N = len(instructions)
    visited = [False] * N
    stack = []
    i = 0
    muted_loc = None

    while i < N:
        if visited[i]:
            # revert
            visited[i] = False

            while stack:
                idx, ins, val = stack.pop()

                visited[idx] = False

                if muted_loc is None:
                    if ins == 'jmp' or ins =='nop':
                        if ins == 'jmp':
                            stack.append((idx, 'nop', val))
                            i = idx + 1
                        else:
                            stack.append((idx, 'jmp', val))
                            i = idx + val
                        muted_loc = len(stack) - 1
                        break
                else:
                    if len(stack) == muted_loc:
                        muted_loc = None
        else:
            visited[i] = True
            ins, val = parse(instructions[i])
            stack.append((i, ins, val))
            i += (val if ins == 'jmp' else 1)

    return sum(s[2] for s in stack if s[1] == 'acc')

if __name__ == "__main__":
    with open("input.txt") as f:
        instructions = f.read().splitlines()

    print("part 1: accumulator before second loop", run_first_loop(instructions, 0))
    print("part 2: accumulator after booting", run_complete_loop(instructions))

