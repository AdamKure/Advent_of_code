import time

import sympy


class Hailstone:
    def __init__(self, sx, sy, sz, vx, vy, vz):
        # Starting point
        self.sx = sx
        self.sy = sy
        self.sz = sz

        # Starting velocity
        self.vx = vx
        self.vy = vy
        self.vz = vz

        # Line equation ax + by + c = 0
        self.a = vy
        self.b = -vx
        self.c = vy * sx - vx * sy


def main():
    # Part 1
    with open("2023/Day_24.txt") as file:
        hailstones = [
            Hailstone(*map(int, line.replace("@", ",").split(",")))
            for line in file.read().splitlines()
        ]

    # Lower and upper bounds for x and y
    lb, ub = 200000000000000, 400000000000000

    # Count the number of intersections
    total = 0
    for i, hs1 in enumerate(hailstones):
        for hs2 in hailstones[:i]:
            a1, b1, c1 = hs1.a, hs1.b, hs1.c
            a2, b2, c2 = hs2.a, hs2.b, hs2.c

            # If parallel, skip
            if a1 * b2 == b1 * a2:
                continue

            # Intersection point
            x = (c1 * b2 - c2 * b1) / (a1 * b2 - a2 * b1)
            y = (c2 * a1 - c1 * a2) / (a1 * b2 - a2 * b1)

            # Intersection point is within bounds and is in the future for both hailstones
            if (lb <= x <= ub and lb <= y <= ub) and all(
                (x - hs.sx) * hs.vx >= 0 and (y - hs.sy) * hs.vy >= 0
                for hs in (hs1, hs2)
            ):
                total += 1

    print(f"Part 1 result: {total}")

    # Part 2
    with open("2023/Day_24.txt") as file:
        hailstones = [
            tuple(map(int, line.replace("@", ",").split(",")))
            for line in file.read().splitlines()
        ]

    # Hailstone variables
    xr, yr, zr, vxr, vyr, vzr = sympy.symbols("xr, yr, zr, vxr, vyr, vzr")

    # Equations for the rock
    equations = []
    for i, (sx, sy, sz, vx, vy, vz) in enumerate(hailstones):
        equations.append((xr - sx) * (vy - vyr) - (yr - sy) * (vx - vxr))
        equations.append((yr - sy) * (vz - vzr) - (zr - sz) * (vy - vyr))

        # Need at least 3 hailstones to solve the equations
        if i < 2:
            continue

        # Possible solutions
        answers = [
            soln
            for soln in sympy.solve(equations)
            if all(x % 1 == 0 for x in soln.values())
        ]

        # Found the only solution
        if len(answers) == 1:
            answer = answers[0]
            break

    print(
        f"Starting position of the rock is: x: {answer[xr]}, y: {answer[yr]}, Z: {answer[zr]}"
    )
    print(f"Part 2 result: {abs(answer[xr]) + abs(answer[yr]) + abs(answer[zr])}")


if __name__ == "__main__":
    start = time.perf_counter()
    main()
    end = time.perf_counter()
    print(f"\nExecuted in: {end - start} s")
