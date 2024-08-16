import time
from collections import deque


class Grid:
    def __init__(self, input_data):
        self.size = len(input_data.strip().splitlines())  # is square shaped
        self.radius = self.size // 2  # import if odd or even
        self.gardens = set()
        self.start = None
        self.cache = {}  # example (x, y, steps): (all_points, edge_points)
        for x, line in enumerate(input_data.strip().splitlines()):
            for y, char in enumerate(line):
                if char == ".":
                    self.gardens.add((x, y))
                elif char == "S":
                    self.start = (x, y)
                    self.gardens.add((x, y))

    def move(self, positions=None):
        if not positions:
            positions = [self.start]
        next_positions = set()
        for position in positions:
            for direction in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                new_position = (position[0] + direction[0], position[1] + direction[1])
                if new_position in self.gardens:
                    next_positions.add(new_position)
        return next_positions

    def cache_moves_from_point(self, origin):
        # cache results for particular outcome and use it for repeating tiles
        # starts in the center
        # distance from center to neighboring center = self.size, same as center to corner of next square
        # if even number of steps left i can always return to self, akak these points alwys present
        # if x steps left, then x+2 is superset of x, can keep track of edge points

        for step in range(2 * self.size + 2):
            if step > 1:
                old_points, _ = self.cache[(origin[0], origin[1], step - 2)]
                _, old_edges = self.cache[(origin[0], origin[1], step - 1)]
            elif step == 0:
                self.cache[(origin[0], origin[1], 0)] = (
                    {origin},
                    {origin},
                )
                continue
            elif step == 1:
                all_points = self.move()
                self.cache[(origin[0], origin[1], 1)] = (
                    all_points,
                    all_points,
                )
                continue
            else:
                raise ValueError("Steps must be non-negative integer")

            new_points = set()
            for point in old_edges:
                for direction in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                    new_position = (
                        point[0] + direction[0],
                        point[1] + direction[1],
                    )
                    if new_position in self.gardens:
                        new_points.add(new_position)
            new_edges = new_points.difference(old_points)
            new_points = old_points.union(new_points)
            self.cache[(origin[0], origin[1], step)] = (new_points, new_edges)

    def get_moves_from_points(self):
        for origin in [
            (x, y)
            for x in [0, self.radius, self.size - 1]
            for y in [0, self.radius, self.size - 1]
        ]:
            self.cache_moves_from_point(origin)

    def infinite_solution(self, steps):
        def fill(x, y, steps):
            visited = set()
            positions = deque([(x, y, steps)])
            res = set()
            while positions:
                x, y, s = positions.popleft()
                if s % 2 == 0:
                    res.add((x, y))
                if s < 1:
                    continue
                for direction in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                    nx = x + direction[0]
                    ny = y + direction[1]
                    if (nx, ny) in self.gardens and (nx, ny) not in visited:
                        positions.append((nx, ny, s - 1))
                        visited.add((nx, ny))
            return len(res)

        center = self.size // 2
        grid_width = steps // self.size - 1
        odds = (grid_width // 2 * 2 + 1) ** 2
        evens = ((grid_width + 1) // 2 * 2) ** 2

        # assert (center, center) == self.start
        # assert (steps - self.radius) % self.size == 0

        odd_filled = fill(center, center, self.size * 2 + 1)
        even_filled = fill(center, center, self.size * 2)

        tips = (
            fill(0, center, self.size - 1)
            + fill(self.size - 1, center, self.size - 1)
            + fill(center, self.size - 1, self.size - 1)
            + fill(center, 0, self.size - 1)
        )

        small_corners = (
            fill(0, 0, self.size // 2 - 1) * (grid_width + 1)
            + fill(0, self.size - 1, self.size // 2 - 1) * (grid_width + 1)
            + fill(self.size - 1, 0, self.size // 2 - 1) * (grid_width + 1)
            + fill(self.size - 1, self.size - 1, self.size // 2 - 1) * (grid_width + 1)
        )

        big_corners = (
            fill(0, 0, self.size * 3 // 2 - 1) * grid_width
            + fill(0, self.size - 1, self.size * 3 // 2 - 1) * grid_width
            + fill(self.size - 1, 0, self.size * 3 // 2 - 1) * grid_width
            + fill(self.size - 1, self.size - 1, self.size * 3 // 2 - 1) * grid_width
        )

        result = (
            fill(center, center, steps)
            if steps < self.radius
            else (
                odds * odd_filled
                + evens * even_filled
                + tips
                + small_corners
                + big_corners
            )
        )

        return result

    def part_1(self):
        visited_positione = []
        for _ in range(64):
            visited_positione = self.move(visited_positione)
        return len(visited_positione)

    def part_2(self):
        return self.infinite_solution(26501365)


def main() -> None:
    with open("2023/Day_21.txt", "r") as file:
        input_data = file.read()

    g = Grid(input_data)
    h = Grid(input_data)

    # Part 1
    print(f"Result 1 is: {g.part_1()}")

    # Part 2
    print(f"Result 2 is: {h.part_2()}")


if __name__ == "__main__":
    start = time.perf_counter()
    main()
    end = time.perf_counter()
    print(f"\nExecuted in: {end - start} s")
