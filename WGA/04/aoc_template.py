# aoc_template.py

import pathlib
import sys
import re
import numpy

def get_copies(card):
    points = 0

    for number in card[0]:
        if number in card[1]:
            points += 1

    return points

def parse(puzzle_input):
    """Parse input."""

    lines = puzzle_input.splitlines()
    result = [None] * len(lines)

    for i, line in enumerate(lines):
        str = re.sub(r"Card\s+\d+: ", "", line).split("|")
        winning_numbers = [int(line.group()) for line in list(re.finditer(r"\d+", str[0]))]
        my_numbers = [int(line.group()) for line in list(re.finditer(r"\d+", str[1]))]
        result[i] = [winning_numbers, my_numbers]

    return result

def part1(data):
    """Solve part 1."""

    result = 0
 
    for card in data:
        copies = get_copies(card)
        result += 0 if copies == 0 else pow(2, copies - 1)

    return result

def part2(data):
    """Solve part 2."""

    cards = numpy.ones(len(data), dtype=int)

    for i, card in enumerate(cards):
        copies = get_copies(data[i])

        for k in range(i + 1, min(i + copies + 1, len(cards))):
            cards[k] += card

    return numpy.sum(cards)

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