import heapq
import time
from collections import deque

DAY = 16


def read_files(day: int) -> tuple[str, str]:
    with open(f"2024/Day_{day:02}_example.txt", "r") as file:
        example = file.read().split("\n")

    with open(f"2024/Day_{day:02}.txt", "r") as file:
        real_input = file.read().split("\n")

    return example, real_input


def part_1(data: str) -> None:
    grid = [list(line.strip()) for line in data]

    rows = len(grid)
    cols = len(grid[0])

    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == "S":
                sr = r
                sc = c
                break
        else:
            continue
        break

    pq = [(0, sr, sc, 0, 1)]
    seen = {(sr, sc, 0, 1)}

    while pq:
        cost, r, c, dr, dc = heapq.heappop(pq)
        seen.add((r, c, dr, dc))
        if grid[r][c] == "E":
            result = cost
            break
        for new_cost, nr, nc, ndr, ndc in [
            (cost + 1, r + dr, c + dc, dr, dc),
            (cost + 1000, r, c, dc, -dr),
            (cost + 1000, r, c, -dc, dr),
        ]:
            if grid[nr][nc] == "#":
                continue
            if (nr, nc, ndr, ndc) in seen:
                continue
            heapq.heappush(pq, (new_cost, nr, nc, ndr, ndc))

    print("Part 1 is:", result)


def part_2(data: str) -> None:
    grid = [list(line.strip()) for line in data]

    rows = len(grid)
    cols = len(grid[0])

    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == "S":
                sr = r
                sc = c
                break
        else:
            continue
        break

    pq = [(0, sr, sc, 0, 1)]
    lowest_cost = {(sr, sc, 0, 1): 0}
    backtrack = {}
    best_cost = float("inf")
    end_states = set()

    while pq:
        cost, r, c, dr, dc = heapq.heappop(pq)
        if cost > lowest_cost.get((r, c, dr, dc), float("inf")):
            continue
        if grid[r][c] == "E":
            if cost > best_cost:
                break
            best_cost = cost
            end_states.add((r, c, dr, dc))
        for new_cost, nr, nc, ndr, ndc in [
            (cost + 1, r + dr, c + dc, dr, dc),
            (cost + 1000, r, c, dc, -dr),
            (cost + 1000, r, c, -dc, dr),
        ]:
            if grid[nr][nc] == "#":
                continue
            lowest = lowest_cost.get((nr, nc, ndr, ndc), float("inf"))
            if new_cost > lowest:
                continue
            if new_cost < lowest:
                backtrack[(nr, nc, ndr, ndc)] = set()
                lowest_cost[(nr, nc, ndr, ndc)] = new_cost
            backtrack[(nr, nc, ndr, ndc)].add((r, c, dr, dc))
            heapq.heappush(pq, (new_cost, nr, nc, ndr, ndc))

    states = deque(end_states)
    seen = set(end_states)

    while states:
        key = states.popleft()
        for last in backtrack.get(key, []):
            if last in seen:
                continue
            seen.add(last)
            states.append(last)

    print("Part 2 is:", len({(r, c) for r, c, _, _ in seen}))


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
