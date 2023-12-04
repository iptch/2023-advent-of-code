import re

from aocd.models import Puzzle


def puzzle_1():
    result = 0

    for line in lines:
        numbers = line.split(": ")[1].split(" | ")
        winning_numbers = re.findall(r"\d+", numbers[0])
        my_numbers = re.findall(r"\d+", numbers[1])
        matches = set(winning_numbers).intersection(my_numbers)
        if len(matches) > 0:
            result += pow(2, len(matches) - 1)

    print(f"result {result}")
    # submit(result)


def puzzle_2():
    result = 0
    pattern = r"(\d+):"

    scratchcards = {}
    for line in lines:
        match = re.search(pattern, line)
        if match:
            card = int(match.group(1))
            scratchcards[card] = 1

    for line in lines:
        match = re.search(pattern, line)
        if match:
            card = int(match.group(1))
            numbers = line.split(": ")[1].split(" | ")
            winning_numbers = re.findall(r"\d+", numbers[0])
            my_numbers = re.findall(r"\d+", numbers[1])
            number_of_matches = set(winning_numbers).intersection(my_numbers)
            for index in range(len(number_of_matches)):
                scratchcards[card + index + 1] += scratchcards[card]
            result += scratchcards[card]

    print(f"result {result}")
    # submit(result)


if __name__ == "__main__":
    puzzle = Puzzle(year=2023, day=4)
    lines = puzzle.input_data.splitlines()

    # f = open("input.txt", "r")
    # lines = []
    # for line in f:
    #     lines.append(line.replace("\n", ""))
    puzzle_1()
    # puzzle_2()
