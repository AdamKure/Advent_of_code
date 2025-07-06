import time
from functools import cache

DAY = 11


def read_files(day: int) -> tuple[str, str]:
    with open(f"2024/Day_{day:02}_example.txt", "r") as file:
        example = file.read()

    with open(f"2024/Day_{day:02}.txt", "r") as file:
        real_input = file.read()

    return example, real_input


def part_1(data: str) -> None:
    stones = [int(x) for x in data.split()]

    for _ in range(25):
        output = []
        for stone in stones:
            if stone == 0:
                output.append(1)
                continue
            string = str(stone)
            length = len(string)
            if length % 2 == 0:
                output.append(int(string[: length // 2]))
                output.append(int(string[length // 2 :]))
            else:
                output.append(stone * 2024)
        stones = output

    print("Part 1 is:", len(stones))


def part_2(data: str) -> None:

    stones = [int(x) for x in data.split()]

    @cache
    def count(stone, steps):
        if steps == 0:
            return 1
        if stone == 0:
            return count(1, steps - 1)
        string = str(stone)
        length = len(string)
        if length % 2 == 0:
            return count(int(string[: length // 2]), steps - 1) + count(
                int(string[length // 2 :]), steps - 1
            )
        return count(stone * 2024, steps - 1)

    print("Part 2 is:", sum(count(stone, 75) for stone in stones))


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
