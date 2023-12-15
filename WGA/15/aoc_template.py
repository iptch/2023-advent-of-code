# aoc_template.py

import pathlib
import sys

def get_hash(str):
    count = 0

    for character in str:
        count = (count + ord(character)) * 17 % 256

    return count

def parse(puzzle_input):
    """Parse input."""

    return puzzle_input.split(",")

def part1(data):
    """Solve part 1."""

    return sum([get_hash(step) for step in data])

def part2(data):
    """Solve part 2."""

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