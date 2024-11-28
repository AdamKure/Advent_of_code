import re
import time

DUMMY = "Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53\n\
Card 2: 13 32 20 16 61 | 61 30 68 82 17 32 24 19\n\
Card 3:  1 21 53 59 44 | 69 82 63 72 16 21 14  1\n\
Card 4: 41 92 73 84 69 | 59 84 76 51 58  5 54 83\n\
Card 5: 87 83 26 28 32 | 88 30 70 12 93 22 82 36\n\
Card 6: 31 18 13 56 72 | 74 77 10 23 35 67 36 11"


def main():
    with open(r"2023\Day_04.txt", "r") as file:
        input_data = file.readlines()

    # input_data = re.split(r"\n", DUMMY)

    # Part 1
    total_points = 0
    for line in input_data:
        _, line = line.split(": ")
        winning_numbers, my_numbers = line.split(" | ")
        winning_numbers = {
            match.group(0) for match in re.finditer(r"(\d+)", winning_numbers)
        }
        my_numbers = {match.group(0) for match in re.finditer(r"(\d+)", my_numbers)}
        overlap = my_numbers.intersection(winning_numbers)
        points = int(2 ** (len(overlap) - 1))
        total_points += points
    print(total_points)

    # Part 2
    card_amount = {f"{index}": 1 for index, _ in enumerate(input_data, start=1)}
    for card_number, line in enumerate(input_data, start=1):
        _, line = line.split(": ")
        winning_numbers, my_numbers = line.split(" | ")
        winning_numbers = {
            match.group(0) for match in re.finditer(r"(\d+)", winning_numbers)
        }
        my_numbers = {match.group(0) for match in re.finditer(r"(\d+)", my_numbers)}
        overlap = my_numbers.intersection(winning_numbers)
        copies = len(overlap)
        for copy in range(copies):
            copy_number = card_number + copy + 1
            card_amount[f"{copy_number}"] += card_amount.get(f"{card_number}")
    print(sum(card_amount.values()))


if __name__ == "__main__":
    start = time.perf_counter()
    main()
    end = time.perf_counter()
    print(f"\nExecuted in: {end - start} s")
