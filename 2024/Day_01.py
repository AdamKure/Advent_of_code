import time
from collections import Counter


def read_files(day: int) -> tuple[str, str]:
    with open(f"2024/Day_{day:02}_example.txt", "r") as file:
        example = file.read()

    with open(f"2024/Day_{day:02}.txt", "r") as file:
        real_input = file.read()

    return example, real_input


def part_1(data: str) -> None:
    lines = data.split("\n")
    a = sorted(map(int, (line.split("  ")[0] for line in lines)))
    b = sorted(map(int, (line.split("  ")[1] for line in lines)))

    total = sum(abs(x - y) for x, y in zip(a, b))

    print(f"Part 1 is: {total}")


def part_2(data: str) -> None:
    lines = data.split("\n")
    a = map(int, (line.split("  ")[0] for line in lines))
    b = map(int, (line.split("  ")[1] for line in lines))

    c = Counter(b)
    total = sum(num * c[num] for num in a)

    print(f"Part 2 is: {total}")


def main() -> None:
    day = 1
    example, real_input = read_files(day)

    part_1(example)
    part_1(real_input)

    part_2(example)
    part_2(real_input)


if __name__ == "__main__":
    start = time.perf_counter()
    main()
    end = time.perf_counter()
    print(f"\nExecuted in: {end - start} s")
