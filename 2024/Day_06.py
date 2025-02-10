import time

DAY = 6


def read_files(day: int) -> tuple[str, str]:
    with open(f"2024/Day_{day:02}_example.txt", "r") as file:
        example = file.read()

    with open(f"2024/Day_{day:02}.txt", "r") as file:
        real_input = file.read()

    return example, real_input


def part_1(data: str) -> None:
    grid = list(map(list, data.splitlines()))

    rows = len(grid)
    cols = len(grid[0])

    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == "^":
                break
        else:
            continue
        break

    dr = -1
    dc = 0

    seen = set()

    while True:
        seen.add((r, c))
        if r + dr < 0 or r + dr >= rows or c + dc < 0 or c + dc >= cols:
            break
        if grid[r + dr][c + dc] == "#":
            dc, dr = -dr, dc
        else:
            r += dr
            c += dc

    print(f"Part 1 is: {len(seen)}")


def part_2(data: str) -> None:
    grid = list(map(list, data.splitlines()))

    rows = len(grid)
    cols = len(grid[0])

    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == "^":
                break
        else:
            continue
        break

    sr = r
    sc = c

    dr = -1
    dc = 0

    positions = set()

    while True:
        positions.add((r, c))
        if r + dr < 0 or r + dr >= rows or c + dc < 0 or c + dc >= cols:
            break
        if grid[r + dr][c + dc] == "#":
            dc, dr = -dr, dc
        else:
            r += dr
            c += dc

    def loops(grid, r, c):
        dr = -1
        dc = 0

        seen = set()

        while True:
            seen.add((r, c, dr, dc))
            if r + dr < 0 or r + dr >= rows or c + dc < 0 or c + dc >= cols:
                return False
            if grid[r + dr][c + dc] == "#":
                dc, dr = -dr, dc
            else:
                r += dr
                c += dc
            if (r, c, dr, dc) in seen:
                return True

    count = 0

    for cr, cc in positions:
        if grid[cr][cc] != ".":
            continue
        grid[cr][cc] = "#"
        if loops(grid, sr, sc):
            count += 1
        grid[cr][cc] = "."

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
