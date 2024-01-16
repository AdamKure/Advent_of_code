import time
from functools import cache

DUMMY = "???.### 1,1,3\n\
.??..??...?##. 1,1,3\n\
?#?#?#?#?#?#?#? 1,3,1,6\n\
????.#...#... 4,1,1\n\
????.######..#####. 1,6,5\n\
?###???????? 3,2,1"


class SpringsMap:
    def __init__(self, springs_map: str, part2: bool = False) -> None:
        self.clusters = []
        self.damaged = []
        self.lengths = []
        self.operational = []
        self.springs = []
        self.unknown = []

        self.__parse(springs_map, part2)

    def __parse(self, springs_map: str, part2: bool) -> None:
        for line in springs_map:
            springs, numbers = line.split(" ")
            numbers = numbers.split(",")
            numbers = [int(n) for n in numbers]
            if part2:
                springs = (5 * (springs + "?"))[:-1]
                numbers = 5 * numbers
            operational = []
            damaged = []
            unknown = []
            for i, char in enumerate(springs):
                if char == ".":
                    operational.append(i)
                elif char == "#":
                    damaged.append(i)
                else:
                    unknown.append(i)
            self.clusters.append(numbers)
            self.damaged.append(damaged)
            self.lengths.append(len(springs))
            self.operational.append(operational)
            self.springs.append(springs)
            self.unknown.append(unknown)

    def find_combinations(self) -> int:
        @cache
        def iterate(springs, numbers):
            if len(numbers) < 1:
                return 1 if "#" not in springs else 0
            num_len = numbers[0]
            if num_len > len(springs):
                return 0
            count = 0
            char = springs[0]
            if char in "?.":
                count += iterate(springs[1:], numbers)
            if char in "?#":
                if "." in springs[:num_len]:
                    return count
                if num_len == len(springs):
                    return count if len(numbers) > 1 else count + 1
                if springs[num_len] in "#":
                    return count
                count += iterate(springs[num_len + 1 :], numbers[1:])
            return count

        total = 0
        for i, line in enumerate(self.springs[:]):
            cluster = self.clusters[i]
            count = iterate(tuple(line), tuple(cluster))
            total += count
        return total


def main():
    with open("2023\\Day_12.txt", "r") as file:
        input_data = file.read().split("\n")[:-1]

    # input_data = DUMMY.split("\n")

    # Part 1
    sm = SpringsMap(input_data)
    result1 = sm.find_combinations()
    print(f"Result 1 is: {result1}")

    # Part 2
    sm2 = SpringsMap(input_data, part2=True)
    result2 = sm2.find_combinations()
    print(f"Result 2 is: {result2}")


if __name__ == "__main__":
    start = time.perf_counter()
    main()
    end = time.perf_counter()
    print(f"\nExecuted in: {end - start} s")
