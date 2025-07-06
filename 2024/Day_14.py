import re
import time
from collections import defaultdict

DAY = 14


def read_files(day: int) -> tuple[str, str]:
    with open(f"2024/Day_{day:02}_example.txt", "r") as file:
        example = file.read()

    with open(f"2024/Day_{day:02}.txt", "r") as file:
        real_input = file.read()

    return example, real_input


def part_1(data: str) -> None:
    WIDTH = 101
    HEIGHT = 103

    robots = []

    for line in data.split("\n"):
        robots.append(tuple(map(int, re.findall(r"-?\d+", line))))

    result = []

    for px, py, vx, vy in robots:
        result.append(((px + vx * 100) % WIDTH, (py + vy * 100) % HEIGHT))

    tl = bl = tr = br = 0

    VM = (HEIGHT - 1) // 2
    HM = (WIDTH - 1) // 2

    for px, py in result:
        if px == HM or py == VM:
            continue
        if px < HM:
            if py < VM:
                tl += 1
            else:
                bl += 1
        else:
            if py < VM:
                tr += 1
            else:
                br += 1

    print("Part 1 is:", tl * bl * tr * br)


def part_2(data: str) -> None:
    WIDTH = 101
    HEIGHT = 103

    robots = []

    for line in data.split("\n"):
        robots.append(list(map(int, re.findall(r"-?\d+", line))))

    initial = list(map(list, robots))

    max_cluster = 0
    best_iteration = None

    for second in range(WIDTH * HEIGHT):
        coords = set((x, y) for x, y, _, _ in robots)

        while coords:
            x, y = coords.pop()
            cluster = 1
            search = {(x, y)}
            while search:
                x, y = search.pop()
                for nx in [x - 1, x, x + 1]:
                    for ny in [y - 1, y, y + 1]:
                        if nx == x and ny == y:
                            continue
                        if (nx, ny) in coords:
                            cluster += 1
                            search.add((nx, ny))
                            coords.remove((nx, ny))
            if cluster > max_cluster:
                max_cluster = cluster
                best_iteration = second

        for robot in robots:
            px, py, vx, vy = robot
            robot[0] = (px + vx) % WIDTH
            robot[1] = (py + vy) % HEIGHT

    coords = []

    for px, py, vx, vy in initial:
        coords.append(
            ((px + vx * best_iteration) % WIDTH, (py + vy * best_iteration) % HEIGHT)
        )

    print("Part 2 is:", best_iteration)
    visualize_grid(coords)


def visualize_grid(positions):
    WIDTH = 101
    HEIGHT = 103

    robot_counts = defaultdict(lambda: 0)
    for r, c in positions:
        robot_counts[(r, c)] += 1

    for r in range(HEIGHT):
        for c in range(WIDTH):
            if (r, c) not in robot_counts:
                print(".", end="")
            else:
                print(robot_counts[(r, c)], end="")
        print()


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
