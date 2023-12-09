# aoc_template.py

import pathlib
import sys

def get_diff(numbers):
    return [numbers[i + 1] - numbers[i] for i in range(len(numbers) - 1)]

def get_prediction(line, forwards = True):                      
    sequences = [line if forwards else list(reversed(line))]
    i = 0

    while any(number != 0 for number in sequences[i]):
        sequences.append(get_diff(sequences[i]))
        i += 1

    prediction = sequences[-1][-1]

    for sequence in list(reversed(sequences))[1:]:
        prediction += sequence[-1]

    return prediction

def parse(puzzle_input):
    """Parse input."""

    return [[int(number) for number in line.split()] for line in puzzle_input.splitlines()]

def part1(data):
    """Solve part 1."""

    return sum([get_prediction(line) for line in data])

def part2(data):
    """Solve part 2."""

    return sum([get_prediction(line, False) for line in data])

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