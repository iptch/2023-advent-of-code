# aoc_template.py

import pathlib
import sys
import re
import math

def get_step(instructions, nodes, start_element, stop_regex):

    element = start_element
    step = 0

    while re.match(stop_regex, element) is None:
        i = step % len(instructions)
        instruction = instructions[i]
        element = next(node for node in nodes if node[0] == element)[1 if instruction == "L" else 2]
        step += 1
        
    return step

def lcm_of_array(integers):
    result = integers[0]

    for integer in integers[1:]:
        result = math.lcm(result, integer)

    return result

def parse(puzzle_input):
    """Parse input."""

    lines = puzzle_input.splitlines()
    result = {}

    result["instructions"] = list(lines[0])
    result["nodes"] = [re.findall(r"[A-Z|1-9]{3}", line) for line in lines[2:]]

    return result

def part1(data):
    """Solve part 1."""

    return get_step(data["instructions"], data["nodes"], "AAA", r"ZZZ")

def part2(data):
    """Solve part 2."""

    instructions, nodes = data["instructions"], data["nodes"]
    start_elements = [node[0] for node in nodes if node[0].endswith("A")]
    steps = [get_step(instructions, nodes, start_element, r"[A-Z|1-9]{2}Z") for start_element in start_elements]
        
    return lcm_of_array(steps)

def solve(puzzle_input):
    """Solve the puzzle for the given input."""
    data = parse(puzzle_input)
    solution1 = part1(data)
    solution2 = part2(data)

    return solution1, solution2

if __name__ == "__main__":
    for path in sys.argv[1:]:
        print(f"{path}:")
        puzzle_input = pathlib.Path(path).read_text().strip()
        solutions = solve(puzzle_input)
        print("\n".join(str(solution) for solution in solutions))