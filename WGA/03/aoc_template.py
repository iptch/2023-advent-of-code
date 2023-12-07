# aoc_template.py

import pathlib
import sys
import re

REGEX_NUMBERS = r"\d+"
REGEX_SYMBOLS = r"[^\w\s.]"
REGEX_GEARS = r"\*"

def extract(regex, line):
    result = []

    for match in re.finditer(regex, line):
        result.append((match.group(), match.start(), match.end()))

    return result

def is_adjacent_to_symbol(data, row, col):
    for i in range(row - 1, row + 2):
        for j in range(col - 1, col + 2):
            if (0 <= i < len(data) and 0 <= j < len(data) and (i != row or j != col) and
                    re.search(REGEX_SYMBOLS, data[i][j]) is not None):
                return True

    return False

def get_adjacent_numbers(numbers_matrix, row, col):
    adjacent_numbers = []

    for i in range(row - 1, row + 2):
        if 0 <= i < len(numbers_matrix):
            for number in numbers_matrix[i]:
                if number[1] <= col + 1 and number[2] >= col:
                    adjacent_numbers.append(int(number[0]))

    return adjacent_numbers

def parse(puzzle_input):
    """Parse input."""
    return puzzle_input.split()

def part1(data):
    """Solve part 1."""

    result = 0

    numbers_matrix = [extract(REGEX_NUMBERS, line) for line in data]

    for i, numbers in enumerate(numbers_matrix):
        for j in numbers:
            for col in range(j[1], j[2]):
                if is_adjacent_to_symbol(data, i, col):
                    result += int(j[0])
                    break

    return result

def part2(data):
    """Solve part 2."""

    result = 0

    numbers_matrix = [extract(REGEX_NUMBERS, line) for line in data]
    gears_matrix = [extract(REGEX_GEARS, line) for line in data]

    for i, gears in enumerate(gears_matrix):
        for j in gears:
            adjacent_numbers = get_adjacent_numbers(numbers_matrix, i, j[1])

            if len(adjacent_numbers) == 2:
                result += adjacent_numbers[0] * adjacent_numbers[1]

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