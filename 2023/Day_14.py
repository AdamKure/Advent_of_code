import time
from functools import cache


class RockPositions:
    def __init__(self, rows, cols, cubes, rounded):
        self.cols = cols
        self.cubes = cubes
        self.rounded = rounded
        self.rows = rows


class ReflectorDish:
    def __init__(self, reflector_dish: str) -> None:
        self.rock_pos = None
        self.__parse(reflector_dish)

    def __parse(self, reflector_dish: str) -> None:
        lines = reflector_dish.split("\n")
        rows = len(lines)
        cols = len(lines[0])
        rounded = set()
        cubes = set()
        for r, row in enumerate(lines):
            for c, char in enumerate(row):
                if char == ".":
                    continue
                if char == "#":
                    cubes.add((r, c))
                    continue
                if char == "O":
                    rounded.add((r, c))
                    continue
        self.rock_pos = RockPositions(
            rows, cols, set(sorted(cubes)), set(sorted(rounded))
        )

    def __rotate(self, rock_pos: RockPositions) -> RockPositions:
        # max(r)-r -> c
        # c -> r
        rows = rock_pos.rows
        new_cubes = {(c, rows - 1 - r) for r, c in rock_pos.cubes}
        new_rounded = {(c, rows - 1 - r) for r, c in rock_pos.rounded}
        return RockPositions(rock_pos.cols, rock_pos.rows, new_cubes, new_rounded)

    def __tilt(self, rock_pos: RockPositions) -> RockPositions:
        tilted = set()
        for c in range(rock_pos.cols):
            first_free = 0
            for r in range(rock_pos.rows):
                if (r, c) in rock_pos.cubes:
                    first_free = r + 1
                if (r, c) in rock_pos.rounded:
                    tilted.add((first_free, c))
                    first_free += 1
        rock_pos.rounded = tilted
        return rock_pos

    def get_weight(self, rotations: int = 0) -> int:
        # @cache
        def tilt_and_rotate(rock_pos):
            for _ in range(4):
                rock_pos = self.__tilt(rock_pos)
                rock_pos = self.__rotate(rock_pos)
            return rock_pos

        rock_pos = self.rock_pos
        cached = {}
        cycle = 0
        while cycle < rotations:
            if frozenset(rock_pos.rounded) in cached:
                dif = cycle - cached[frozenset(rock_pos.rounded)]
                rem = (rotations - cycle) % dif
                print()
                print(
                    f"Current {cycle}, cycle repetition {dif}, new rot {rotations-rem}"
                )
                cycle = rotations - rem
                cached = {}
            cached[frozenset(rock_pos.rounded)] = cycle
            rock_pos = tilt_and_rotate(rock_pos)
            if cycle == 100000:
                raise RuntimeError("Not cached after 10k iterations")
            cycle += 1
        # printer(rock_pos)
        # rock_pos = self.__tilt(rock_pos)
        rows = rock_pos.rows
        weight = 0
        for r, _ in rock_pos.rounded:
            weight += rows - r
        return weight


def printer(rock_pos):
    O_count = 0
    for r in range(rock_pos.rows):
        line = ""
        for c in range(rock_pos.cols):
            if (r, c) in rock_pos.rounded:
                line += " O"
                O_count += 1
            elif (r, c) in rock_pos.cubes:
                line += " #"
            else:
                line += " ."
        print(line)
    print()
    # print(f"Number of Os = {O_count}")


def main() -> None:
    with open("2023/Day_14.txt", "r") as file:
        input_data = file.read()

    # Part 1
    # result1 = ReflectorDish(input_data).get_weight()
    # print(f"Result 1 is: {result1}")

    # Part 2
    cycles = 1000000000
    result2 = ReflectorDish(input_data).get_weight(cycles)
    print(f"Result 2 is: {result2}")


if __name__ == "__main__":
    start = time.perf_counter()
    main()
    end = time.perf_counter()
    print(f"\nExecuted in: {end - start} s")
