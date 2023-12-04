from timeit import default_timer as timer
import re


def puzzle_1():
    result = 0
    input_txt = open("input.txt", "r")
    lines = [line.rstrip() for line in input_txt]
    for line_index, line in enumerate(lines):
        groups = re.match(r"Card +\d+:([0-9 ]+) \|([0-9 ]+)", line).groups()
        winning_number = set(re.findall(r"( [0-9 ][0-9])", groups[0]))
        numbers_i_have = set(re.findall(r"( [0-9 ][0-9])", groups[1]))
        matching_numbers = len(winning_number.intersection(numbers_i_have))
        if matching_numbers > 0:
            result += 2 ** (matching_numbers-1)
    return result


def puzzle_2():
    input_txt = open("input.txt", "r")
    lines = [line.rstrip() for line in input_txt]
    cards = [1] * len(lines)
    for line_index, line in enumerate(lines):
        groups = re.match(r"Card +(\d+):([0-9 ]+) \|([0-9 ]+)", line).groups()
        card_number = int(groups[0])-1
        winning_number = set(re.findall(r"( [0-9 ][0-9])", groups[1]))
        numbers_i_have = set(re.findall(r"( [0-9 ][0-9])", groups[2]))
        matching_numbers = len(winning_number.intersection(numbers_i_have))
        for i in range(card_number + 1, card_number + 1 + matching_numbers):
            cards[i] += cards[card_number]
    return sum(cards)


if __name__ == '__main__':
    start1 = timer()
    print(f"Puzzle 1: {puzzle_1()} (in {timer()-start1}sec)")
    start2 = timer()
    print(f"Puzzle 2: {puzzle_2()} (in {timer()-start2}sec)")