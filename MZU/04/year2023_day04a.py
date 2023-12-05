import re
from timeit import default_timer as timer

from aocd import data

DAY = '04'
PART = 'a'


def solve(lines, number_of_winning_numbers):
    total_score = 0
    for line in lines:
        numbers_of_line = re.findall(r'\d+', line)
        winning_numbers = numbers_of_line[1:number_of_winning_numbers + 1]
        card_numbers = numbers_of_line[number_of_winning_numbers + 1:]
        line_score = 0
        for winning_number in winning_numbers:
            if winning_number in card_numbers:
                if line_score == 0:
                    line_score = 1
                else:
                    line_score = line_score * 2
        total_score = total_score + line_score

    return total_score


def main():
    print(f'Advent of Code 2023 --- Day {DAY} --- Part {PART}')

    lines = data.splitlines()
    result = solve(lines, 10)

    print(f'{str(result)}')


if __name__ == '__main__':
    start = timer()
    main()
    print(f"Completed in {timer() - start} sec")
