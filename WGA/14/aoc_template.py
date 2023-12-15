# aoc_template.py

import pathlib
import sys

def transpose(data):
    return [[row[i] for row in data] for i in range(len(data[0]))]

def tilt(line):
    cubic_rocks = [i for i, x in enumerate(line) if x == "#"]

    for i, cubic_rock in enumerate(cubic_rocks[0:-1]):
        round_rocks = 0

        for j, x in enumerate(line[cubic_rock : cubic_rocks[i + 1]]):
            if x == "O":
                round_rocks += 1
                line[cubic_rock + j] = "."
                line[cubic_rock + round_rocks] = "O"

    return line

def tilt_north(data):
    return transpose([tilt(line) for line in transpose(data)])

def tilt_west(data):
    return [tilt(line) for line in data]

def tilt_south(data):
    return transpose([list(reversed(tilt(list(reversed(line))))) for line in transpose(data)])

def tilt_east(data):
    return [list(reversed(tilt(list(reversed(line))))) for line in data]

def parse(puzzle_input):
    """Parse input."""

    lines = [list("#" + line + "#") for line in puzzle_input.splitlines()]
    border = [["#"] * len(lines[0])]

    return border + lines + border

def part1(data):
    """Solve part 1."""

    return sum([sum([len(line) - i - 1 for i, x in enumerate(line) if x == "O"]) for line in transpose(tilt_north(data))])

def part2(data):
    """Solve part 2."""

    loads = []
    positions = data

    for _ in range(3):
        positions = tilt_east(tilt_south(tilt_west(tilt_north(positions))))
        loads.append(sum([sum([len(line) - i - 1 for i, x in enumerate(line) if x == "O"]) for line in transpose(positions)]))

    for line in positions:
        print("".join(line))

    return 0

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