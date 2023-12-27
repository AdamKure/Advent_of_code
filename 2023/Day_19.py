import re
import time
from typing import Dict, List, Tuple, Union


def does_overlap(ranges: List[Dict[str, Union[str, int]]]) -> bool:
    if len(ranges) < 2:
        return False
    for i, item in enumerate(ranges[:-1]):
        for comp in ranges[i + 1 :]:
            if (
                (
                    item["x"][0] <= comp["x"][0] < item["x"][1]
                    or comp["x"][0] <= item["x"][0] < comp["x"][1]
                )
                and (
                    item["m"][0] <= comp["m"][0] < item["m"][1]
                    or comp["m"][0] <= item["m"][0] < comp["m"][1]
                )
                and (
                    item["a"][0] <= comp["a"][0] < item["a"][1]
                    or comp["a"][0] <= item["a"][0] < comp["a"][1]
                )
                and (
                    item["s"][0] <= comp["s"][0] < item["s"][1]
                    or comp["s"][0] <= item["s"][0] < comp["s"][1]
                )
            ):
                return True
    return False


def main():
    with open(r"2023\Day_19.txt", "r") as file:
        input_data = file.read()[:-1]

    wfs, ratings = input_data.split("\n\n")
    wfs = wfs.split("\n")
    ratings = ratings.split("\n")

    workflows = {}
    for line in wfs:
        m = re.search(r"(\w+)\{(.+)\}", line)
        cur, rules = m.group(1, 2)
        workflows[cur] = rules.split(",")

    parts = []
    for line in ratings:
        m = re.search(r"x=(\d+),m=(\d+),a=(\d+),s=(\d+)", line)
        x, m, a, s = m.group(1, 2, 3, 4)
        x, m, a, s = int(x), int(m), int(a), int(s)
        parts.append(
            {
                "x": x,
                "m": m,
                "a": a,
                "s": s,
                "sum": sum([x, m, a, s]),
            }
        )

    parts_sum = 0
    for part in parts:
        if is_valid(workflows, part):
            parts_sum += part["sum"]

    print(f"Part 1 result is: {parts_sum}")

    # Part 2
    valid_combinations = workflow_ranges(workflows)
    print(f"Overlaping regions: {does_overlap(valid_combinations)}")

    result = 0
    for item in valid_combinations:
        x = item["x"]
        m = item["m"]
        a = item["a"]
        s = item["s"]
        inc = (x[1] - x[0]) * (m[1] - m[0]) * (a[1] - a[0]) * (s[1] - s[0])
        result += inc
    print(f"Part 2 result is: {result}")


def is_valid(workflows: Dict[str, List[str]], part: Dict[str, int]) -> bool:
    def get_destination(rules: List[str], part: Dict[str, int]) -> str:
        for rule in rules:
            if ":" not in rule:
                return rule
            condition, target = rule.split(":")
            cat, sign, lim = condition[0], condition[1], int(condition[2:])
            if sign == "<":
                if part[cat] < lim:
                    return target
                continue
            if sign == ">":
                if part[cat] > lim:
                    return target
                continue
            raise ValueError("Expected < or >")

    workflow = "in"
    while 1:
        rules = workflows[workflow]
        workflow = get_destination(rules, part)
        if workflow == "R":
            return False
        if workflow == "A":
            return True


def workflow_ranges(workflows: str) -> List[Dict[str, Union[str, int]]]:
    def get_ranges(rules: List[str], subrange: Dict[str, Union[str, int]]):
        for rule in rules:
            if ":" not in rule:
                subrange["target"] = rule
                return [subrange]
            condition, target = rule.split(":")
            cat, sign, lim = condition[0], condition[1], int(condition[2:])
            bot, top = subrange[cat]
            if sign not in {"<", ">"}:
                raise ValueError("Expected < or >")
            if sign == "<" and bot >= lim:
                continue
            if sign == "<" and top <= lim:
                subrange["target"] = target
                return [subrange]
            if sign == ">" and top <= lim + 1:
                continue
            if sign == ">" and bot > lim:
                subrange["target"] = target
                return [subrange]
            if sign == "<":
                cat1, cat2 = (bot, lim), (lim, top)
            else:
                cat1, cat2 = (bot, lim + 1), (lim + 1, top)

            subrange1 = subrange.copy()
            subrange2 = subrange.copy()
            subrange1[cat] = cat1
            subrange2[cat] = cat2
            return get_ranges(rules, subrange1) + get_ranges(rules, subrange2)

    base_range = (1, 4001)
    start_range = {
        "x": base_range,
        "m": base_range,
        "a": base_range,
        "s": base_range,
        "target": "in",
        "log": "",
    }
    ranges = [start_range]
    accepted = []
    while ranges:
        subrange = ranges.pop(0)
        workflow = subrange["target"]
        if workflow == "R":
            continue
        if workflow == "A":
            accepted.append(subrange)
            continue
        rules = workflows[workflow]
        ranges.extend(get_ranges(rules, subrange))
    return accepted


if __name__ == "__main__":
    start = time.perf_counter()
    main()
    end = time.perf_counter()
    print(f"Time to complete: {end - start}")
