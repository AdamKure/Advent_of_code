import time

DAY = 9


def read_files(day: int) -> tuple[str, str]:
    with open(f"2024/Day_{day:02}_example.txt", "r") as file:
        example = file.read().strip()

    with open(f"2024/Day_{day:02}.txt", "r") as file:
        real_input = file.read().strip()

    return example, real_input


def part_1(data: str) -> None:
    disk = []
    fid = 0

    for i, char in enumerate(data):
        x = int(char)
        if i % 2 == 0:
            disk += [fid] * x
            fid += 1
        else:
            disk += [-1] * x

    blanks = [i for i, x in enumerate(disk) if x == -1]

    for i in blanks:
        while disk[-1] == -1:
            disk.pop()
        if len(disk) <= i:
            break
        disk[i] = disk.pop()

    print("Part 1 is:", sum(i * x for i, x in enumerate(disk)))


def part_2(data: str) -> None:
    files = {}
    blanks = []

    fid = 0
    pos = 0

    for i, char in enumerate(data):
        x = int(char)
        if i % 2 == 0:
            if x == 0:
                raise ValueError("unexpected x=0 for file")
            files[fid] = (pos, x)
            fid += 1
        else:
            if x != 0:
                blanks.append((pos, x))
        pos += x

    while fid > 0:
        fid -= 1
        pos, size = files[fid]
        for i, (start, length) in enumerate(blanks):
            if start >= pos:
                blanks = blanks[:i]
                break
            if size <= length:
                files[fid] = (start, size)
                if size == length:
                    blanks.pop(i)
                else:
                    blanks[i] = (start + size, length - size)
                break

    total = 0

    for fid, (pos, size) in files.items():
        for x in range(pos, pos + size):
            total += fid * x

    print(f"Part 2 is:", total)


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
