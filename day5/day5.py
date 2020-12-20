import pytest


def get_seat_id(s: str) -> int:
    ans = 0
    for c in s:
        ans <<= 1
        if c == "R" or c == "B":
            ans += 1
    return ans


# @pytest.mark.parametrize(
#     "boarding_pass, seat_id",
#     [
#         ("FBFBBFFRLR", 357),
#         ("BFFFBBFRRR", 567),
#         ("FFFBBBFRRR", 119),
#         ("BBFFBBFRLL", 820),
#     ],
# )
# def test(boarding_pass, seat_id):
#     assert get_seat_id(boarding_pass) == seat_id


if __name__ == "__main__":
    with open('input.txt') as f:
        all_seat_ids = [get_seat_id(line.strip()) for line in f]

    max_seat_id = max(all_seat_ids)
    print('part 1: max seat id is ', max_seat_id)

    all_seat_ids.sort()
    for a, b in zip(all_seat_ids, all_seat_ids[1:]):
        if a + 1 != b:
            my_seat_id = a+1
            print('part 2: my seat id is', my_seat_id)
            break

