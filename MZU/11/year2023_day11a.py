from timeit import default_timer as timer

import numpy
from aocd import data

DAY = '11'
PART = 'a'


def expand_rows(galaxy_map):
    empty_rows = []
    for row_idx, row in enumerate(galaxy_map):
        if all(position == '.' for position in row):
            empty_rows.append(row_idx)

    empty_rows.reverse()
    for row_idx in empty_rows:
        galaxy_map.insert(row_idx, ['.' for _ in range(len(row))])


def solve(lines):
    galaxy_map = [[position for position in row] for row in lines]
    expand_rows(galaxy_map)
    galaxy_map = numpy.transpose(galaxy_map).tolist()
    expand_rows(galaxy_map)
    galaxy_map = numpy.transpose(galaxy_map).tolist()
    galaxy_positions = []
    for row_idx in range(len(galaxy_map)):
        for col_idx in range(len(galaxy_map[0])):
            if galaxy_map[row_idx][col_idx] == '#':
                galaxy_positions.append((row_idx, col_idx))
    sum_of_distances = 0
    for first_idx in range(len(galaxy_positions)):
        for second_idx in range(first_idx + 1, len(galaxy_positions), 1):
            sum_of_distances += (abs(galaxy_positions[second_idx][0] - galaxy_positions[first_idx][0])
                                 + abs(galaxy_positions[second_idx][1] - galaxy_positions[first_idx][1]))
    return sum_of_distances


def main():
    print(f'Advent of Code 2023 --- Day {DAY} --- Part {PART}')

    lines = data.splitlines()
    result = solve(lines)

    print(f'{str(result)}')


if __name__ == '__main__':
    start = timer()
    main()
    print(f"Completed in {timer() - start} sec")
