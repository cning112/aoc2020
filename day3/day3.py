from functools import reduce
from itertools import count, starmap


def part_1():
    print("part 1: trees ", count_trees(3, 1))


def part_2():
    options = [
        (1, 1),
        (3, 1),
        (5, 1),
        (7, 1),
        (1, 2),
    ]
    prod = reduce(lambda x, y: x * y, starmap(count_trees, options), 1)
    print("part 2: product ", prod)


def count_trees(x_step: int, y_step: int):
    with open("input.txt") as f:
        trees = sum(
            1
            for x, (_, line) in zip(
                count(0, step=x_step),
                filter(lambda e: e[0] % y_step == 0, enumerate(f)),
            )
            if line.strip()[x % (len(line) - 1)] == "#"
        )
        return trees


if __name__ == "__main__":
    part_1()
    part_2()
