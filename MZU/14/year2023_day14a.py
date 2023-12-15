from timeit import default_timer as timer

from aocd import data

DAY = '14'
PART = 'a'


def solve(lines):
    dish_map = [[position for position in row] for row in lines]
    still_moving = True
    while still_moving:
        still_moving = False
        for row_idx in range(len(dish_map) - 1):
            for col_idx in range(len(dish_map)):
                if dish_map[row_idx][col_idx] == '.' and dish_map[row_idx + 1][col_idx] == 'O':
                    dish_map[row_idx][col_idx] = 'O'
                    dish_map[row_idx + 1][col_idx] = '.'
                    still_moving = True

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
