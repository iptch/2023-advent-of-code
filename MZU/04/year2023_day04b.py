import re
from timeit import default_timer as timer

from aocd import data

DAY = '04'
PART = 'b'


def solve(lines, number_of_winning_numbers):
    total_cards = {i + 1: 1 for i in range(len(lines))}
    for idx, line in enumerate(lines):
        numbers_of_line = re.findall(r'\d+', line)
        winning_numbers = numbers_of_line[1:number_of_winning_numbers + 1]
        card_numbers = numbers_of_line[number_of_winning_numbers + 1:]
        line_score = len(list(set(winning_numbers) & set(card_numbers)))
        for i in range(line_score):
            total_cards[idx + 2 + i] += 1 * total_cards[idx + 1]

    return sum(total_cards.values())


def main():
    print(f'Advent of Code 2023 --- Day {DAY} --- Part {PART}')

    lines = data.splitlines()
    result = solve(lines, 10)

    print(f'{str(result)}')


if __name__ == '__main__':
    start = timer()
    main()
    print(f"Completed in {timer() - start} sec")
