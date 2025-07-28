import time
from collections import deque

DAY = 18


def read_files(day: int) -> tuple[str, str]:
    with open(f"2024/Day_{day:02}_example.txt", "r") as file:
        example = file.read()

    with open(f"2024/Day_{day:02}.txt", "r") as file:
        real_input = file.read()

    return example, real_input


def part_1(data: str) -> None:
    s = 70
    n = 1024

    grid = [[0] * (s + 1) for _ in range(s + 1)]
    coords = [list(map(int, line.split(","))) for line in data.split("\n")]

    for c, r in coords[:n]:
        grid[r][c] = 1

    q = deque([(0, 0, 0)])
    seen = {(0, 0)}

    while q:
        r, c, d = q.popleft()
        for nr, nc in [(r + 1, c), (r, c + 1), (r - 1, c), (r, c - 1)]:
            if nr < 0 or nc < 0 or nr > s or nc > s:
                continue
            if grid[nr][nc] == 1:
                continue
            if (nr, nc) in seen:
                continue
            if nr == nc == s:
                print("Part 1 is:", d + 1)
                return
            seen.add((nr, nc))
            q.append((nr, nc, d + 1))


def part_2(data: str) -> None:
    s = 71

    walls = [tuple(map(int, line.split(","))) for line in data.split("\n")]

    wset = set(walls)
    seen = set(wset)

    parent_grid = [[None] * s for _ in range(s)]

    for r in range(s):
        for c in range(s):
            if (r, c) in seen:
                continue
            search = {(r, c)}
            seen.add((r, c))
            while search:
                cr, cc = search.pop()
                for nr, nc in [(cr - 1, cc), (cr + 1, cc), (cr, cc - 1), (cr, cc + 1)]:
                    if nr < 0 or nc < 0 or nr >= s or nc >= s:
                        continue
                    if (nr, nc) in seen:
                        continue
                    search.add((nr, nc))
                    seen.add((nr, nc))
                    parent_grid[nr][nc] = (r, c)

    def find(r, c):
        parent = parent_grid[r][c]
        if parent is None:
            return (r, c)
        parent_grid[r][c] = find(*parent)
        return parent_grid[r][c]

    def union(r1, c1, r2, c2):
        r1, c1 = find(r1, c1)
        r2, c2 = find(r2, c2)
        if (r1, c1) == (r2, c2):
            return
        parent_grid[r2][c2] = (r1, c1)

    last_blocking_coords = None

    for wr, wc in walls[::-1]:
        wset.remove((wr, wc))

        for nr, nc in [(wr - 1, wc), (wr + 1, wc), (wr, wc - 1), (wr, wc + 1)]:
            if nr < 0 or nc < 0 or nr >= s or nc >= s:
                continue
            if (nr, nc) in wset:
                continue
            union(wr, wc, nr, nc)

        if find(0, 0) == find(s - 1, s - 1):
            print("Part 2 is:", f"{wr},{wc}")
            break


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
