import re
import time

def record_number(time, record):
    record_number = 2 * race_record(time, record)
    if time/2 == int(time/2):
        record_number += -1
    return record_number

def race_record(time, record):
    record_counter = 0
    for num in range(int(time/2 + 1)):
        charge = int(time/2) - num
        race_time = time - charge
        distance = charge * race_time
        if distance <= record:
            return record_counter
        record_counter += 1


def main():
    with open(r"2023\Day_06.txt", "r") as file:
        input_data = file.read().lower()

    time_str, distance_str, _ = input_data.split("\n")
    times = re.findall(r"(\d+)", time_str)
    distances = re.findall(r"(\d+)", distance_str)
    record_variations = [record_number(int(times[index]), int(distances[index])) for index, _ in enumerate(times)]

    result1 = 1
    for rec in record_variations:
        result1 *= rec
    print(f"Result 1 is: {result1}")

    time = int("".join(times))
    distance = int("".join(distances))
    result2 = record_number(time, distance)
    print(f"Result 2 is: {result2}")

if __name__ == "__main__":
    start = time.perf_counter()
    main()
    end = time.perf_counter()
    print(end - start)
