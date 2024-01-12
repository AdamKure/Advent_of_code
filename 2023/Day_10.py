import time
from typing import Dict, List, Set, Tuple, Union

DUMMY = "7-F7-\n\
.FJ|7\n\
SJLL7\n\
|F--J\n\
LJ.LJ"

DUMMY2 = "...........\n\
.S-------7.\n\
.|F-----7|.\n\
.||.....||.\n\
.||.....||.\n\
.|L-7.F-J|.\n\
.|..|.|..|.\n\
.L--J.L--J.\n\
..........."

DUMMY3 = ".F----7F7F7F7F-7....\n\
.|F--7||||||||FJ....\n\
.||.FJ||||||||L7....\n\
FJL7L7LJLJ||LJ.L-7..\n\
L--J.L7...LJS7F-7L7.\n\
....F-J..F7FJ|L7L7L7\n\
....L7.F7||L7|.L7L7|\n\
.....|FJLJ|FJ|F7|.LJ\n\
....FJL-7.||.||||...\n\
....L---J.LJ.LJLJ..."

TRANS = {
    "|": ((-1, 0), (1, 0)),
    "-": ((0, -1), (0, 1)),
    "L": ((-1, 0), (0, 1)),
    "J": ((-1, 0), (0, -1)),
    "7": ((0, -1), (1, 0)),
    "F": ((0, 1), (1, 0)),
    "S": ((-1, 0), (0, -1), (0, 1), (1, 0)),
}


class PipeArray:
    def __init__(self, text: str):
        self.array = None
        self.edges = None
        self.start = None
        self.start_dirs = None
        self.text = text

        self.__parse()

    def __parse(self):
        r, c = 0, 0
        array = {}
        edges = (0, 0)
        for char in self.text:
            if char == "\n":
                r += 1
                c = 0
                continue
            if r > edges[0] or c > edges[1]:
                edges = (max(edges[0], r), max(edges[1], c))
            if char == ".":
                c += 1
                continue
            if char == "S":
                self.start = (r, c)
            array[(r, c)] = TRANS.get(char)
            c += 1
        self.array = array
        self.edges = edges

    # def __within_boundaries(self, pos: Tuple[int]) -> bool:
    #     return 0 <= pos[0] <= self.edges[0] and 0 <= pos[1] <= self.edges[1]

    def __area_inside_pipe(self, path: Set[Tuple[int]]):
        stop_switching = False
        counting = False
        state = (0, 0)
        count = 0
        for row in range(self.edges[0] + 1):
            state = (0, 0)
            counting = False
            for col in range(self.edges[1] + 1):
                if (row, col) not in path:
                    if counting and not stop_switching:
                        count += 1
                    continue
                if (row, col) == self.start:
                    conns = self.start_dirs
                else:
                    conns = self.array.get((row, col))
                dif = (0, 0)
                for item in conns:
                    dif = (dif[0] + item[0], dif[1] + item[1])
                if dif == (0, 0) and stop_switching:
                    continue
                if dif == (0, 0) and not stop_switching:
                    counting = not counting
                    continue
                stop_switching = not stop_switching
                state = (state[0] + dif[0], state[1] + dif[1])
                if state == (0, 0):
                    counting = not counting
                if not state[0] % 2 and not state[1] % 2:
                    state = (0, 0)
        return count

    def find_animal_pipe(self) -> List[List[Union[Tuple[int], int]]]:
        if not self.array or not self.start or not self.edges:
            self.__parse()
        possible_routes = []
        for start_dire in self.array.get(self.start):
            self.start_dirs = [start_dire]
            dire = start_dire
            cur = self.start
            path = set()
            is_closed = False
            while True:
                path.update([(cur)])
                next_el = (cur[0] + dire[0], cur[1] + dire[1])
                if next_el == self.start:
                    is_closed = True
                    break
                if next_el not in self.array:
                    break
                # if not self.__within_boundaries(next_el):
                #     break

                dire_oppo = tuple(-el for el in dire)
                next_conns = self.array[next_el]
                if dire_oppo not in next_conns:
                    break
                if next_conns[0] == dire_oppo:
                    dire = next_conns[1]
                elif next_conns[1] == dire_oppo:
                    dire = next_conns[0]
                else:
                    break
                cur = next_el
            if is_closed:
                self.start_dirs.append(tuple(-el for el in dire))
                area = self.__area_inside_pipe(sorted(path))
                possible_routes += [start_dire, path, area]
                break
        return possible_routes

    def get_array(self) -> Dict[Tuple[int], str]:
        if self.array:
            return self.array
        self.__parse()
        return self.array

    def get_start(self) -> Tuple[int]:
        if self.start:
            return self.start
        self.__parse()
        return self.start


def main():
    with open(r"2023\Day_10.txt", "r") as file:
        input_data = file.read()

    # input_data = DUMMY3

    pipes = PipeArray(input_data)
    paths = pipes.find_animal_pipe()
    result1 = int(len(paths[1]) / 2)
    print(f"Result 1 is: {result1}")
    result2 = paths[2]
    print(f"Result 2 is: {result2}")


if __name__ == "__main__":
    start = time.perf_counter()
    main()
    end = time.perf_counter()
    print(f"Code has executed in: {end - start} s")
