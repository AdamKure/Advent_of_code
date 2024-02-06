import time
from collections import deque
from math import lcm
from typing import List, Tuple, Union


class Module:
    def __init__(self, name, prefix, targets):
        self.memo = None
        self.name = name
        self.prefix = prefix
        self.targets = targets

        self.__set_memo(prefix)

    def __set_memo(self, prefix) -> None:
        if prefix == "%":
            self.memo = 0
        elif prefix == "&":
            self.memo = {}
        else:
            raise ValueError("Prefix is not valid")

    def process_signal(self, origin, value) -> Union[None, List[Tuple[str, int]]]:
        if self.prefix == "%":
            if value == 1:
                return
            self.memo = 1 - self.memo
            return [(self.name, target, self.memo) for target in self.targets]
        self.memo[origin] = value
        if all(value == 1 for value in self.memo.values()):
            output = 0
        else:
            output = 1
        return [(self.name, target, output) for target in self.targets]


def part1(input_data) -> int:
    modules = {}
    for line in input_data.split("\n"):
        left, right = line.split(" -> ")
        targets = right.strip().split(", ")
        if left == "broadcaster":
            bc_targets = targets
        else:
            prefix = left[0]
            name = left[1:]
            modules[name] = Module(name, prefix, targets)
    for name, module in modules.items():
        for target in module.targets:
            if target in modules and modules[target].prefix == "&":
                modules[target].memo[name] = 0

    low_high = [0, 0]
    for _ in range(1000):
        low_high[0] += 1
        signals = deque([("bc", target, 0) for target in bc_targets])
        while signals:
            origin, target, value = signals.popleft()
            low_high[value] += 1
            if target not in modules:
                continue
            new_signals = modules[target].process_signal(origin, value)
            if new_signals:
                signals.extend(new_signals)
    return low_high[0] * low_high[1]


def part2(input_data) -> int:
    modules = {}
    for line in input_data.split("\n"):
        left, right = line.split(" -> ")
        targets = right.strip().split(", ")
        if left == "broadcaster":
            bc_targets = targets
        else:
            prefix = left[0]
            name = left[1:]
            if "rx" in targets:
                feed_name = name
            modules[name] = Module(name, prefix, targets)
    for name, module in modules.items():
        for target in module.targets:
            if target in modules and modules[target].prefix == "&":
                modules[target].memo[name] = 0

    feed_reps = {name: 0 for name in modules[feed_name].memo}
    presses = 0
    while True:
        presses += 1
        signals = deque([("bc", target, 0) for target in bc_targets])
        while signals:
            origin, target, value = signals.popleft()
            if target == feed_name and value == 1:
                feed_reps[origin] = presses - feed_reps[origin]
                if all(feed_reps.values()):
                    return lcm(*[rep for rep in feed_reps.values()])
            if target not in modules:
                continue
            new_signals = modules[target].process_signal(origin, value)
            if new_signals:
                signals.extend(new_signals)
    return "No match found"


def main() -> None:
    with open("2023/Day_20.txt", "r") as file:
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
