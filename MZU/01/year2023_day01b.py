import re
from timeit import default_timer as timer

from aocd import data

DAY = '1'
PART = 'b'

REPLACEMENTS = {
    'one': 'o1e',
    'two': 't2o',
    'three': 't3e',
    'four': 'f4r',
    'five': 'f5e',
    'six': 's6x',
    'seven': 's7n',
    'eight': 'e8t',
    'nine': 'n9e'
}


def solve(lines):
    calibration_values = []
    for line in lines:
        for k, v in REPLACEMENTS.items():
            line = line.replace(k, v)
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
