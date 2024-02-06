import time

# serves as a template for now


def part1(input_data):
    return "Not implemented yet"


def part2(input_data):
    return "Not implemented yet"


def main() -> None:
    with open("2023/Day_.txt", "r") as file:
        input_data = file.read()

    # Part 1
    result1 = part1(input_data)
    print(f"Result 1 is: {result1}")

    # Part 2
    result2 = part2(input_data)
    print(f"Result 2 is: {result2}")


if __name__ == "__main__":
    start = time.perf_counter()
    main()
    end = time.perf_counter()
    print(f"\nExecuted in: {end - start} s")
