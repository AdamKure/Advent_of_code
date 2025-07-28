import time
from functools import cache

DAY = 19


def read_files(day: int) -> tuple[str, str]:
    with open(f"2024/Day_{day:02}_example.txt", "r") as file:
        example = file.read()

    with open(f"2024/Day_{day:02}.txt", "r") as file:
        real_input = file.read()

    return example, real_input


def part_1(data: str) -> None:

    lines = data.splitlines()

    patterns = set(lines[0].split(", "))
    maxlen = max(map(len, patterns))

    @cache
    def can_obtain(design):
        if design == "":
            return True
        for i in range(min(len(design), maxlen) + 1):
            if design[:i] in patterns and can_obtain(design[i:]):
                return True
        return False

    print("Part 1 is:", sum(1 if can_obtain(design) else 0 for design in lines[2:]))


def part_2(data: str) -> None:
    lines = data.splitlines()

    patterns = set(lines[0].split(", "))
    maxlen = max(map(len, patterns))

    @cache
    def num_possibilities(design):
        if design == "":
            return 1
        count = 0
        for i in range(min(len(design), maxlen) + 1):
            if design[:i] in patterns:
                count += num_possibilities(design[i:])
        return count

    print("Part 2 is:", sum(num_possibilities(design) for design in lines[2:]))


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
