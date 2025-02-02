import time

DAY = 4


def read_files(day: int) -> tuple[str, str]:
    with open(f"2024/Day_{day:02}_example.txt", "r") as file:
        example = file.read()

    with open(f"2024/Day_{day:02}.txt", "r") as file:
        real_input = file.read()

    return example, real_input


def part_1(data: str) -> None:
    grid = data.split("\n")
    count = 0
    for r, row in enumerate(grid):
        for c, col in enumerate(grid[r]):
            if col != "X":
                continue
            for dr in [-1, 0, 1]:
                for dc in [-1, 0, 1]:
                    if dr == dc == 0:
                        continue
                    if not (
                        0 <= r + 3 * dr < len(grid) and 0 <= c + 3 * dc < len(grid[0])
                    ):
                        continue
                    if (
                        grid[r + dr][c + dc] == "M"
                        and grid[r + 2 * dr][c + 2 * dc] == "A"
                        and grid[r + 3 * dr][c + 3 * dc] == "S"
                    ):
                        count += 1

    print(f"Part 1 is: {count}")


def part_2(data: str) -> None:
    grid = data.split("\n")
    count = 0
    for r in range(1, len(grid) - 1):
        for c in range(1, len(grid[0]) - 1):
            if grid[r][c] != "A":
                continue
            corners = [
                grid[r - 1][c - 1],
                grid[r - 1][c + 1],
                grid[r + 1][c + 1],
                grid[r + 1][c - 1],
            ]
            if "".join(corners) in ["MMSS", "MSSM", "SSMM", "SMMS"]:
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
