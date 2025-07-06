import time
from collections import deque

DAY = 10


def read_files(day: int) -> tuple[str, str]:
    with open(f"2024/Day_{day:02}_example.txt", "r") as file:
        example = file.readlines()

    with open(f"2024/Day_{day:02}.txt", "r") as file:
        real_input = file.readlines()

    return example, real_input


def part_1(data: str) -> None:
    grid = [[int(char) for char in line.strip()] for line in data]

    rows = len(grid)
    cols = len(grid[0])

    trailheads = [(r, c) for r in range(rows) for c in range(cols) if grid[r][c] == 0]

    def score(grid, r, c):
        q = deque([(r, c)])
        seen = {(r, c)}
        summits = 0
        while len(q) > 0:
            cr, cc = q.popleft()
            for nr, nc in [(cr - 1, cc), (cr, cc + 1), (cr + 1, cc), (cr, cc - 1)]:
                if nr < 0 or nc < 0 or nr >= rows or nc >= cols:
                    continue
                if grid[nr][nc] != grid[cr][cc] + 1:
                    continue
                if (nr, nc) in seen:
                    continue
                seen.add((nr, nc))
                if grid[nr][nc] == 9:
                    summits += 1
                else:
                    q.append((nr, nc))
        return summits

    print("Result 1 is:", sum(score(grid, r, c) for r, c in trailheads))


def part_2(data: str) -> None:
    grid = [[int(char) for char in line.strip()] for line in data]

    rows = len(grid)
    cols = len(grid[0])

    trailheads = [(r, c) for r in range(rows) for c in range(cols) if grid[r][c] == 0]

    def score(grid, r, c):
        q = deque([(r, c)])
        seen = {(r, c): 1}
        trails = 0
        while len(q) > 0:
            cr, cc = q.popleft()
            if grid[cr][cc] == 9:
                trails += seen[(cr, cc)]
            for nr, nc in [(cr - 1, cc), (cr, cc + 1), (cr + 1, cc), (cr, cc - 1)]:
                if nr < 0 or nc < 0 or nr >= rows or nc >= cols:
                    continue
                if grid[nr][nc] != grid[cr][cc] + 1:
                    continue
                if (nr, nc) in seen:
                    seen[(nr, nc)] += seen[(cr, cc)]
                    continue
                seen[(nr, nc)] = seen[(cr, cc)]
                q.append((nr, nc))
        return trails

    print("Part 2 is:", sum(score(grid, r, c) for r, c in trailheads))


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
