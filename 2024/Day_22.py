import time

DAY = 22


def read_files(day: int) -> tuple[str, str]:
    with open(f"2024/Day_{day:02}_example.txt", "r") as file:
        example = file.read()

    with open(f"2024/Day_{day:02}.txt", "r") as file:
        real_input = file.read()

    return example, real_input


def part_1(data: str) -> None:
    def step(num):
        num = (num ^ (num * 64)) % 16777216
        num = (num ^ (num // 32)) % 16777216
        num = (num ^ (num * 2048)) % 16777216
        return num

    total = 0

    for line in data.split("\n"):
        num = int(line)
        for _ in range(2000):
            num = step(num)
        total += num

    print("Part 1 is:", total)


def part_2(data: str) -> None:
    def step(num):
        num = (num ^ (num * 64)) % 16777216
        num = (num ^ (num // 32)) % 16777216
        num = (num ^ (num * 2048)) % 16777216
        return num

    seq_to_total = {}

    for line in data.split("\n"):
        num = int(line)
        buyer = [num % 10]
        for _ in range(2000):
            num = step(num)
            buyer.append(num % 10)
        seen = set()
        for i in range(len(buyer) - 4):
            a, b, c, d, e = buyer[i : i + 5]
            seq = (b - a, c - b, d - c, e - d)
            if seq in seen:
                continue
            seen.add(seq)
            if seq not in seq_to_total:
                seq_to_total[seq] = 0
            seq_to_total[seq] += e

    print("Part 2 is:", max(seq_to_total.values()))


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
