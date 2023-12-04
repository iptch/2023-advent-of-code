# aoc_template.py

import pathlib
import sys
import re

def get_cards(data, i):
    if i < len(data):
        number_of_copies = 0

        for number in data[i][0]:
            if number in data[i][1]:
                number_of_copies += 1

        number_of_cards = 1

        for point in range(1, number_of_copies + 1):
            number_of_cards += get_cards(data, i + point)

        return number_of_cards
    
    return 0

def parse(puzzle_input):
    """Parse input."""

    result = []

    for line in puzzle_input.splitlines():
        str = re.sub(r'Card\s+\d+: ', '', line).split("|")
        winning_numbers = [int(line.group()) for line in list(re.finditer(r'\d+', str[0]))]
        my_numbers = [int(line.group()) for line in list(re.finditer(r'\d+', str[1]))]
        result.append([winning_numbers, my_numbers])

    return result

def part1(data):
    """Solve part 1."""

    result = 0

    for card in data:
        points = 0

        for number in card[0]:
            if number in card[1]:
                points = 1 if points == 0 else points * 2

        result += points

    return result

def part2(data):
    """Solve part 2."""

    result = 0

    for i in range(0, len(data)):
        result += get_cards(data, i)

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