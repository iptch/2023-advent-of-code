# aoc_template.py

import pathlib
import sys
from parse import search

def parse_number(color, set):
    result = search("{:d} " + color, set)
    return 0 if result is None else result.fixed[0]

def parse_set(set):
    return [parse_number("red", set), parse_number("green", set), parse_number("blue", set)]

def parse(puzzle_input):
    """Parse input."""
    return [[parse_set(set) for set in line.split(";")] for line in puzzle_input.splitlines()]

def part1(data):
    """Solve part 1."""
    
    red_max = 12
    green_max = 13
    blue_max = 14

    result = 0

    for i, game in enumerate(data):
        red = max([set[0] for set in game])
        green = max([set[1] for set in game])
        blue = max([set[2] for set in game])

        if red <= red_max and green <= green_max and blue <= blue_max:
            result += i + 1

    return result

def part2(data):
    """Solve part 2."""

    result = 0

    for game in data:
        red = max([set[0] for set in game])
        green = max([set[1] for set in game])
        blue = max([set[2] for set in game])

        result += red * green * blue

    return result

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