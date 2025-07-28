import re
import time

DAY = 17


def read_files(day: int) -> tuple[str, str]:
    with open(f"2024/Day_{day:02}_example.txt", "r") as file:
        example = file.read()

    with open(f"2024/Day_{day:02}.txt", "r") as file:
        real_input = file.read()

    return example, real_input


def part_1(data: str) -> None:
    a, b, c, *program = map(int, re.findall(r"\d+", data))

    pointer = 0
    output = []

    def combo(operand):
        if 0 <= operand <= 3:
            return operand
        if operand == 4:
            return a
        if operand == 5:
            return b
        if operand == 6:
            return c
        raise AssertionError(f"unrecognized combo operand {operand}")

    while pointer < len(program):
        ins = program[pointer]
        operand = program[pointer + 1]
        if ins == 0:  # adv
            a = a >> combo(operand)
        elif ins == 1:  # bxl
            b = b ^ operand
        elif ins == 2:  # bst
            b = combo(operand) % 8
        elif ins == 3:  # jnz
            if a != 0:
                pointer = operand
                continue
        elif ins == 4:  # bxc
            b = b ^ c
        elif ins == 5:  # out
            output.append(combo(operand) % 8)
        elif ins == 6:  # bdv
            b = a >> combo(operand)
        elif ins == 7:  # cdv
            c = a >> combo(operand)
        pointer += 2

    print("Part 1 is: ", ",".join(map(str, output)))


def part_2(data: str) -> None:
    program = list(map(int, re.findall(r"\d+", data)[3:]))
    assert program[-2:] == [3, 0], "program does not end with JNZ 0"

    def find(target, ans):
        if target == []:
            return ans
        for t in range(8):
            a = ans << 3 | t
            b = 0
            c = 0
            output = None
            adv3 = False

            def combo(operand):
                if 0 <= operand <= 3:
                    return operand
                if operand == 4:
                    return a
                if operand == 5:
                    return b
                if operand == 6:
                    return c
                raise AssertionError(f"unrecognized combo operand {operand}")

            for pointer in range(0, len(program) - 2, 2):
                ins = program[pointer]
                operand = program[pointer + 1]
                if ins == 0:
                    assert not adv3, "program has multiple ADVs"
                    assert operand == 3, "program has ADV with operand other than 3"
                    adv3 = True
                elif ins == 1:
                    b = b ^ operand
                elif ins == 2:
                    b = combo(operand) % 8
                elif ins == 3:

                    raise AssertionError("program has JNZ inside expected loop body")
                elif ins == 4:
                    b = b ^ c
                elif ins == 5:
                    assert output is None, "program has multiple OUT"
                    output = combo(operand) % 8
                elif ins == 6:
                    b = a >> combo(operand)
                elif ins == 7:
                    c = a >> combo(operand)
                if output == target[-1]:
                    sub = find(target[:-1], a)
                    if sub is None:
                        continue
                    return sub

    print("Part 2 is:", find(program, 0))


def main() -> None:
    example, real_input = read_files(DAY)

    part_1(example)
    part_1(real_input)

    part_2(real_input)


if __name__ == "__main__":
    start = time.perf_counter()
    main()
    end = time.perf_counter()
    print(f"\nExecuted in: {end - start} s")
