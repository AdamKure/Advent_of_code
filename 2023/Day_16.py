import time
from functools import cache
from typing import Dict, Set, Tuple


class BeamGrid:
    def __init__(self, grid: Dict[Tuple[int], str]) -> None:
        self.grid = grid
        self.visited = None

    def __interact(self, current: Tuple[int], direction: Tuple[int]) -> None:
        r, c = direction
        new_direction = [direction]
        if self.grid[current] == "/":
            new_direction = [(-c, -r)]
        if self.grid[current] == "\\":
            new_direction = [(c, r)]
        if self.grid[current] == "|" and c != 0:
            new_direction = [(-1, 0), (1, 0)]
        if self.grid[current] == "-" and r != 0:
            new_direction = [(0, -1), (0, 1)]
        for new_dire in new_direction:
            next_step = (current[0] + new_dire[0], current[1] + new_dire[1])
            self.__propagate(next_step, new_dire)

    def __propagate(self, current: Tuple[int], direction: Tuple[int]) -> None:
        max_r, max_c = tuple(max(z) for z in zip(*self.grid.keys()))
        while 0 <= current[0] <= max_r and 0 <= current[1] <= max_c:
            if current in self.visited and direction in self.visited[current]:
                break
            if current not in self.visited:
                self.visited[current] = set()
            self.visited[current].add(direction)
            if self.grid[current] != ".":
                self.__interact(current, direction)
                break
            next_step = (current[0] + direction[0], current[1] + direction[1])
            current = next_step

    def get_energized(
        self, entry_pos: Tuple[int], entry_dir: Tuple[int]
    ) -> Dict[Tuple[int], Set[Tuple[int]]]:
        self.visited = {}
        self.__propagate(entry_pos, entry_dir)
        return self.visited


def main() -> None:
    with open("2023/Day_16.txt", "r") as file:
        input_data = file.read()

    # Part 1
    grid = {
        (r, c): char
        for r, row in enumerate(input_data.split("\n"))
        for c, char in enumerate(row)
    }
    max_row, max_col = tuple(max(z) for z in zip(*grid.keys()))
    bg = BeamGrid(grid)

    result1 = len(bg.get_energized((0, 0), (0, 1)))
    print(f"Result 1 is: {result1}")

    # Part 2
    max_energized = 0
    for col in range(max_col + 1):
        a = len(bg.get_energized((0, col), (1, 0)))
        b = len(bg.get_energized((max_row, col), (-1, 0)))
        max_energized = max(max_energized, a, b)
        print(f"Done col: {col}/{max_col}")
    for row in range(max_row + 1):
        a = len(bg.get_energized((row, 0), (0, 1)))
        b = len(bg.get_energized((row, max_col), (0, -1)))
        max_energized = max(max_energized, a, b)
        print(f"Done row: {row}/{max_row}")
    result2 = max_energized
    print(f"Result 2 is: {result2}")


if __name__ == "__main__":
    start = time.perf_counter()
    main()
    end = time.perf_counter()
    print(f"\nExecuted in: {end - start} s")
