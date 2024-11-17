import time


def parse_map(file_path):
    with open(file_path, "r") as file:
        return [list(line.strip()) for line in file]


def is_valid_move(x, y):
    global maze_map, rows, cols
    if (0 <= x < rows and 0 <= y < cols) and (maze_map[x][y] in ".^v<>"):
        return True
    return False


def simplify_nodes(maze_map):
    global rows, cols
    start_x, start_y = 0, maze_map[0].index(".")
    end_x, end_y = len(maze_map) - 1, maze_map[-1].index(".")
    nodes = [(start_x, start_y), (end_x, end_y)]
    for r in range(rows):
        for c in range(cols):
            if not is_valid_move(r, c):
                continue
            neighboors = 0
            for dr, dc in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                if is_valid_move(r + dr, c + dc):
                    neighboors += 1
            if neighboors > 2:
                nodes.append((r, c))
    return nodes


def get_edges(nodes):
    directions = {
        ".": [(0, 1), (1, 0), (0, -1), (-1, 0)],
        "^": [(-1, 0)],
        "v": [(1, 0)],
        ">": [(0, 1)],
        "<": [(0, -1)],
    }
    edges = {node: {} for node in nodes}
    for sr, sc in nodes:
        stack = [(sr, sc, 0, {(sr, sc)})]
        while stack:
            r, c, n, visited = stack.pop()

            if n != 0 and (r, c) in nodes:
                edges[(sr, sc)][(r, c)] = n
                continue

            # For part 1
            # for dr, dc in directions[maze_map[r][c]]:
            #     nr, nc = r + dr, c + dc
            #     if is_valid_move(nr, nc) and (nr, nc) not in visited:
            #         stack.append((nr, nc, n + 1, visited.union({(nr, nc)})))

            # For part 2
            for dr, dc in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                nr, nc = r + dr, c + dc
                if is_valid_move(nr, nc) and (nr, nc) not in visited:
                    stack.append((nr, nc, n + 1, visited.union({(nr, nc)})))

    return edges


def dfs(nodes, edges):
    start, end = nodes[:2]
    stack = [(start, 0, {start})]
    longest_path = 0
    while stack:
        node, steps, visited = stack.pop()
        if node == end:
            # print(f"Path: {steps}")
            longest_path = max(longest_path, steps)
            continue
        for next_node, dist in edges[node].items():
            if next_node not in visited:
                stack.append((next_node, steps + dist, visited.union({next_node})))
    return longest_path


def main():
    global maze_map, rows, cols, start_x, start_y, end_x, end_y
    # Example
    # maze_map = parse_map("2023/Day_23_example.txt")
    # Real input
    maze_map = parse_map("2023/Day_23.txt")
    rows, cols = len(maze_map), len(maze_map[0])
    nodes = simplify_nodes(maze_map)
    edges = get_edges(nodes)
    lp = dfs(nodes, edges)
    print(f"Longest hike length: {lp}")


if __name__ == "__main__":
    start = time.perf_counter()
    main()
    end = time.perf_counter()
    print(f"\nExecuted in: {end - start} s")
