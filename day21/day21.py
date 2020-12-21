from collections import defaultdict
from functools import lru_cache
from functools import lru_cache
from typing import List, Dict, Optional, Tuple, Set

import numpy as np
from scipy import ndimage

Tile = np.ndarray


def load(foods: List[str]) -> List[Tuple[Set[str], Set[str]]]:
    ans = []
    for f in foods:
        ingredients, allergies = f.split("(", 1)
        ingredients = set(ingredients.strip().split())
        allergies = set(allergies[9:-1].split(", "))
        ans.append((ingredients, allergies))
    return ans


def extract(foods: List[Tuple[Set[str], Set[str]]]) -> Dict[str, str]:
    # One ingredient contains zero or one allergy
    # One allergy only exists in ONE ingredient
    # Not every allergy is labelled

    ingredients_of = {}

    for ingredients, allergies in foods:
        for alg in allergies:
            if alg not in ingredients_of:
                ingredients_of[alg] = ingredients.copy()
            else:
                ingredients_of[alg] &= ingredients

    allergy_of = {}

    while ingredients_of:
        for allergy in ingredients_of:
            ingredients_of[allergy] = ingredients_of[allergy] - allergy_of.keys()

        found = set()
        for allergy, ingredients in ingredients_of.items():
            if len(ingredients) == 1:
                allergy_of[ingredients.pop()] = allergy
                found.add(allergy)

        ingredients_of = {k: v for k, v in ingredients_of.items() if k not in found}

    return allergy_of


def part1(foods, allergies) -> int:
    return sum(1 for f in foods for igd in f[0] if igd not in allergies)


def part2(allergies: Dict[str, str]) -> str:
    s = sorted(allergies.keys(), key=lambda x: allergies[x])
    return ",".join(s)


if __name__ == "__main__":
    # test
    foods = """
mxmxvkd kfcds sqjhc nhms (contains dairy, fish)
trh fvjkl sbzzf mxmxvkd (contains dairy)
sqjhc fvjkl (contains soy)
sqjhc mxmxvkd sbzzf (contains fish)""".strip().splitlines()
    foods = load(foods)
    allergies = extract(foods)
    assert part1(foods, allergies) == 5
    assert part2(allergies) == "mxmxvkd,sqjhc,fvjkl"

    with open("input.txt") as f:
        foods = f.read().strip().splitlines()
        foods = load(foods)
        allergies = extract(foods)
        print("part 1 answer: ", part1(foods, allergies))
        print("part 2 answer: ", part2(allergies))
