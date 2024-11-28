import re
import time
from typing import Dict, List, Tuple

WORD2NUM = {
    "one": "1",
    "two": "2",
    "three": "3",
    "four": "4",
    "five": "5",
    "six": "6",
    "seven": "7",
    "eight": "8",
    "nine": "9",
}


def filter_numbers_only(searched_text: str) -> str:
    pattern = r"(?=(one|two|three|four|five|six|seven|eight|nine|\d|\n))"
    filtered_list = re.findall(pattern, searched_text)
    return "".join(filtered_list)


def get_coordinate(digits: List[int]) -> Tuple[int]:
    if digits:
        coordinate = int(digits[0] + digits[-1])
        return coordinate


def get_digits(text: str) -> List[int]:
    return re.findall(r"\d", text)


def load_input_data(path: str) -> str:
    with open(path, "r") as file:
        return file.read()


def replace_words_with_digits(original_text: str, replacements: Dict[str, str]) -> str:
    filtered_text = filter_numbers_only(original_text)
    for num_text, num_digit in replacements.items():
        filtered_text = filtered_text.replace(num_text, num_digit)
    return filtered_text


def split_into_lines(text: str) -> List[str]:
    return text.split("\n")


def main():
    # Part 1
    input_data = load_input_data(r"2023\Day_01.txt").lower()
    line_list1 = split_into_lines(input_data)
    line_digits1 = (get_coordinate(get_digits(line)) for line in line_list1 if line)
    result1 = sum(line_digits1)
    print(f"Part 1 result is: {result1}")

    # Part 2
    text2num = replace_words_with_digits(input_data, WORD2NUM)
    line_list2 = split_into_lines(text2num)
    line_digits2 = (get_coordinate(get_digits(line)) for line in line_list2 if line)
    result2 = sum(line_digits2)
    print(f"Part 2 result is: {result2}")


if __name__ == "__main__":
    start = time.perf_counter()
    main()
    end = time.perf_counter()
    print(f"\nExecuted in: {end - start} s")
