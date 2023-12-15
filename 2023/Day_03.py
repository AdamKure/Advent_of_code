import re

class SchematicsLine():
    def __init__(self, text, line_index):
        self.text = text.lower().replace("\n", "")
        self.line_index = line_index

    def get_line_numbers(self):
        search_pattern = r"\d+"
        number_list = [(int((match.group())), self.line_index, int(match.start()), int(match.end())) for match in re.finditer(search_pattern, self.text)]
        return number_list

    def get_line_symbols(self):
        search_pattern = r"[^\d.]"
        symbol_list = [(match.group(), self.line_index, int(match.start()), int(match.end()))for match in re.finditer(search_pattern, self.text)]
        return symbol_list


class EngineSchematics:
    def __init__(self, schematics):
        self.schematics_lines = {f"{index}": SchematicsLine(line, index) for index, line in enumerate(schematics)}
        self.line_width = len(schematics[0])
        self.numbers = self.get_numbers()
        self.symbols = self.get_symbols()

    def calculate_grid_proximity(self, line, start, end):
        up = max(line-1, 0)  # including
        down = min(line+2, len(self.schematics_lines))  # excluding
        left = max(start-1, 0)  # including
        right = min(end+1, self.line_width)  # excluding
        return (up, down, left, right)

    def get_gear_numbers(self):
        gear_numbers = []
        for symbol, line, start, end in self.symbols:
            if symbol == "*":
                search_area = self.calculate_grid_proximity(line, start, end)
                connected_numbers = [number_tup[0] for number_tup in self.numbers if self.is_connected_to(search_area, [number_tup])]
                if len(connected_numbers) == 2:
                    gear_numbers.append(connected_numbers[0]*connected_numbers[1])
        return gear_numbers

    def get_numbers(self):
        number_list = []
        for line in self.schematics_lines.values():
            numbers = line.get_line_numbers()
            if len(numbers) < 1:
                continue
            else:
                number_list.extend(numbers)
        return number_list

    def get_symbols(self):
        symbol_list = []
        for line in self.schematics_lines.values():
            symbols = line.get_line_symbols()
            if len(symbols) < 1:
                continue
            else:
                symbol_list.extend(symbols)
        return symbol_list

    def get_valid_numbers(self):
        valid_numbers = []
        for number, line, start, end in self.numbers:
            search_area = self.calculate_grid_proximity(line, start, end)
            if self.is_connected_to(search_area, self.symbols):
                valid_numbers.append(number)
        return valid_numbers

    def is_connected_to(self, searched_area, search_target):
        for target in search_target:
            if searched_area[0] <= target[1] < searched_area[1]:
                if searched_area[2] <= target[2] < searched_area[3]:
                    return True
                if searched_area[2] <= target[3]-1 < searched_area[3]:
                    return True
        return False


def main():
    with open(r"2023\Day_03.txt", "r") as file:
        data = file.readlines()

    engine1 = EngineSchematics(data)
    result1 = sum(engine1.get_valid_numbers())
    print(result1)
    result2 = sum(engine1.get_gear_numbers())
    print(result2)


if __name__ == "__main__":
    main()