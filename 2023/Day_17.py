import time
from heapq import heappop, heappush


def djikstra1(grid):
    visited = set()
    total_h = 0
    # heat, row, col, dr, dc, step
    queue = [(0, 0, 0, 0, 0, 0)]
    while queue:
        h, r, c, dr, dc, s = heappop(queue)
        if r == len(grid) - 1 and c == len(grid[0]) - 1:
            total_h = h
            break

        if (r, c, dr, dc, s) in visited:
            continue
        visited.add((r, c, dr, dc, s))

        if s < 3 and (dr, dc) != (0, 0):
            nr = r + dr
            nc = c + dc
            if 0 <= nr < len(grid) and 0 <= nc < len(grid[0]):
                nh = h + grid[nr][nc]
                heappush(queue, (nh, nr, nc, dr, dc, s + 1))

        for ndr, ndc in [(-1, 0), (0, -1), (0, 1), (1, 0)]:
            if (ndr, ndc) != (-dr, -dc) and (ndr, ndc) != (dr, dc):
                nr = r + ndr
                nc = c + ndc
                if 0 <= nr < len(grid) and 0 <= nc < len(grid[0]):
                    nh = h + grid[nr][nc]
                    heappush(queue, (nh, nr, nc, ndr, ndc, 1))
    if not total_h:
        raise RuntimeError("No route found")
    return total_h


def djikstra2(grid):
    visited = set()
    total_h = 0
    # heat, row, col, dr, dc, step
    queue = [(0, 0, 0, 0, 0, 0)]
    while queue:
        h, r, c, dr, dc, s = heappop(queue)
        if r == len(grid) - 1 and c == len(grid[0]) - 1 and s >= 4:
            total_h = h
            break

        if (r, c, dr, dc, s) in visited:
            continue
        visited.add((r, c, dr, dc, s))

        if s < 10 and (dr, dc) != (0, 0):
            nr = r + dr
            nc = c + dc
            if 0 <= nr < len(grid) and 0 <= nc < len(grid[0]):
                nh = h + grid[nr][nc]
                heappush(queue, (nh, nr, nc, dr, dc, s + 1))

        if s < 4 and (dr, dc) != (0, 0):
            continue
        for ndr, ndc in [(-1, 0), (0, -1), (0, 1), (1, 0)]:
            if (ndr, ndc) != (-dr, -dc) and (ndr, ndc) != (dr, dc):
                nr = r + ndr
                nc = c + ndc
                if 0 <= nr < len(grid) and 0 <= nc < len(grid[0]):
                    nh = h + grid[nr][nc]
                    heappush(queue, (nh, nr, nc, ndr, ndc, 1))
    if not total_h:
        raise RuntimeError("No route found")
    return total_h


def main() -> None:
    with open("2023/Day_17.txt", "r") as file:
        input_data = file.read().split("\n")

    # Part 1
    grid = [list(map(int, line.strip())) for line in input_data]
    result1 = djikstra1(grid)
    print(f"Result 1 is: {result1}")

    # Part 2
    result2 = djikstra2(grid)
    print(f"Result 2 is: {result2}")


if __name__ == "__main__":
    start = time.perf_counter()
    main()
    end = time.perf_counter()
    print(f"\nExecuted in: {end - start} s")
