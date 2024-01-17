import time
from typing import Dict, List, Tuple


def find_axies(pattern: str) -> Tuple[int, int]:
    lines = pattern.split("\n")
    cols = len(lines[0])
    axis_vert = []
    axis_hor = []
    for line in lines:
        if axis_vert:
            axis_vert = find_symetry(line, axis_vert)
        else:
            axis_vert = find_symetry(line)
        if not axis_vert:
            break

    for col in range(cols):
        subpattern = "".join(line[col] for line in lines)
        if axis_hor:
            axis_hor = find_symetry(subpattern, axis_hor)
        else:
            axis_hor = find_symetry(subpattern)
        if not axis_hor:
            break

    if len(axis_vert) == 1:
        vertical = axis_vert[0]
    else:
        vertical = 0
    if len(axis_hor) == 1:
        horizontal = axis_hor[0]
    else:
        horizontal = 0
    return vertical, horizontal


def find_symetry(pattern: str, positions: List[int] = None) -> int:
    if positions is None:
        positions = range(1, len(pattern))
    cols = len(pattern)
    symetries = []
    for pos in positions:
        pos_left = pos - 1
        pos_right = pos
        is_symetric = True
        while 0 <= pos_left < cols - 1 and 1 <= pos_right < cols:
            if pattern[pos_left] != pattern[pos_right]:
                is_symetric = False
                break
            pos_left -= 1
            pos_right += 1
        if is_symetric:
            symetries.append(pos)
    return symetries


def fix_smudge(pattern: str):
    def find_smudge(subpattern: str, positions: Dict[int, int] = None) -> int:
        cols = len(subpattern)
        for pos in positions:
            pos_left = pos - 1
            pos_right = pos
            while 0 <= pos_left < cols - 1 and 1 <= pos_right < cols:
                if subpattern[pos_left] != subpattern[pos_right]:
                    positions[pos] += 1
                if positions[pos] == 2:
                    break
                pos_left -= 1
                pos_right += 1
        return {key: val for key, val in positions.items() if val < 2}

    lines = pattern.split("\n")
    rows = len(lines)
    cols = len(lines[0])
    positions_row = {pos: 0 for pos in range(1, rows)}
    positions_col = {pos: 0 for pos in range(1, cols)}
    for line in lines:
        positions_col = find_smudge(line, positions_col)
    for col in range(cols):
        subpattern = "".join(line[col] for line in lines)
        positions_row = find_smudge(subpattern, positions_row)
    col = [key for key, val in positions_col.items() if val == 1]
    row = [key for key, val in positions_row.items() if val == 1]
    col = col[0] if col else 0
    row = row[0] if row else 0
    return col, row


def main():
    with open("2023\\Day_13.txt", "r") as file:
        input_data = file.read()
        patterns = input_data.split("\n\n")

    # Part 1
    result1 = 0
    for pattern in patterns:
        vert, hor = find_axies(pattern)
        result1 += vert + 100 * hor
    print(f"Result 1 is: {result1}")

    # Part 2
    result2 = 0
    for pattern in patterns:
        new_vert, new_hor = fix_smudge(pattern)
        result2 += new_vert + 100 * new_hor
    print(f"Result 2 is: {result2}")


if __name__ == "__main__":
    start = time.perf_counter()
    main()
    end = time.perf_counter()
    print(f"\nExecuted in: {end - start} s")
