import time


def part1(input_data):
    DIRECTIONS = {"U": (-1, 0), "D": (1, 0), "L": (0, -1), "R": (0, 1)}
    instructions = [
        tuple(inst for inst in line.strip().split(" "))
        for line in input_data.split("\n")
    ]
    corner_count = 0
    corners = [(0, 0)]
    for dire, length, _ in instructions:
        dr, dc = DIRECTIONS[dire]
        length = int(length)
        r, c = corners[-1]
        nr, nc = r + dr * length, c + dc * length
        corner_count += length
        if (nr, nc) == (0, 0):
            break
        corners.append((nr, nc))

    # pick theorem + shoelace theorem
    area = abs(
        sum(
            corners[i][0] * (corners[i - 1][1] - corners[(i + 1) % len(corners)][1])
            for i, _ in enumerate(corners)
        )
        / 2
    )
    total_area = area + corner_count / 2 + 1
    return total_area


def part2(input_data):
    DIRECTIONS = {0: (0, 1), 1: (1, 0), 2: (0, -1), 3: (-1, 0)}
    instructions = [
        tuple(inst for inst in line.strip().split(" "))
        for line in input_data.split("\n")
    ]
    corner_count = 0
    corners = [(0, 0)]
    for _, _, color in instructions:
        dire = int(color[-2])
        dr, dc = DIRECTIONS[dire]
        length = int(color[2:-2], 16)
        r, c = corners[-1]
        nr, nc = r + dr * length, c + dc * length
        corner_count += length
        if (nr, nc) == (0, 0):
            break
        corners.append((nr, nc))

    # pick theorem + shoelace theorem
    area = abs(
        sum(
            corners[i][0] * (corners[i - 1][1] - corners[(i + 1) % len(corners)][1])
            for i, _ in enumerate(corners)
        )
        / 2
    )
    total_area = area + corner_count / 2 + 1
    return total_area


def main() -> None:
    with open("2023/Day_18.txt", "r") as file:
        input_data = file.read()

    # Part 1
    result1 = part1(input_data)
    print(f"Result 1 is: {result1}")

    # Part 2
    result2 = part2(input_data)
    print(f"Result 2 is: {result2}\n")


if __name__ == "__main__":
    start = time.perf_counter()
    main()
    end = time.perf_counter()
    print(f"Executed in: {end - start} s")
