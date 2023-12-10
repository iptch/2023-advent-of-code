from timeit import default_timer as timer

from aocd import data

DAY = '10'
PART = 'a'


class HitTheGroundException(Exception):
    pass


def calculate_next_position(curr_row_idx, curr_col_idx, prev_row_idx, prev_col_idx, pipe_map):
    pipe = pipe_map[curr_row_idx][curr_col_idx]
    if pipe == '|':
        if prev_row_idx < curr_row_idx:
            return curr_row_idx + 1, curr_col_idx, curr_row_idx, curr_col_idx
        else:
            return curr_row_idx - 1, curr_col_idx, curr_row_idx, curr_col_idx
    elif pipe == '-':
        if prev_col_idx < curr_col_idx:
            return curr_row_idx, curr_col_idx + 1, curr_row_idx, curr_col_idx
        else:
            return curr_row_idx, curr_col_idx - 1, curr_row_idx, curr_col_idx
    elif pipe == 'L':
        if prev_row_idx < curr_row_idx:
            return curr_row_idx, curr_col_idx + 1, curr_row_idx, curr_col_idx
        else:
            return curr_row_idx - 1, curr_col_idx, curr_row_idx, curr_col_idx
    elif pipe == 'J':
        if prev_row_idx < curr_row_idx:
            return curr_row_idx, curr_col_idx - 1, curr_row_idx, curr_col_idx
        else:
            return curr_row_idx - 1, curr_col_idx, curr_row_idx, curr_col_idx
    elif pipe == '7':
        if prev_row_idx == curr_row_idx:
            return curr_row_idx + 1, curr_col_idx, curr_row_idx, curr_col_idx
        else:
            return curr_row_idx, curr_col_idx - 1, curr_row_idx, curr_col_idx
    elif pipe == 'F':
        if prev_row_idx == curr_row_idx:
            return curr_row_idx + 1, curr_col_idx, curr_row_idx, curr_col_idx
        else:
            return curr_row_idx, curr_col_idx + 1, curr_row_idx, curr_col_idx
    else:
        raise HitTheGroundException


def solve(lines):
    pipe_map = [[character for character in row] for row in lines]
    start_position = (0, 0)
    for row_idx, row in enumerate(pipe_map):
        for col_idx, position in enumerate(row):
            if position == 'S':
                start_position = (row_idx, col_idx)

    prev_row_idx, prev_col_idx = start_position
    curr_row_idx, curr_col_idx = prev_row_idx - 1, prev_col_idx  # start direction is hardcoded for my input!
    next_position = pipe_map[curr_row_idx][curr_col_idx]
    steps = 1
    while next_position != 'S':
        curr_row_idx, curr_col_idx, prev_row_idx, prev_col_idx = \
            calculate_next_position(curr_row_idx, curr_col_idx, prev_row_idx, prev_col_idx, pipe_map)
        next_position = pipe_map[curr_row_idx][curr_col_idx]
        steps = steps + 1

    return int(steps / 2)


def main():
    print(f'Advent of Code 2023 --- Day {DAY} --- Part {PART}')

    lines = data.splitlines()
    result = solve(lines)

    print(f'{str(result)}')


if __name__ == '__main__':
    start = timer()
    main()
    print(f"Completed in {timer() - start} sec")
