import time
from itertools import combinations

DAY = 8


def read_files(day: int) -> tuple[str, str]:
    with open(f"2024/Day_{day:02}_example.txt", "r") as file:
        example = file.readlines()

    with open(f"2024/Day_{day:02}.txt", "r") as file:
        real_input = file.readlines()

    return example, real_input


def part_1(data: str) -> None:
    grid = [line.strip() for line in data]

    rows = len(grid)
    cols = len(grid[0])

    antennas = {}

    for r, row in enumerate(grid):
        for c, char in enumerate(row):
            if char != ".":
                if char not in antennas:
                    antennas[char] = []
                antennas[char].append((r, c))

    antinodes = set()

    for array in antennas.values():
        for (r1, c1), (r2, c2) in combinations(array, 2):
            antinodes.add((2 * r1 - r2, 2 * c1 - c2))
            antinodes.add((2 * r2 - r1, 2 * c2 - c1))

    antinodes_in_grid = sum(1 for r, c in antinodes if 0 <= r < rows and 0 <= c < cols)

    print(f"Part 1 is: {antinodes_in_grid}")


def part_2(data: str) -> None:
    grid = [line.strip() for line in data]

    rows = len(grid)
    cols = len(grid[0])

    antennas = {}

    for r, row in enumerate(grid):
        for c, char in enumerate(row):
            if char != ".":
                if char not in antennas:
                    antennas[char] = []
                antennas[char].append((r, c))

    antinodes = set()

    for array in antennas.values():
        for i, sub_a in enumerate(array):
            r1, c1 = sub_a
            for j, sub_b in enumerate(array):
                if i == j:
                    continue
                r2, c2 = sub_b
                dr = r2 - r1
                dc = c2 - c1
                r = r1
                c = c1
                while 0 <= r < rows and 0 <= c < cols:
                    antinodes.add((r, c))
                    r += dr
                    c += dc

    print(f"Part 2 is: {len(antinodes)}")


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
