import re
from typing import Dict, List, Tuple

DUMMY = "Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green\n\
        Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue\n\
        Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red\n\
        Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red\n\
        Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green)\n\
        "


def calculate_minimal_cubes(pick_list: List[int]) -> int:
    max_rgb = [0, 0, 0]
    for pick in pick_list:
        max_rgb = [max(max_rgb[id], elem) for id, elem in enumerate(pick)]
    return max_rgb[0] * max_rgb[1] * max_rgb[2]


def load_input_data(path: str) -> str:
    with open(path, "r") as file:
        return file.read()


def sum_game_ids(game_dict: Dict[str, Dict[str, int]]) -> int:
    valid_ids = (val["id"] for val in game_dict.values() if val["is_valid"])
    return sum(valid_ids)


def sum_minimal_mult(game_dict: Dict[str, Dict[str, int]]) -> int:
    return sum(
        calculate_minimal_cubes(val.get("pick_list")) for val in game_dict.values()
    )


def text2dict(text: str) -> Dict[str, Dict[str, int]]:
    lines = text.split("\n")
    pattern_game = r"game (\d+)"
    game_dict = {}
    for line in lines[:-1]:
        head, tail = re.split(r": ", line)
        match1 = re.search(pattern_game, head)
        game_name = match1.group(0)
        game_num = match1.group(1)
        game_dict[game_name] = {"id": int(game_num)}

        picks = re.split(r";", tail)
        pick_list = []
        for pick in picks:
            r = re.findall(r"(\d+) red", pick)
            if r:
                r = int(r[0])
            else:
                r = 0
            g = re.findall(r"(\d+) green", pick)
            if g:
                g = int(g[0])
            else:
                g = 0
            b = re.findall(r"(\d+) blue", pick)
            if b:
                b = int(b[0])
            else:
                b = 0
            pick_list.append((r, g, b))

        game_dict[game_name]["pick_list"] = pick_list
    return game_dict


def validate_dict(
    dict: Dict[str, Dict[str, int]], max_vals: Tuple[int]
) -> Dict[str, Dict[str, int]]:
    for name, val in dict.items():
        pick_list = val.get("pick_list")
        flag = False
        for pick in pick_list:
            for index in range(3):
                if pick[index] > max_vals[index]:
                    flag = True
                    break
            if flag:
                dict[name]["is_valid"] = False
                break
        else:
            dict[name]["is_valid"] = True
    return dict


if __name__ == "__main__":
    input_data = load_input_data("2023/Day_02.txt").lower()
    game_dict = text2dict(input_data)
    max_vals = (12, 13, 14)
    game_dict = validate_dict(game_dict, max_vals)
    result1 = sum_game_ids(game_dict)
    print(result1)

    result2 = sum_minimal_mult(game_dict)
    print(result2)
