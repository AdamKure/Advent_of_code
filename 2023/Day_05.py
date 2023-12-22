import re
import time

class Converter:
    def __init__(self, s2s_map, s2f_map, f2w_map, w2l_map, l2t_map, t2h_map, h2l_map):
        self.s2s_map = s2s_map
        self.s2f_map = s2f_map
        self.f2w_map = f2w_map
        self.w2l_map = w2l_map
        self.l2t_map = l2t_map
        self.t2h_map = t2h_map
        self.h2l_map = h2l_map

    def map_numbers(self, map_raw, seed_numbers):
        seed_start, seed_length = seed_numbers
        seed_end = seed_start + seed_length
        lines = map_raw.split("\n")
        maps = [line.split(" ") for line in lines if line]
        map_list = [(int(dest), int(st), int(le)) for dest, st, le in maps]
        for map_dest, map_start, map_length in map_list:
            map_end = map_start+map_length
            if map_start <= seed_start < map_end:
                offset = map_dest - map_start
                if seed_end <= map_end:
                    return [(seed_start + offset, seed_length)]
                head = [(seed_start + offset, map_end - seed_start)]
                t = (map_end, seed_end - map_end)
                tail = self.map_numbers(map_raw, t)
                return head + tail
            if seed_start < map_start < seed_end:
                h = (seed_start, map_start - seed_start)
                t = (map_start, seed_end - map_start)
                head = self.map_numbers(map_raw, h)
                tail = self.map_numbers(map_raw, t)
                return head + tail
        return [(seed_start, seed_length)]

    def seed2location(self, seed_num):
        soil = self.map_numbers(self.s2s_map, seed_num)
        fert = [self.map_numbers(self.s2f_map, so) for so in soil]
        water = [self.map_numbers(self.f2w_map, fe) for fe_li in fert for fe in fe_li]
        light = [self.map_numbers(self.w2l_map, wa) for wa_li in water for wa in wa_li]
        temp = [self.map_numbers(self.l2t_map, li) for li_li in light for li in li_li]
        hum = [self.map_numbers(self.t2h_map, te) for te_li in temp for te in te_li]
        loc = [self.map_numbers(self.h2l_map, hu) for hu_li in hum for hu in hu_li]
        res = [location[0] for lo in loc for location in lo]
        return res

def main():
    with open(r"2023\Day_05.txt", "r") as file:
        input_data = file.read().lower()

    seeds, seed2soil, soil2fert, fert2water, water2light, light2temp, temp2hum, hum2loc = input_data.split("\n\n")
    _, s2s_map = seed2soil.split("\n", maxsplit=1)
    _, s2f_map = soil2fert.split("\n", maxsplit=1)
    _, f2w_map = fert2water.split("\n", maxsplit=1)
    _, w2l_map = water2light.split("\n", maxsplit=1)
    _, l2t_map = light2temp.split("\n", maxsplit=1)
    _, t2h_map = temp2hum.split("\n", maxsplit=1)
    _, h2l_map = hum2loc.split("\n", maxsplit=1)

    Conv = Converter(s2s_map, s2f_map, f2w_map, w2l_map, l2t_map, t2h_map, h2l_map)

    # Part 1 
    seed_nums = ((int(seed_num), 1) for seed_num in re.findall(r"(\d+)", seeds))
    locations = (Conv.seed2location(seed) for seed in seed_nums)
    print(min(location for loc_list in locations for location in loc_list))

    # Part 2
    seed_numbers = [int(seed_num) for seed_num in re.findall(r"(\d+)", seeds)]
    seed_nums = ((seed_num, seed_numbers[2*index+1]) for index, seed_num in enumerate(seed_numbers[::2]))
    locations = [location for seed in seed_nums for location in Conv.seed2location(seed)]
    print(min(locations))


if __name__ == "__main__":
    start = time.perf_counter()
    main()
    end = time.perf_counter()
    print(end - start)
