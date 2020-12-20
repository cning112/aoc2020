from typing import List, Tuple, Dict


def bus_and_wait_time(arr_time: int, buses: Dict[int, int]) -> Tuple[int, int]:
    wait_time = float("inf")
    the_bus = None
    for bus in buses.values():
        d, m = divmod(arr_time, bus)
        if m == 0:
            return bus, 0
        else:
            m = bus - m
            if m < wait_time:
                wait_time = m
                the_bus = bus
    return the_bus, wait_time


def use_lcm(buses: Dict[int, int], start=0):
    tuples = [
        (k, (k + start + v - 1) // v * v, v) for k, v in buses.items()
    ]  # delay, start, interval

    def combine(b1, b2):
        d1, s1, i1 = b1
        d2, s2, i2 = b2
        a = s1 - d1
        b = s2 - d2
        while a != b:
            if a > b:
                b += i2
            else:
                a += i1
        r = (
            d1,
            a + d1,
            i1 * i2,
        )  # i1 * i2 is the least common multiple, because we know both i1 and i2 are prime numbers
        return r

    def dc(arr: List[Tuple[int, int, int]]) -> Tuple[int, int, int]:
        if len(arr) >= 2:
            half = len(arr) >> 1
            return combine(dc(arr[:half]), dc(arr[half:]))
        else:
            return arr[0]

    ret = dc(tuples)
    return ret[1] - ret[0]


def to_buses(s: str) -> Dict[int, int]:
    return {i: int(x) for i, x in enumerate(s.split(",")) if x != "x"}


if __name__ == "__main__":

    # test:
    notes = """
939
7,13,x,x,59,x,31,19
""".strip().splitlines()
    arr_time = int(notes[0])
    buses = {i: int(x) for i, x in enumerate(notes[1].split(",")) if x != "x"}

    ans1 = bus_and_wait_time(arr_time, buses)
    # ans2 = use_waypoint(instructions)
    assert ans1 == (59, 5), f"wrong answer: {ans1}"
    assert use_lcm(to_buses("17,x,13,19"), 0) == 3417
    assert use_lcm(to_buses("67,7,59,61"), 0) == 754018
    assert use_lcm(to_buses("67,x,7,59,61"), 0) == 779210
    assert use_lcm(to_buses("1789,37,47,1889"), 0) == 1202161486

    # data
    with open("input.txt") as f:
        notes = f.read().splitlines()
        arr_time = int(notes[0])
        buses = {i: int(x) for i, x in enumerate(notes[1].split(",")) if x != "x"}

        ans1 = bus_and_wait_time(arr_time, buses)
        print("part 1 answer: ", ans1[0] * ans1[1])

        ans2 = use_lcm(buses, 100000000000000)
        print("part 2 answer: ", ans2)
