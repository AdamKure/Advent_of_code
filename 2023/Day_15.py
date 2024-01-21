import time


def get_hash(text: str) -> int:
    num = 0
    for char in text:
        num += ord(char)
        num *= 17
        num = num % 256
    return num


def main() -> None:
    with open("2023/Day_15.txt", "r") as file:
        input_data = file.read()

    # Part 1
    lines = input_data.split("\n")
    steps_list = (line.split(",") for line in lines)
    ini_hash = (get_hash(step) for steps in steps_list for step in steps)
    result1 = sum(ini_hash)
    print(f"Result 1 is: {result1}")

    # Part 2
    hashmap = {box_id: [] for box_id in range(256)}
    steps = input_data.replace("\n", "").split(",")
    for step in steps:
        if "-" in step:
            label = step.replace("-", "")
            box_id = get_hash(label)
            box_contains = []
            for lens in hashmap[box_id]:
                if label in lens:
                    continue
                box_contains.append(lens)
            hashmap[box_id] = box_contains
        if "=" in step:
            label, focal = step.split("=")
            box_id = get_hash(label)
            new_lens = {label: int(focal)}
            box_contains = []
            is_in_box = False
            for lens in hashmap[box_id]:
                if label in lens:
                    box_contains.append(new_lens)
                    is_in_box = True
                else:
                    box_contains.append(lens)
            if not is_in_box:
                box_contains.append(new_lens)
            hashmap[box_id] = box_contains

    result2 = 0
    for box_id, box_contains in hashmap.items():
        for i, lens in enumerate(box_contains):
            inc = (box_id + 1) * (i + 1) * next(iter(lens.values()))
            result2 += inc

    print(f"Result 2 is: {result2}")


if __name__ == "__main__":
    start = time.perf_counter()
    main()
    end = time.perf_counter()
    print(f"\nExecuted in: {end - start} s")
