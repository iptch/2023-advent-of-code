# aoc_template.py

import pathlib
import sys
import re

def text2digit(text):
    if text.isdigit():
        return text
    if text == "one":
        return "1"
    if text == "two":
        return "2"
    if text == "three":
        return "3"
    if text == "four":
        return "4"
    if text == "five":
        return "5"
    if text == "six":
        return "6"
    if text == "seven":
        return "7"
    if text == "eight":
        return "8"
    if text == "nine":
        return "9"

# Requires lookahead to also find overlapping matches (e.g. "fiveight")
REGEX = r"(?=(\d|one|two|three|four|five|six|seven|eight|nine))"

def parse(puzzle_input):
    """Parse input."""
    return puzzle_input.split()

def part1(data):
    """Solve part 1."""
    result = 0

    for line in data:
        matches = re.findall(r"\d", line)
        result += int("".join(matches[0] + matches[-1]))

    return result

def part2(data):
    """Solve part 2."""
    result = 0

    for line in data:
        matches = re.findall(REGEX, line)
        result += int("".join(text2digit(matches[0]) + text2digit(matches[-1])))

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