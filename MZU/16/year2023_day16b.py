import sys
from timeit import default_timer as timer

from aocd import data

DAY = '16'
PART = 'b'


def get_next_position(current_row, current_col, direction):
    if direction == 'right':
        return current_row, current_col + 1
    elif direction == 'down':
        return current_row + 1, current_col
    elif direction == 'left':
        return current_row, current_col - 1
    elif direction == 'up':
        return current_row - 1, current_col


def get_mirrored_direction(direction, mirror):
    if mirror == '/':
        if direction == 'right':
            return 'up'
        elif direction == 'down':
            return 'left'
        elif direction == 'left':
            return 'down'
        elif direction == 'up':
            return 'right'
    elif mirror == '\\':
        if direction == 'right':
            return 'down'
        elif direction == 'down':
            return 'right'
        elif direction == 'left':
            return 'up'
        elif direction == 'up':
            return 'left'


def get_splittered_directions(direction, splitter):
    if splitter == '-':
        if direction == 'right':
            return ['right']
        elif direction == 'down':
            return ['left', 'right']
        elif direction == 'left':
            return ['left']
        elif direction == 'up':
            return ['left', 'right']
    elif splitter == '|':
        if direction == 'right':
            return ['up', 'down']
        elif direction == 'down':
            return ['down']
        elif direction == 'left':
            return ['up', 'down']
        elif direction == 'up':
            return ['up']


def already_done_that(row_idx, col_idx, direction, log):
    return direction[0] in log[row_idx][col_idx]


def is_on_contraption(row_idx, col_idx, contraption):
    return 0 <= row_idx < len(contraption) and 0 <= col_idx < len(contraption[0])


def move_beam(current_row, current_col, direction, contraption, energized_tiles, log):
    if not is_on_contraption(current_row, current_col, contraption):
        return
    if already_done_that(current_row, current_col, direction, log):
        return

    energized_tiles[current_row][current_col] = '#'
    log[current_row][current_col].add(direction[0])
    tile = contraption[current_row][current_col]
    if tile == '.':
        next_row, next_col = get_next_position(current_row, current_col, direction)
        move_beam(next_row, next_col, direction, contraption, energized_tiles, log)
    elif tile in '/\\':
        next_direction = get_mirrored_direction(direction, tile)
        next_row, next_col = get_next_position(current_row, current_col, next_direction)
        move_beam(next_row, next_col, next_direction, contraption, energized_tiles, log)
    elif tile in '-|':
        next_directions = get_splittered_directions(direction, tile)
        for next_direction in next_directions:
            next_row, next_col = get_next_position(current_row, current_col, next_direction)
            move_beam(next_row, next_col, next_direction, contraption, energized_tiles, log)


def try_configuration(lines, start_row, start_col, start_direction):
    contraption = [[tile for tile in row] for row in lines]
    energized_tiles = [['.' for _ in row] for row in lines]
    log = [[set() for _ in row] for row in lines]
    move_beam(start_row, start_col, start_direction, contraption, energized_tiles, log)
    return sum([row.count('#') for row in energized_tiles])


def solve(lines):
    max_energized_tiles = 0
    for start_col in range(len(lines[0])):
        energized_tiles = try_configuration(lines, 0, start_col, 'down')
        max_energized_tiles = max(energized_tiles, max_energized_tiles)
        energized_tiles = try_configuration(lines, len(lines) - 1, start_col, 'up')
        max_energized_tiles = max(energized_tiles, max_energized_tiles)
    for start_row in range(len(lines)):
        energized_tiles = try_configuration(lines, start_row, 0, 'right')
        max_energized_tiles = max(energized_tiles, max_energized_tiles)
        energized_tiles = try_configuration(lines, start_row, len(lines[0]) - 1, 'left')
        max_energized_tiles = max(energized_tiles, max_energized_tiles)
    return max_energized_tiles


def main():
    print(f'Advent of Code 2023 --- Day {DAY} --- Part {PART}')

    sys.setrecursionlimit(10000)
    lines = data.splitlines()
    result = solve(lines)

    print(f'{str(result)}')


if __name__ == '__main__':
    start = timer()
    main()
    print(f"Completed in {timer() - start} sec")
