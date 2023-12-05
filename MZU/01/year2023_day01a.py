import re
from timeit import default_timer as timer

from aocd import data

DAY = '1'
PART = 'a'


def solve(lines):
    calibration_values = []
    for line in lines:
        numbers = re.findall(r'\d', line)
        calibration_values.append(int(f'{numbers[0]}{numbers[-1]}'))

    return sum(calibration_values)


def main():
    print(f'Advent of Code 2023 --- Day {DAY} --- Part {PART}')

    lines = data.splitlines()
    result = solve(lines)

    print(f'{str(result)}')


if __name__ == '__main__':
    start = timer()
    main()
    print(f"Completed in {timer() - start} sec")
