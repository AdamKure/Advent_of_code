import re
import time

DAY = 13


def read_files(day: int) -> tuple[str, str]:
    with open(f"2024/Day_{day:02}_example.txt", "r") as file:
        example = file.read()

    with open(f"2024/Day_{day:02}.txt", "r") as file:
        real_input = file.read()

    return example, real_input


def part_1(data: str) -> None:
    total = 0

    for block in data.split("\n\n"):
        ax, ay, bx, by, px, py = map(int, re.findall(r"\d+", block))
        ca = (px * by - py * bx) / (ax * by - ay * bx)
        cb = (px - ax * ca) / bx
        if ca % 1 == cb % 1 == 0:
            if ca <= 100 and cb <= 100:
                total += int(ca * 3 + cb)

    print("Part 1 is:", total)


def part_2(data: str) -> None:
    total = 0

    for block in data.split("\n\n"):
        ax, ay, bx, by, px, py = map(int, re.findall(r"\d+", block))
        px += 10000000000000
        py += 10000000000000
        ca = (px * by - py * bx) / (ax * by - ay * bx)
        cb = (px - ax * ca) / bx
        if ca % 1 == cb % 1 == 0:
            total += int(ca * 3 + cb)

    print("Part 2 is:", total)


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
