import re

checks = {
    "byr": lambda x: len(x) == 4 and 1920 <= int(x) <= 2002,
    "iyr": lambda x: len(x) == 4 and 2010 <= int(x) <= 2020,
    "eyr": lambda x: len(x) == 4 and 2020 <= int(x) <= 2030,
    "hgt": lambda x: 150 <= int(x[:-2]) <= 193
    if x[-2:] == "cm"
    else 59 <= int(x[:-2]) <= 76
    if x[-2:] == "in"
    else False,
    "hcl": lambda x: re.match(r"^#[a-f0-9]{6}$", x),
    "ecl": lambda x: x in {"amb", "blu", "brn", "gry", "grn", "hzl", "oth"},
    "pid": lambda x: re.match(r"^\d{9}$", x),
}

optional_keys = {"cid"}


def part_1(docs):
    ans = 0
    keys = set(checks.keys())
    for data in docs:
        if keys.issubset(data.keys()):
            ans += 1
    return ans


def part_2(docs):
    ans = 0
    for data in docs:
        if all(k in data and f(data[k]) for k, f in checks.items()):
            ans += 1
    return ans


def read_data(f):
    data = []
    d = {}
    for line in f:
        line = line.strip()
        if not line:
            data.append(d)
            d = {}
        else:
            d.update(dict(kv.split(":") for kv in line.split()))
    data.append(d)
    return data


if __name__ == "__main__":
    test_data = """
ecl:gry pid:860033327 eyr:2020 hcl:#fffffd
byr:1937 iyr:2017 cid:147 hgt:183cm

iyr:2013 ecl:amb cid:350 eyr:2023 pid:028048884
hcl:#cfa07d byr:1929

hcl:#ae17e1 iyr:2013
eyr:2024
ecl:brn pid:760753108 byr:1931
hgt:179cm

hcl:#cfa07d eyr:2025 pid:166559648
iyr:2011 ecl:brn hgt:59in
"""
    assert part_1(read_data(test_data.strip().split("\n"))) == 2

    with open("input.txt") as f:
        print("part 1: valid passport: ", part_1(read_data(f)))

    with open("input.txt") as f:
        print("part 2: valid passport: ", part_2(read_data(f)))
