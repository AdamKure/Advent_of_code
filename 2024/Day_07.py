import time

DAY = 7


def read_files(day: int) -> tuple[str, str]:
    with open(f"2024/Day_{day:02}_example.txt", "r") as file:
        example = file.read()

    with open(f"2024/Day_{day:02}.txt", "r") as file:
        real_input = file.read()

    return example, real_input


def part_1(data: str) -> None:
    total = 0

    def can_obtain(target, array):
        if len(array) == 1:
            return target == array[0]
        if target % array[-1] == 0 and can_obtain(target // array[-1], array[:-1]):
            return True
        if target > array[-1] and can_obtain(target - array[-1], array[:-1]):
            return True
        return False

    for line in data.splitlines():
        l, r = line.split(": ")
        target = int(l)
        array = [int(x) for x in r.split()]
        if can_obtain(target, array):
            total += target

    print(f"Part 1 is: {total}")


def part_2(data: str) -> None:
    total = 0

    def can_obtain(target, array):
        if len(array) == 1:
            return target == array[0]
        if target % array[-1] == 0 and can_obtain(target // array[-1], array[:-1]):
            return True
        if target > array[-1] and can_obtain(target - array[-1], array[:-1]):
            return True
        s_target = str(target)
        s_last = str(array[-1])
        if (
            s_target.endswith(s_last)
            and len(s_target) > len(s_last)
            and can_obtain(int(s_target[: -len(s_last)]), array[:-1])
        ):
            return True
        return False

    for line in data.splitlines():
        l, r = line.split(": ")
        target = int(l)
        array = [int(x) for x in r.split()]
        if can_obtain(target, array):
            total += target

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
