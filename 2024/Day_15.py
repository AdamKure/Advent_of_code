import time

DAY = 15


def read_files(day: int) -> tuple[str, str]:
    with open(f"2024/Day_{day:02}_example.txt", "r") as file:
        example = file.read()

    with open(f"2024/Day_{day:02}.txt", "r") as file:
        real_input = file.read()

    return example, real_input


def part_1(data: str) -> None:
    top, bottom = data.split("\n\n")

    grid = [list(line) for line in top.splitlines()]
    moves = bottom.replace("\n", "")

    rows = len(grid)
    cols = len(grid[0])

    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == "@":
                break
        else:
            continue
        break

    for move in moves:
        dr = {"^": -1, "v": 1}.get(move, 0)
        dc = {"<": -1, ">": 1}.get(move, 0)
        targets = [(r, c)]
        cr = r
        cc = c
        go = True
        while True:
            cr += dr
            cc += dc
            char = grid[cr][cc]
            if char == "#":
                go = False
                break
            if char == "O":
                targets.append((cr, cc))
            if char == ".":
                break
        if not go:
            continue
        grid[r][c] = "."
        grid[r + dr][c + dc] = "@"
        for br, bc in targets[1:]:
            grid[br + dr][bc + dc] = "O"
        r += dr
        c += dc

    print(
        "Part 1 is:",
        sum(100 * r + c for r in range(rows) for c in range(cols) if grid[r][c] == "O"),
    )


def part_2(data: str) -> None:
    top, bottom = data.split("\n\n")

    expansion = {"#": "##", "O": "[]", ".": "..", "@": "@."}

    grid = [
        list("".join(expansion[char] for char in line)) for line in top.splitlines()
    ]
    moves = bottom.replace("\n", "")

    rows = len(grid)
    cols = len(grid[0])

    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == "@":
                break
        else:
            continue
        break

    for move in moves:
        dr = {"^": -1, "v": 1}.get(move, 0)
        dc = {"<": -1, ">": 1}.get(move, 0)
        targets = [(r, c)]
        go = True
        for cr, cc in targets:
            nr = cr + dr
            nc = cc + dc
            if (nr, nc) in targets:
                continue
            char = grid[nr][nc]
            if char == "#":
                go = False
                break
            if char == "[":
                targets.append((nr, nc))
                targets.append((nr, nc + 1))
            if char == "]":
                targets.append((nr, nc))
                targets.append((nr, nc - 1))
        if not go:
            continue
        copy = [list(row) for row in grid]
        grid[r][c] = "."
        grid[r + dr][c + dc] = "@"
        for br, bc in targets[1:]:
            grid[br][bc] = "."
        for br, bc in targets[1:]:
            grid[br + dr][bc + dc] = copy[br][bc]
        r += dr
        c += dc

    print(
        "Part 2 is:",
        sum(100 * r + c for r in range(rows) for c in range(cols) if grid[r][c] == "["),
    )


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
