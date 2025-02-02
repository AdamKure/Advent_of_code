import re
import time

DAY = 3


def read_files(day: int) -> tuple[str, str]:
    with open(f"2024/Day_{day:02}_example.txt", "r") as file:
        example = file.read()

    with open(f"2024/Day_{day:02}.txt", "r") as file:
        real_input = file.read()

    return example, real_input


def part_1(data: str) -> None:
    total = 0
    for x, y in re.findall(r"mul\((\d{1,3}),(\d{1,3})\)", data):
        total += int(x) * int(y)
    print(f"Part 1 is: {total}")


def part_2(data: str) -> None:
    memory = re.sub(r"don't\(\).*?(do\(\)|$)", "", data, flags=re.DOTALL)
    total = 0
    for x, y in re.findall(r"mul\((\d{1,3}),(\d{1,3})\)", memory):
        total += int(x) * int(y)
    print(f"Part 2 is: {total}")


def main() -> None:
    example, real_input = read_files(DAY)

    part_1(example)
    part_1(real_input)

    part_2(example)
    part_2(real_input)


if __name__ == "__main__":
    start = time.perf_counter()
    main()
    end = time.perf_counter()
    print(f"\nExecuted in: {end - start} s")
