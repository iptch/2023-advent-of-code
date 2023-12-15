import copy
from timeit import default_timer as timer

from aocd import data

DAY = '14'
PART = 'b'

CYCLES = 1000000000


def tilt_north(dish_map):
    still_moving = True
    while still_moving:
        still_moving = False
        for row_idx in range(len(dish_map) - 1):
            for col_idx in range(len(dish_map)):
                if dish_map[row_idx][col_idx] == '.' and dish_map[row_idx + 1][col_idx] == 'O':
                    dish_map[row_idx][col_idx] = 'O'
                    dish_map[row_idx + 1][col_idx] = '.'
                    still_moving = True


def tilt_west(dish_map):
    still_moving = True
    while still_moving:
        still_moving = False
        for row_idx in range(len(dish_map)):
            for col_idx in range(len(dish_map) - 1):
                if dish_map[row_idx][col_idx] == '.' and dish_map[row_idx][col_idx + 1] == 'O':
                    dish_map[row_idx][col_idx] = 'O'
                    dish_map[row_idx][col_idx + 1] = '.'
                    still_moving = True


def tilt_south(dish_map):
    still_moving = True
    while still_moving:
        still_moving = False
        for row_idx in range(len(dish_map) - 1, 0, -1):
            for col_idx in range(len(dish_map) - 1, -1, -1):
                if dish_map[row_idx][col_idx] == '.' and dish_map[row_idx - 1][col_idx] == 'O':
                    dish_map[row_idx][col_idx] = 'O'
                    dish_map[row_idx - 1][col_idx] = '.'
                    still_moving = True


def tilt_east(dish_map):
    still_moving = True
    while still_moving:
        still_moving = False
        for row_idx in range(len(dish_map) - 1, -1, -1):
            for col_idx in range(len(dish_map) - 1, 0, -1):
                if dish_map[row_idx][col_idx] == '.' and dish_map[row_idx][col_idx - 1] == 'O':
                    dish_map[row_idx][col_idx] = 'O'
                    dish_map[row_idx][col_idx - 1] = '.'
                    still_moving = True


def run_cycles(n, dish_map):
    for i in range(n):
        tilt_north(dish_map)
        tilt_west(dish_map)
        tilt_south(dish_map)
        tilt_east(dish_map)


def solve(lines):
    dish_map = [[position for position in row] for row in lines]
    run_cycles(200, dish_map)
    print('starting to find repetition counter now')
    comparison_dish_map = copy.deepcopy(dish_map)
    repetition_counter = 1
    run_cycles(1, dish_map)
    while dish_map != comparison_dish_map:
        run_cycles(1, dish_map)
        repetition_counter += 1
        print(repetition_counter)

    cycles_left = (CYCLES - 200) % repetition_counter
    run_cycles(cycles_left, dish_map)
    for row in dish_map:
        print(''.join(row))
    print(' ')

    total_load = 0
    for row_idx in range(len(dish_map)):
        for col_idx in range(len(dish_map)):
            if dish_map[row_idx][col_idx] == 'O':
                total_load += len(dish_map) - row_idx

    return total_load


def main():
    print(f'Advent of Code 2023 --- Day {DAY} --- Part {PART}')

    lines = data.splitlines()
    result = solve(lines)

    print(f'{str(result)}')


if __name__ == '__main__':
    start = timer()
    main()
    print(f"Completed in {timer() - start} sec")
