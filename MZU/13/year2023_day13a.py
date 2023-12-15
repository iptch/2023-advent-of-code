from timeit import default_timer as timer

import numpy
from aocd import data

DAY = '13'
PART = 'a'


def read_patterns(lines):
    patterns = []

    pattern = []
    for line in lines:
        if not line:
            patterns.append(pattern)
            pattern = []
        else:
            pattern.append(line)
    patterns.append(pattern)

    return patterns


def is_middle_of_reflection(row_idx, pattern):
    result = True
    counter = 1
    for i in range(row_idx + 1, 2 * (row_idx + 1), 1):
        try:
            if pattern[i] != pattern[i - counter]:
                result = False
                break
            counter += 2
        except IndexError:
            break
    return result


def solve(lines):
    patterns = read_patterns(lines)
    result = 0
    for pattern in patterns:
        for row_idx in range(len(pattern) - 1):
            if is_middle_of_reflection(row_idx, pattern):
                result += (row_idx + 1) * 100
                break

        transposed_pattern = numpy.transpose([[item for item in row] for row in pattern]).tolist()
        for row_idx in range(len(transposed_pattern) - 1):
            if is_middle_of_reflection(row_idx, transposed_pattern):
                result += (row_idx + 1)

    return result


def main():
    print(f'Advent of Code 2023 --- Day {DAY} --- Part {PART}')

    lines = data.splitlines()
    result = solve(lines)

    print(f'{str(result)}')


if __name__ == '__main__':
    start = timer()
    main()
    print(f"Completed in {timer() - start} sec")
