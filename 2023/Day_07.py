import time
from collections import Counter
from typing import Dict, List, Tuple, Union

STRENGTHS1 = ("A", "K", "Q", "J", "T", "9", "8", "7", "6", "5", "4", "3", "2")
STRENGTHS2 = ("A", "K", "Q", "T", "9", "8", "7", "6", "5", "4", "3", "2", "J")
TYPES = ((5, 0), (4, 1), (3, 2), (3, 1), (2, 2), (2, 1), (1, 1))


def get_type(hand: str, joker: bool = False) -> Tuple[int]:
    c = Counter(hand)
    char_counts = c.most_common(2)
    j_count = c["J"]
    if len(char_counts) > 1:
        hand_type = (char_counts[0][1], char_counts[1][1])
    else:
        hand_type = (5, 0)
    if not joker:
        return hand_type

    if j_count > 0 and j_count < 5:
        if hand_type == (4, 1) or hand_type == (3, 2):
            hand_type = (5, 0)
        elif j_count == 3:
            hand_type = (4, 1)
        elif j_count == 2:
            hand_type = (hand_type[1] + j_count, 1)
        else:
            hand_type = (hand_type[0] + 1, hand_type[1])
    return hand_type


def main():
    strength_table1 = {val: len(STRENGTHS1) - i for i, val in enumerate(STRENGTHS1)}
    type_table = {val: len(TYPES) - i for i, val in enumerate(TYPES)}

    with open(r"2023\Day_07.txt", "r") as file:
        data = file.readlines()

    separated_data = (line.replace("\n", "").split(" ") for line in data)
    hand_table = {hand: {"bid": int(bid)} for hand, bid in separated_data}
    # hand_table = {hand: int(bid) for line in data if (line := line.strip("\n").split(" ")) and (hand := line[0]) and (bid := line[1])}

    for hand in hand_table:
        hand_table[hand]["type"] = get_type(hand)

    sorted_hands = rank_hands(hand_table, type_table, strength_table1)

    total_sum = 0
    for i, hand in enumerate(sorted_hands):
        increment = (i + 1) * hand_table[hand]["bid"]
        total_sum += increment
    print(f"Part 1 result: {total_sum}")

    # Part 2
    strength_table2 = {val: len(STRENGTHS2) - i for i, val in enumerate(STRENGTHS2)}
    for hand in hand_table:
        hand_table[hand]["type"] = get_type(hand, True)
    sorted_hands = rank_hands(hand_table, type_table, strength_table2)
    total_sum = 0
    for i, hand in enumerate(sorted_hands):
        increment = (i + 1) * hand_table[hand]["bid"]
        total_sum += increment
    print(f"Part 1 result: {total_sum}")


def rank_hands(
    hand_table: Dict[str, Dict[str, Union[int, Tuple[int]]]],
    type_table: Dict[Tuple[int], int],
    strength_table: Dict[str, int],
) -> List[str]:
    def second_rule_value(hand: str) -> Tuple[int]:
        return tuple(strength_table[char] for char in hand)

    hand_type = {type: [] for type in type_table.keys()}
    for hand, vals in hand_table.items():
        h_type = vals["type"]
        h_val = second_rule_value(hand)
        hand_type[h_type].append((hand, h_val))

    hands_sorted = []
    for h_type in sorted(hand_type):
        for hand, _ in sorted(hand_type[h_type], key=lambda h: h[1]):
            hands_sorted.append(hand)
    return hands_sorted


if __name__ == "__main__":
    start = time.perf_counter()
    main()
    end = time.perf_counter()
    print(f"\nExecuted in: {end - start} s")
