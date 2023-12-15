from timeit import default_timer as timer

import numpy
from aocd import data

DAY = '11'
PART = 'b'


def get_empty_row_and_cols(galaxy_map):
    empty_rows = []
    for row_idx, row in enumerate(galaxy_map):
        if all(position == '.' for position in row):
            empty_rows.append(row_idx)
    galaxy_map = numpy.transpose(galaxy_map).tolist()
    empty_cols = []
    for row_idx, row in enumerate(galaxy_map):
        if all(position == '.' for position in row):
            empty_cols.append(row_idx)
    return empty_cols, empty_rows


def get_galaxy_positions(galaxy_map):
    galaxy_positions = []
    for row_idx in range(len(galaxy_map)):
        for col_idx in range(len(galaxy_map[0])):
            if galaxy_map[row_idx][col_idx] == '#':
                galaxy_positions.append((row_idx, col_idx))

    return galaxy_positions


def solve(lines, expansion_factor):
    galaxy_map = [[position for position in row] for row in lines]
    empty_cols, empty_rows = get_empty_row_and_cols(galaxy_map)
    galaxy_positions = get_galaxy_positions(galaxy_map)

    sum_of_distances = 0
    for first_idx in range(len(galaxy_positions)):
        for second_idx in range(first_idx + 1, len(galaxy_positions), 1):
            sum_of_distances += (abs(galaxy_positions[second_idx][0] - galaxy_positions[first_idx][0])
                                 + abs(galaxy_positions[second_idx][1] - galaxy_positions[first_idx][1]))

            for empty_row_idx in empty_rows:
                if min([galaxy_positions[second_idx][0], galaxy_positions[first_idx][0]]) < empty_row_idx \
                        < max([galaxy_positions[second_idx][0], galaxy_positions[first_idx][0]]):
                    sum_of_distances += expansion_factor - 1

            for empty_col_idx in empty_cols:
                if min([galaxy_positions[second_idx][1], galaxy_positions[first_idx][1]]) < empty_col_idx \
                        < max([galaxy_positions[second_idx][1], galaxy_positions[first_idx][1]]):
                    sum_of_distances += expansion_factor - 1

    return sum_of_distances


def main():
    print(f'Advent of Code 2023 --- Day {DAY} --- Part {PART}')

    lines = data.splitlines()
    result = solve(lines, 1000000)

    print(f'{str(result)}')


if __name__ == '__main__':
    start = timer()
    main()
    print(f"Completed in {timer() - start} sec")
