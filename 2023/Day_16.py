import time


def main() -> None:
    with open("2023/Day_16.txt", "r") as file:
        input_data = file.read()

    def move(start_pos):
        rows, cols = len(grid), len(grid[0])
        visited = set()
        moves = [start_pos]
        while moves:
            r, c, dr, dc = moves.pop()
            r += dr
            c += dc
            if r < 0 or r >= rows or c < 0 or c >= cols:
                continue
            char = grid[r][c]
            if char == "." or char == "|" and dr != 0 or char == "-" and dc != 0:
                if (r, c, dr, dc) not in visited:
                    visited.add((r, c, dr, dc))
                    moves.append((r, c, dr, dc))
            elif char == "\\":
                dr, dc = dc, dr
                visited.add((r, c, dr, dc))
                moves.append((r, c, dr, dc))
            elif char == "/":
                dr, dc = -dc, -dr
                visited.add((r, c, dr, dc))
                moves.append((r, c, dr, dc))
            else:
                for dr, dc in [(-1, 0), (1, 0)] if char == "|" else [(0, -1), (0, 1)]:
                    if (r, c, dr, dc) not in visited:
                        visited.add((r, c, dr, dc))
                        moves.append((r, c, dr, dc))
        return len({(r, c) for r, c, _, _ in visited})

    # Part 1
    grid = input_data.split("\n")
    start_pos = (0, -1, 0, 1)
    result1 = move(start_pos)
    print(f"Result 1 is: {result1}")

    # Part 2
    results = []
    for r in range(len(grid)):
        results.append(move((r, -1, 0, 1)))
        results.append(move((r, len(grid[0]), 0, -1)))
    for c in range(len(grid[0])):
        results.append(move((-1, c, 1, 0)))
        results.append(move((len(grid) + 1, c, -1, 0)))
    result2 = max(results)
    print(f"Result 2 is: {result2}")


if __name__ == "__main__":
    start = time.perf_counter()
    main()
    end = time.perf_counter()
    print(f"\nExecuted in: {end - start} s")
