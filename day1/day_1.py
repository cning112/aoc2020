from typing import List


def two_sum(data: List[int]):
    memo = set()
    target = 2020
    for d in data:
        if d in memo:
            return d * (target - d)
        else:
            memo.add(target - d)


def three_sum(data: List[int]):
    target = 2020
    memo = {}

    for i, x in enumerate(data):
        for y in data[i + 1 :]:
            if y in memo:
                return memo[y][0] * memo[y][1] * y
            else:
                memo[target - x - y] = (x, y)


if __name__ == "__main__":
    with open("input.txt") as f:
        data = [int(x) for x in f.read().strip().split("\n")]

    print("part 1 ans: ", two_sum(data))
    print("part 2 ans: ", three_sum(data))
