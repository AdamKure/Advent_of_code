import time

DAY = 2


def read_files(day: int) -> tuple[str, str]:
    with open(f"2024/Day_{day:02}_example.txt", "r") as file:
        example = file.read()

    with open(f"2024/Day_{day:02}.txt", "r") as file:
        real_input = file.read()

    return example, real_input


def is_safe(levels):
    if len(levels) < 2:
        return False
    diffs = [x - y for x, y in zip(levels, levels[1:])]
    return all(1 <= x <= 3 for x in diffs) or all(-3 <= x <= -1 for x in diffs)


def part_1(data: str) -> None:
    count = 0

    for line in data.split("\n"):
        levels = list(map(int, line.split()))
        if is_safe(levels):
            count += 1

    print(f"Part 1 is: {count}")


def part_2(data: str) -> None:
    count = 0

    for line in data.split("\n"):
        levels = list(map(int, line.split()))
        if any(
            is_safe(levels[:index] + levels[index + 1 :])
            for index in range(len(levels))
        ):
            count += 1

    print(f"Part 2 is: {count}")


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
