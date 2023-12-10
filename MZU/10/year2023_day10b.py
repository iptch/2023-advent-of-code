import copy
from timeit import default_timer as timer

from aocd import data

DAY = '10'
PART = 'b'


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


def calculate_loop(pipe_map, start_position):
    prev_row_idx, prev_col_idx = start_position
    # direction to go is hardcoded to my input (by manually inferring direction from context around S)!
    curr_row_idx, curr_col_idx = prev_row_idx + 1, prev_col_idx
    next_position = pipe_map[curr_row_idx][curr_col_idx]
    loop_list = [start_position]
    while next_position != 'S':
        loop_list.append((curr_row_idx, curr_col_idx))
        curr_row_idx, curr_col_idx, prev_row_idx, prev_col_idx = \
            calculate_next_position(curr_row_idx, curr_col_idx, prev_row_idx, prev_col_idx, pipe_map)
        next_position = pipe_map[curr_row_idx][curr_col_idx]

    # mark the loop in a loop_map for quick lookup
    loop_map = copy.deepcopy(pipe_map)
    for row_idx, col_idx in loop_list:
        loop_map[row_idx][col_idx] = 'o'

    return loop_list, loop_map


def mark_inside(row_idx, col_idx, pipe_map, loop_map):
    if loop_map[row_idx][col_idx] != 'o':  # if not on loop
        try:
            pipe_map[row_idx][col_idx] = 'X'  # mark inside
        except IndexError:
            pass


def mark_inside_loop(loop_list, loop_map, pipe_map):
    for i in range(len(loop_list) - 1):
        pipe = pipe_map[loop_list[i][0]][loop_list[i][1]]
        if pipe == '|':
            if loop_list[i + 1][0] > loop_list[i][0]:  # going south
                mark_inside(loop_list[i][0], loop_list[i][1] - 1, pipe_map, loop_map)  # mark west
            else:  # going north
                mark_inside(loop_list[i][0], loop_list[i][1] + 1, pipe_map, loop_map)  # mark east
        elif pipe == '-':
            if loop_list[i + 1][1] > loop_list[i][1]:  # going east
                mark_inside(loop_list[i][0] + 1, loop_list[i][1], pipe_map, loop_map)  # mark south
            else:  # going west
                mark_inside(loop_list[i][0] - 1, loop_list[i][1], pipe_map, loop_map)  # mark north
        elif pipe == 'L':
            if loop_list[i + 1][1] > loop_list[i][1]:  # going east
                mark_inside(loop_list[i][0], loop_list[i][1] - 1, pipe_map, loop_map)  # mark west
                mark_inside(loop_list[i][0] + 1, loop_list[i][1], pipe_map, loop_map)  # mark south
        elif pipe == 'J':
            if loop_list[i + 1][0] < loop_list[i][0]:  # going north
                mark_inside(loop_list[i][0] + 1, loop_list[i][1], pipe_map, loop_map)  # mark south
                mark_inside(loop_list[i][0], loop_list[i][1] + 1, pipe_map, loop_map)  # mark east
        elif pipe == '7':
            if loop_list[i + 1][1] < loop_list[i][1]:  # going west
                mark_inside(loop_list[i][0], loop_list[i][1] + 1, pipe_map, loop_map)  # mark east
                mark_inside(loop_list[i][0] - 1, loop_list[i][1], pipe_map, loop_map)  # mark north
        elif pipe == 'F':
            if loop_list[i + 1][0] > loop_list[i][0]:  # going south
                mark_inside(loop_list[i][0], loop_list[i][1] - 1, pipe_map, loop_map)  # mark west
                mark_inside(loop_list[i][0] - 1, loop_list[i][1], pipe_map, loop_map)  # mark north


def fill_in_loop(loop_list, pipe_map):
    for row_idx in range(len(pipe_map)):
        for col_idx in range(1, len(pipe_map[0]), 1):
            if (row_idx, col_idx) not in loop_list and pipe_map[row_idx][col_idx - 1] == 'X':
                pipe_map[row_idx][col_idx] = 'X'


def visualize(loop_map, pipe_map):
    for row_idx in range(len(pipe_map)):
        for col_idx in range(len(pipe_map[0])):
            if loop_map[row_idx][col_idx] == 'o':
                pipe_map[row_idx][col_idx] = 'o'
    for row in pipe_map:
        print(''.join(row))


def solve(lines, replacement_of_s):
    pipe_map = [[pipe for pipe in row] for row in lines]
    start_position = (0, 0)
    for row_idx, row in enumerate(pipe_map):
        for col_idx, position in enumerate(row):
            if position == 'S':
                start_position = (row_idx, col_idx)

    loop_list, loop_map = calculate_loop(pipe_map, start_position)
    pipe_map[start_position[0]][start_position[1]] = str(replacement_of_s)
    mark_inside_loop(loop_list, loop_map, pipe_map)
    fill_in_loop(loop_list, pipe_map)
    visualize(loop_map, pipe_map)

    return [position for row in pipe_map for position in row].count('X')


def main():
    print(f'Advent of Code 2023 --- Day {DAY} --- Part {PART}')

    lines = data.splitlines()
    result = solve(lines, 7)  # needs to match my input!

    print(f'{str(result)}')


if __name__ == '__main__':
    start = timer()
    main()
    print(f"Completed in {timer() - start} sec")
