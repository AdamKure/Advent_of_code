import time
from typing import List


def find_zero_difs(history: List[int]):
    difs = [history[i + 1] - num for i, num in enumerate(history[:-1])]
    if all(num == 0 for num in difs):
        return [history, difs]
    else:
        return [history] + find_zero_difs(difs)


def main():
    with open(r"2023\Day_09.txt", "r") as file:
        input_data = file.readlines()

    history = [[int(num) for num in line.split()] for line in input_data]
    predictions = []
    for line in history:
        derivs = find_zero_difs(line)
        prediction = 0
        for order in reversed(derivs):
            prediction += order[-1]
        predictions.append(prediction)

    print(sum(predictions))

    # Part 2
    predictions2 = []
    for line in history:
        derivs = find_zero_difs(line)
        prediction = 0
        for order in reversed(derivs):
            prediction = order[0] - prediction
        predictions2.append(prediction)

    print(sum(predictions2))


if __name__ == "__main__":
    start = time.perf_counter()
    main()
    end = time.perf_counter()
    print(f"\nExecuted in: {end - start} s")
