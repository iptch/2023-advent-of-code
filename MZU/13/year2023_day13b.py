import copy
from timeit import default_timer as timer

import numpy
from aocd import data

DAY = '13'
PART = 'b'


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


def fixed_smudge(original):
    if original == '.':
        return '#'
    else:
        return '.'


def solve(lines):
    patterns = read_patterns(lines)
    result = 0

    old_reflection = {}
    for idx, pattern in enumerate(patterns):
        for row_idx in range(len(pattern) - 1):
            if is_middle_of_reflection(row_idx, pattern):
                old_reflection[idx] = ('row', row_idx)
                break

        transposed_pattern = numpy.transpose([[item for item in row] for row in pattern]).tolist()
        for row_idx in range(len(transposed_pattern) - 1):
            if is_middle_of_reflection(row_idx, transposed_pattern):
                old_reflection[idx] = ('col', row_idx)
                break

    for idx, pattern in enumerate(patterns):
        result_found = False
        for row_idx in range(len(pattern)):
            for col_idx in range(len(pattern[0])):
                # fix the smudge
                pattern_copy = copy.deepcopy(pattern)
                if col_idx + 1 != len(pattern_copy[0]):
                    pattern_copy[row_idx] = pattern_copy[row_idx][:col_idx] + fixed_smudge(pattern_copy[row_idx][col_idx]) + pattern_copy[row_idx][col_idx + 1:]
                else:
                    pattern_copy[row_idx] = pattern_copy[row_idx][:col_idx] + fixed_smudge(pattern_copy[row_idx][col_idx])

                # try to find reflection horizontally
                for i in range(len(pattern_copy) - 1):
                    if is_middle_of_reflection(i, pattern_copy):
                        if old_reflection[idx][0] != 'row' or (old_reflection[idx][0] == 'row' and old_reflection[idx][1] != i):
                            result += (i + 1) * 100
                            result_found = True
                            break

                if not result_found:
                    # try to find reflection vertically
                    transposed_pattern = numpy.transpose([[item for item in row] for row in pattern_copy]).tolist()
                    for i in range(len(transposed_pattern) - 1):
                        if is_middle_of_reflection(i, transposed_pattern):
                            if old_reflection[idx][0] != 'col' or (old_reflection[idx][0] == 'col' and old_reflection[idx][1] != i):
                                result += (i + 1)
                                result_found = True
                                break

                if result_found:
                    break

            if result_found:
                break

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
