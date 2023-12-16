# aoc_template.py

import pathlib
import sys
import copy

class Color:
    BLUE = "\033[94m"
    GREEN = "\033[92m"
    RED = "\033[91m"
    ENDC = "\033[0m"

def get_start_tile(graph):
    for y, line in enumerate(graph):
        x = line.index("S") if "S" in line else -1

        if x > -1:
            return (y, x, "S")

def get_steps(steps, graph, visited_graph):
    prev_tile = steps[-1]
    visited_graph[prev_tile[0]][prev_tile[1]] = "X"

    if prev_tile[2] == "S" and len(steps) > 1:
        return steps
    
    steps_north = steps_east = steps_south = steps_west = steps

    # Search north
    next_pos = (prev_tile[0] - 1, prev_tile[1])

    if next_pos[0] >= 0 and prev_tile[2] in ["S", "J", "|", "L"]:
        next_tile = (next_pos[0], next_pos[1], graph[next_pos[0]][next_pos[1]])
        has_been_visited = visited_graph[next_tile[0]][next_tile[1]] == "X"

        if next_tile[2] in ["S", "7", "|", "F"] and not has_been_visited:
            steps_north = get_steps(steps + [(next_tile)], graph, visited_graph)

    # Search east
    next_pos = (prev_tile[0], prev_tile[1] + 1)

    if next_pos[1] < len(graph[prev_tile[0]]) and prev_tile[2] in ["S", "L", "-", "F"]:
        next_tile = (next_pos[0], next_pos[1], graph[next_pos[0]][next_pos[1]])
        has_been_visited = visited_graph[next_tile[0]][next_tile[1]] == "X"

        if next_tile[2] in ["S", "J", "-", "7"] and not has_been_visited:
            steps_east = get_steps(steps + [(next_tile)], graph, visited_graph)
        
    # Search south
    next_pos = (prev_tile[0] + 1, prev_tile[1])

    if next_pos[0] < len(graph) and prev_tile[2] in ["S", "F", "|", "7"]:
        next_tile = (next_pos[0], next_pos[1], graph[next_pos[0]][next_pos[1]])
        has_been_visited = visited_graph[next_tile[0]][next_tile[1]] == "X"

        if next_tile[2] in ["S", "L", "|", "J"] and not has_been_visited:
            steps_south = get_steps(steps + [(next_tile)], graph, visited_graph)

    # Search west    
    next_pos = (prev_tile[0], prev_tile[1] - 1)

    if next_pos[1] >= 0 and prev_tile[2] in ["S", "7", "-", "J"]:
        next_tile = (next_pos[0], next_pos[1], graph[next_pos[0]][next_pos[1]])
        has_been_visited = visited_graph[next_tile[0]][next_tile[1]] == "X"

        if next_tile[2] in ["S", "F", "-", "L"] and not has_been_visited:
            steps_west = get_steps(steps + [(next_tile)], graph, visited_graph)

    return max(steps_north, steps_east, steps_south, steps_west, key=lambda x: len(x))

def get_enclosed_tiles(steps, graph):
    tiles = []

    for y, line in enumerate(graph):
        is_enclosed = 0

        for x, tile in enumerate(line):
            matching_steps = [n for n, step in enumerate(steps) if (step[0] == y and step[1] == x)]

            if len(matching_steps) == 1:
                n_current = matching_steps[0]

                if y < len(graph):
                    n_prev = (n_current - 1) if n_current > 0 else len(steps) - 1
                    n_next = (n_current + 1) if n_current < len(steps) - 1 else 0

                    if steps[n_prev][0] == y + 1 and steps[n_prev][1] == x:
                        is_enclosed += 1
                    elif steps[n_next][0] == y + 1 and steps[n_next][1] == x:
                        is_enclosed -= 1
            elif is_enclosed != 0:
                tiles.append((y, x, tile))

    return tiles

def print_graph(steps, tiles, graph):
    graph[steps[0][0]][steps[0][1]] = Color.RED + "S" + Color.ENDC

    for step in steps[1:]:
        graph[step[0]][step[1]] = Color.BLUE + graph[step[0]][step[1]] + Color.ENDC

    for tile in tiles:
        graph[tile[0]][tile[1]] = Color.GREEN + graph[tile[0]][tile[1]] + Color.ENDC

    for line in graph:
        print("".join(line))

def parse(puzzle_input):
    """Parse input."""

    return [list(line) for line in puzzle_input.splitlines()]

def part1(data):
    """Solve part 1."""

    start_tile = get_start_tile(data)
    steps = get_steps([start_tile], data, copy.deepcopy(data))

    return int(len(steps) / 2)

def part2(data):
    """Solve part 2."""

    start_tile = get_start_tile(data)
    steps = get_steps([start_tile], data, copy.deepcopy(data))
    tiles = get_enclosed_tiles(steps, data)
    print_graph(steps, tiles, copy.deepcopy(data))

    return len(tiles)

def solve(puzzle_input):
    """Solve the puzzle for the given input."""
    data = parse(puzzle_input)
    solution1 = part1(data)
    solution2 = part2(data)

    return solution1, solution2

if __name__ == "__main__":
    sys.setrecursionlimit(20000)

    for path in sys.argv[1:]:
        print(f"{path}:")
        puzzle_input = pathlib.Path(path).read_text().strip()
        solutions = solve(puzzle_input)
        print("\n".join(str(solution) for solution in solutions))