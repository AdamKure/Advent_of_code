import re
import time
from math import lcm


def main():
    with open(r"2023\Day_08.txt", "r") as file:
        input_data = file.readlines()

    directions = input_data[0].replace("\n", "")
    data = (line.replace("\n", "") for line in input_data[2:])
    nodes = {}
    for line in data:
        match = re.search(r"(\w+|\d+) = \((\w+|\d+), (\w+|\d+)\)", line)
        node, left, right = match.group(1, 2, 3)
        nodes[node] = (left, right)

    node = "AAA"
    count = 0
    while node != "ZZZ":
        d = directions[count % len(directions)]
        if d == "L":
            node = nodes[node][0]
        else:
            node = nodes[node][1]
        count += 1
    print(count)

    # Part 2
    def get_path_steps(start_node):
        node = start_node
        count = 0
        while node[2] != "Z":
            d = directions[count % len(directions)]
            if d == "L":
                node = nodes[node][0]
            else:
                node = nodes[node][1]
            count += 1
        return count

    a_nodes = [node for node in nodes.keys() if node[2] == "A"]
    lengths = [get_path_steps(node) for node in a_nodes]
    print(lcm(*lengths))


if __name__ == "__main__":
    start = time.perf_counter()
    main()
    end = time.perf_counter()
    print(end - start)
