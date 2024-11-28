import time
from collections import deque


def main() -> None:
    with open("2023/Day_25_example.txt", "r") as file:
        input_data = file.read()

    # with open("2023/Day_25.txt", "r") as file:
    #     input_data = file.read()

    # Part 1
    # Parse input
    edges = {}
    for line in input_data.splitlines():
        l, right = line.split(": ")
        r_list = right.split(" ")

        if l not in edges:
            edges[l] = []

        # Add the bidirectional edge
        for r in r_list:
            if r not in edges:
                edges[r] = []
            edges[l].append(r)
            edges[r].append(l)

    # Breadth-first search for shortest path
    graph = {}
    for node in set(edges):
        if node not in graph:
            graph[node] = {}
        path = []
        q = deque([(node, path)])
        while q:
            current, path = q.popleft()

            # Skip already visited nodes
            if current in graph[node]:
                continue

            # Store the path for each node
            path.append(current)
            graph[node][
                current
            ] = path.copy()  # Copy the list to avoid reference issues
            next_nodes = edges[current]
            for next_node in next_nodes:
                q.append(
                    (next_node, path.copy())
                )  # Copy the list to avoid reference issues

    # Find most used edges
    edge_cost = {node: {n: 0 for n in edges} for node in edges}
    most_used = [(0, "aaa", "bbb"), (0, "aaa", "bbb"), (0, "aaa", "bbb")]
    for dic in graph.values():
        for path in dic.values():
            for i, n in enumerate(path[:-1]):
                a, b = n, path[i + 1]
                edge_cost[a][b] += 1

                # Check if the edge is already in most_used
                edge_in_most_used = False
                for j, _ in enumerate(most_used):
                    if (most_used[j][1] == a and most_used[j][2] == b) or (
                        most_used[j][1] == b and most_used[j][2] == a
                    ):
                        edge_in_most_used = True
                        # If the edge is already in most_used and the current edge is greater, replace it
                        if edge_cost[a][b] > most_used[j][0]:
                            most_used[j] = (edge_cost[a][b], a, b)
                        break

                # If the edge is not in most_used, compare integers and replace the edge with the lowest value in most_used if the current edge is greater
                if not edge_in_most_used and edge_cost[a][b] > most_used[-1][0]:
                    most_used[-1] = (edge_cost[a][b], a, b)

                # Sort most_used by the edge cost in descending order
                most_used.sort(key=lambda x: x[0], reverse=True)

    # Remove edges with highest cost
    for i in range(3):
        a, b = most_used[i][1], most_used[i][2]
        edges[a].remove(b)
        edges[b].remove(a)

    # Find group sizes after removing the edges
    group_1_node = a
    group_1 = set()
    q = deque([group_1_node])
    while q:
        current = q.popleft()
        if current in group_1:
            continue
        group_1.add(current)
        next_nodes = edges[current]
        for next_node in next_nodes:
            q.append(next_node)

    group_1_size = len(group_1)
    group_2_size = len(set(edges)) - group_1_size

    print(f"Final result is: {group_1_size * group_2_size}")


if __name__ == "__main__":
    start = time.perf_counter()
    main()
    end = time.perf_counter()
    print(f"\nExecuted in: {end - start} s")
