import time

DAY = 23


def read_files(day: int) -> tuple[str, str]:
    with open(f"2024/Day_{day:02}_example.txt", "r") as file:
        example = file.read()

    with open(f"2024/Day_{day:02}.txt", "r") as file:
        real_input = file.read()

    return example, real_input


def part_1(data: str) -> None:
    edges = [line.strip().split("-") for line in data.split("\n")]
    conns = {}

    for x, y in edges:
        if x not in conns:
            conns[x] = set()
        if y not in conns:
            conns[y] = set()
        conns[x].add(y)
        conns[y].add(x)

    sets = set()

    for x in conns:
        for y in conns[x]:
            for z in conns[y]:
                if x != z and x in conns[z]:
                    sets.add(tuple(sorted([x, y, z])))

    print("Part 1 is:", len([s for s in sets if any(cn.startswith("t") for cn in s)]))


def part_2(data: str) -> None:
    edges = [line.strip().split("-") for line in data.split("\n")]
    conns = {}

    for x, y in edges:
        if x not in conns:
            conns[x] = set()
        if y not in conns:
            conns[y] = set()
        conns[x].add(y)
        conns[y].add(x)

    sets = set()

    def search(node, req):
        key = tuple(sorted(req))
        if key in sets:
            return
        sets.add(key)
        for neighbor in conns[node]:
            if neighbor in req:
                continue
            if not all(neighbor in conns[query] for query in req):
                continue
            search(neighbor, {*req, neighbor})

    for x in conns:
        search(x, {x})

    print("Part 2 is:", ",".join(sorted(max(sets, key=len))))


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
