import time

DAY = 25


def read_files(day: int) -> tuple[str, str]:
    with open(f"2024/Day_{day:02}_example.txt", "r") as file:
        example = file.read()

    with open(f"2024/Day_{day:02}.txt", "r") as file:
        real_input = file.read()

    return example, real_input


def part_1(data: str) -> None:
    locks = []
    keys = []

    for block in data.split("\n\n"):
        grid = list(zip(*block.splitlines()))
        if grid[0][0] == "#":
            locks.append([row.count("#") - 1 for row in grid])
        else:
            keys.append([row.count("#") - 1 for row in grid])

    total = 0

    for lock in locks:
        for key in keys:
            if all(x + y <= 5 for x, y in zip(lock, key)):
                total += 1

    print("Part 1 is:", total)


def main() -> None:
    example, real_input = read_files(DAY)

    part_1(example)
    part_1(real_input)


if __name__ == "__main__":
    start = time.perf_counter()
    main()
    end = time.perf_counter()
    print(f"\nExecuted in: {end - start} s")
