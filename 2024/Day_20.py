import time

DAY = 20


def read_files(day: int) -> tuple[str, str]:
    with open(f"2024/Day_{day:02}_example.txt", "r") as file:
        example = file.read()

    with open(f"2024/Day_{day:02}.txt", "r") as file:
        real_input = file.read()

    return example, real_input


def part_1(data: str) -> None:
    grid = [list(line.strip()) for line in data.split("\n")]

    rows = len(grid)
    cols = len(grid[0])

    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == "S":
                break
        else:
            continue
        break

    dists = [[-1] * cols for _ in range(rows)]
    dists[r][c] = 0

    while grid[r][c] != "E":
        for nr, nc in [(r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1)]:
            if nr < 0 or nc < 0 or nr >= rows or nc >= cols:
                continue
            if grid[nr][nc] == "#":
                continue
            if dists[nr][nc] != -1:
                continue
            dists[nr][nc] = dists[r][c] + 1
            r = nr
            c = nc

    count = 0

    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == "#":
                continue
            for nr, nc in [(r + 2, c), (r + 1, c + 1), (r, c + 2), (r - 1, c + 1)]:
                if nr < 0 or nc < 0 or nr >= rows or nc >= cols:
                    continue
                if grid[nr][nc] == "#":
                    continue
                if abs(dists[r][c] - dists[nr][nc]) >= 102:
                    count += 1

    print("Part 1 is:", count)


def part_2(data: str) -> None:
    grid = [list(line.strip()) for line in data.split("\n")]

    rows = len(grid)
    cols = len(grid[0])

    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == "S":
                break
        else:
            continue
        break

    path = [(r, c)]

    while grid[r][c] != "E":
        grid[r][c] = "#"
        for nr, nc in [(r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1)]:
            if nr < 0 or nc < 0 or nr >= rows or nc >= cols:
                continue
            if grid[nr][nc] == "#":
                continue
            path.append((nr, nc))
            r = nr
            c = nc

    count = 0

    for i, (r, c) in enumerate(path):
        for j, (nr, nc) in enumerate(path[i + 101 :]):
            radius = abs(r - nr) + abs(c - nc)
            if radius > 20:
                continue
            if j + 1 >= radius:
                count += 1

    print("Part 2 is:", count)


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
