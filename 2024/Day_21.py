import time
from collections import deque
from functools import cache
from itertools import product

DAY = 21


def read_files(day: int) -> tuple[str, str]:
    with open(f"2024/Day_{day:02}_example.txt", "r") as file:
        example = file.read()

    with open(f"2024/Day_{day:02}.txt", "r") as file:
        real_input = file.read()

    return example, real_input


def part_1(data: str) -> None:
    # NOTE: this solution is quite suboptimal; this is my initial approach and the one I showed in part 1 of my video
    # for an optimal solution, just take part 2 and change the 25 to 2
    def compute_seqs(keypad):
        pos = {}
        for r in range(len(keypad)):
            for c in range(len(keypad[r])):
                if keypad[r][c] is not None:
                    pos[keypad[r][c]] = (r, c)
        seqs = {}
        for x in pos:
            for y in pos:
                if x == y:
                    seqs[(x, y)] = ["A"]
                    continue
                possibilities = []
                q = deque([(pos[x], "")])
                optimal = float("inf")
                while q:
                    (r, c), moves = q.popleft()
                    for nr, nc, nm in [
                        (r - 1, c, "^"),
                        (r + 1, c, "v"),
                        (r, c - 1, "<"),
                        (r, c + 1, ">"),
                    ]:
                        if (
                            nr < 0
                            or nc < 0
                            or nr >= len(keypad)
                            or nc >= len(keypad[0])
                        ):
                            continue
                        if keypad[nr][nc] is None:
                            continue
                        if keypad[nr][nc] == y:
                            if optimal < len(moves) + 1:
                                break
                            optimal = len(moves) + 1
                            possibilities.append(moves + nm + "A")
                        else:
                            q.append(((nr, nc), moves + nm))
                    else:
                        continue
                    break
                seqs[(x, y)] = possibilities
        return seqs

    def solve(_string, seqs):
        options = [seqs[(x, y)] for x, y in zip("A" + _string, _string)]
        return ["".join(x) for x in product(*options)]

    num_keypad = [["7", "8", "9"], ["4", "5", "6"], ["1", "2", "3"], [None, "0", "A"]]

    num_seqs = compute_seqs(num_keypad)

    dir_keypad = [[None, "^", "A"], ["<", "v", ">"]]

    dir_seqs = compute_seqs(dir_keypad)

    total = 0

    for line in data.splitlines():
        robot1 = solve(line, num_seqs)
        next = robot1
        for _ in range(2):
            possible_next = []
            for seq in next:
                possible_next += solve(seq, dir_seqs)
            minlen = min(map(len, possible_next))
            next = [seq for seq in possible_next if len(seq) == minlen]
        total += len(next[0]) * int(line[:-1])

    print("Part 1 is:", total)


def part_2(data: str) -> None:
    def compute_seqs(keypad):
        pos = []
        for r in range(len(keypad)):
            for c in range(len(keypad[r])):
                if keypad[r][c] is None:
                    ir, ic = r, c
                else:
                    pos.append((r, c))
        seqs = {}
        for rx, cx in pos:
            for ry, cy in pos:
                x = keypad[rx][cx]
                y = keypad[ry][cy]
                dr = ry - rx
                dc = cy - cx
                usd = "^" * -dr + "<" * -dc + ">" * dc + "v" * dr + "A"
                dsu = "v" * dr + "<" * -dc + ">" * dc + "^" * -dr + "A"
                ap, sp = (usd, dsu) if keypad == num_keypad else (dsu, usd)
                seqs[(x, y)] = [ap]
                if (
                    dr != 0
                    and dc != 0
                    and (rx != ir and cx != ic or ry != ir and cy != ic)
                ):
                    seqs[(x, y)].append(sp)
        return seqs

    def solve(string, seqs):
        options = [seqs[(x, y)] for x, y in zip("A" + string, string)]
        return ["".join(x) for x in product(*options)]

    num_keypad = [["7", "8", "9"], ["4", "5", "6"], ["1", "2", "3"], [None, "0", "A"]]

    num_seqs = compute_seqs(num_keypad)

    dir_keypad = [[None, "^", "A"], ["<", "v", ">"]]

    dir_seqs = compute_seqs(dir_keypad)
    dir_lengths = {key: len(value[0]) for key, value in dir_seqs.items()}

    @cache
    def compute_length(seq, depth=25):
        if depth == 1:
            return sum(dir_lengths[(x, y)] for x, y in zip("A" + seq, seq))
        length = 0
        for x, y in zip("A" + seq, seq):
            length += min(
                compute_length(subseq, depth - 1) for subseq in dir_seqs[(x, y)]
            )
        return length

    total = 0

    for line in data.splitlines():
        inputs = solve(line, num_seqs)
        length = min(map(compute_length, inputs))
        total += length * int(line[:-1])

    print("Part 2 is:", total)


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
