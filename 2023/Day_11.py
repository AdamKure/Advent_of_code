import copy
import time
from typing import List, Tuple

DUMMY = "...#......\n\
.......#..\n\
#.........\n\
..........\n\
......#...\n\
.#........\n\
.........#\n\
..........\n\
.......#..\n\
#...#....."


def calculate_shortest_paths(galaxies: List[List[int]]) -> List[int]:
    dist = []
    for i, gal1 in enumerate(galaxies[:-1]):
        for gal2 in galaxies[i + 1 :]:
            dist.append(abs(gal1[0] - gal2[0]) + abs(gal1[1] - gal2[1]))
    return dist


def compansate_for_expansion(
    galaxy_map: List[str], expansion_rate: int
) -> List[List[int]]:
    galaxies = [
        [i, j]
        for i, line in enumerate(galaxy_map)
        for j, ch in enumerate(line)
        if ch == "#"
    ]
    empty_rows, empty_cols = find_empty_space(galaxy_map)
    g = copy.deepcopy(galaxies)  # control list, delete before commit
    for galaxy in galaxies:
        r = 0
        c = 0
        for row in empty_rows:
            if galaxy[0] > row:
                r += 1
        for col in empty_cols:
            if galaxy[1] > col:
                c += 1
        galaxy[0] += (expansion_rate - 1) * r
        galaxy[1] += (expansion_rate - 1) * c
    return galaxies


def expand_map(galaxy_map: List[str], amount: int = 1) -> List[str]:
    empty_rows, empty_cols = find_empty_space(galaxy_map)
    expanded = []
    # az sem to je spravne, dal to nekde dela chybu
    for i, line in enumerate(galaxy_map):
        for j in sorted(empty_cols, reverse=True):
            insertion = "." * amount
            line = line[:j] + insertion + line[j:]
        expanded.append(line)
        if i in empty_rows:
            insertion = ["." * len(line)] * amount
            expanded.extend(insertion)
    return expanded


def find_empty_space(galaxy_map: List[str]) -> List[List[int]]:
    empty_cols = []
    for j, _ in enumerate(galaxy_map[0]):
        for line in galaxy_map:
            if line[j] == "#":
                break
        else:
            empty_cols.append(j)
    empty_rows = [i for i, line in enumerate(galaxy_map) if "#" not in line]
    return [empty_rows, empty_cols]


def main():
    with open("2023\\Day_11.txt", "r") as file:
        input_data = file.read().split("\n")[:-1]

    # input_data = DUMMY.split("\n")

    # Part 1
    expanded_map = expand_map(input_data)
    galaxies = [
        [i, j]
        for i, line in enumerate(expanded_map)
        for j, ch in enumerate(line)
        if ch == "#"
    ]
    paths = calculate_shortest_paths(galaxies)
    print(f"Result 1 is: {sum(paths)}")

    # Part 2
    expansion_rate = 10**6
    galaxies2 = compansate_for_expansion(input_data, expansion_rate)
    paths2 = paths = calculate_shortest_paths(galaxies2)
    print(f"Result 2 is: {sum(paths2)}")


if __name__ == "__main__":
    start = time.perf_counter()
    main()
    end = time.perf_counter()
    print(f"Code has executed in: {end - start} s")
