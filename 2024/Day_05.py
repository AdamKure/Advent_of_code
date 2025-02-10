import functools
import time

DAY = 5


def read_files(day: int) -> tuple[str, str]:
    with open(f"2024/Day_{day:02}_example.txt", "r") as file:
        example = file.read()

    with open(f"2024/Day_{day:02}.txt", "r") as file:
        real_input = file.read()

    return example, real_input


def part_1(data: str) -> None:
    data_rules, data_updates = data.split("\n\n")
    rules = []
    for line in data_rules.splitlines():
        rules.append(list(map(int, line.split("|"))))

    cache = {}
    for x, y in rules:
        cache[(x, y)] = True
        cache[(y, x)] = False

    def is_ordered(update):
        for i, _ in enumerate(update):
            for j in range(i + 1, len(update)):
                key = (update[i], update[j])
                if key in cache and not cache[key]:
                    return False
        return True

    total = 0
    for line in data_updates.splitlines():
        update = list(map(int, line.split(",")))
        if is_ordered(update):
            total += update[len(update) // 2]

    print(f"Part 1 is: {total}")


def part_2(data: str) -> None:
    data_rules, data_updates = data.split("\n\n")
    rules = []

    for line in data_rules.splitlines():
        rules.append(list(map(int, line.split("|"))))

    cache = {}

    for x, y in rules:
        cache[(x, y)] = -1
        cache[(y, x)] = 1

    def is_ordered(update):
        for i, _ in enumerate(update):
            for j in range(i + 1, len(update)):
                key = (update[i], update[j])
                if key in cache and cache[key] == 1:
                    return False
        return True

    def cmp(x, y):
        return cache.get((x, y), 0)

    total = 0
    for line in data_updates.splitlines():
        update = list(map(int, line.split(",")))
        if is_ordered(update):
            continue
        update.sort(key=functools.cmp_to_key(cmp))
        total += update[len(update) // 2]

    print(f"Part 2 is: {total}")


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
