import time
from collections import deque

DAY = 12


def read_files(day: int) -> tuple[str, str]:
    with open(f"2024/Day_{day:02}_example.txt", "r") as file:
        example = file.readlines()

    with open(f"2024/Day_{day:02}.txt", "r") as file:
        real_input = file.readlines()

    return example, real_input


def part_1(data: str) -> None:
    from collections import deque

    grid = [list(line.strip()) for line in data]

    rows = len(grid)
    cols = len(grid[0])

    regions = []
    seen = set()

    for r in range(rows):
        for c in range(cols):
            if (r, c) in seen:
                continue
            seen.add((r, c))
            region = {(r, c)}
            q = deque([(r, c)])
            crop = grid[r][c]
            while q:
                cr, cc = q.popleft()
                for nr, nc in [(cr - 1, cc), (cr + 1, cc), (cr, cc - 1), (cr, cc + 1)]:
                    if nr < 0 or nc < 0 or nr >= rows or nc >= cols:
                        continue
                    if grid[nr][nc] != crop:
                        continue
                    if (nr, nc) in region:
                        continue
                    region.add((nr, nc))
                    q.append((nr, nc))
            seen |= region
            regions.append(region)

    def perimeter(region):
        output = 0
        for r, c in region:
            output += 4
            for nr, nc in [(r + 1, c), (r - 1, c), (r, c - 1), (r, c + 1)]:
                if (nr, nc) in region:
                    output -= 1
        return output

    print("Part 1 is:", sum(len(region) * perimeter(region) for region in regions))


def part_2(data: str) -> None:
    grid = [list(line.strip()) for line in data]

    rows = len(grid)
    cols = len(grid[0])

    regions = []
    seen = set()

    for r in range(rows):
        for c in range(cols):
            if (r, c) in seen:
                continue
            seen.add((r, c))
            region = {(r, c)}
            q = deque([(r, c)])
            crop = grid[r][c]
            while q:
                cr, cc = q.popleft()
                for nr, nc in [(cr - 1, cc), (cr + 1, cc), (cr, cc - 1), (cr, cc + 1)]:
                    if nr < 0 or nc < 0 or nr >= rows or nc >= cols:
                        continue
                    if grid[nr][nc] != crop:
                        continue
                    if (nr, nc) in region:
                        continue
                    region.add((nr, nc))
                    q.append((nr, nc))
            seen |= region
            regions.append(region)

    def sides(region):
        corner_candidates = set()
        for r, c in region:
            for cr, cc in [
                (r - 0.5, c - 0.5),
                (r + 0.5, c - 0.5),
                (r + 0.5, c + 0.5),
                (r - 0.5, c + 0.5),
            ]:
                corner_candidates.add((cr, cc))
        corners = 0
        for cr, cc in corner_candidates:
            config = [
                (sr, sc) in region
                for sr, sc in [
                    (cr - 0.5, cc - 0.5),
                    (cr + 0.5, cc - 0.5),
                    (cr + 0.5, cc + 0.5),
                    (cr - 0.5, cc + 0.5),
                ]
            ]
            number = sum(config)
            if number == 1:
                corners += 1
            elif number == 2:
                if config == [True, False, True, False] or config == [
                    False,
                    True,
                    False,
                    True,
                ]:
                    corners += 2
            elif number == 3:
                corners += 1
        return corners

    print("Part 2 is:", sum(len(region) * sides(region) for region in regions))


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
