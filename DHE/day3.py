import numpy as np

INPUT = """467..114..
...*......
..35..633.
......#...
617*......
.....+.58.
..592.....
......755.
...$.*....
.664.598.."""


def parse_grid(input):
    return np.asarray([list(line) for line in input.split('\n')])


def find_gear_candidates(grid):
    candidates = []

    for i in range(grid.shape[0]):
        for j in range(grid.shape[1]):
            if '*' == grid[i, j]:
                candidates.append((i, j))

    return candidates


def find_number_starts(grid):
    number_starts = []

    for i in range(grid.shape[0]):
        prev_is_number = False

        for j in range(grid.shape[1]):
            if grid[i, j].isnumeric():
                if not prev_is_number:
                    number_starts.append((i, j))
                    prev_is_number = True
            else:
                prev_is_number = False

    return number_starts


def find_number_starting_at(grid, number_start):
    number = []
    for c in grid[number_start[0], number_start[1]:]:
        if c.isnumeric():
            number.append(int(c))
        else:
            break
    return number


def has_surrounding_symbol(grid, number_start):
    number_len = len(find_number_starting_at(grid, number_start))

    start_row = max(number_start[0]-1, 0)
    end_row = min(number_start[0]+2, grid.shape[0]+1)
    start_col = max(number_start[1]-1, 0)
    end_col = min(number_start[1]+number_len+2, grid.shape[1]+1)
    sub_grid = grid[start_row:end_row, start_col:end_col]
    # print(sub_grid)

    for i in range(sub_grid.shape[0]):
        for j in range(sub_grid.shape[1]):
            c = sub_grid[i, j]
            if not c.isnumeric() and c != '.':
                return True
    return False


def has_two_surrounding_numbers(grid, pos):
    number_len = len(find_number_starting_at(grid, pos))

    start_row = max(pos[0]-1, 0)
    end_row = min(pos[0]+2, grid.shape[0]+1)
    start_col = max(pos[1]-1, 0)
    end_col = min(pos[1]+number_len+2, grid.shape[1]+1)
    sub_grid = grid[start_row:end_row, start_col:end_col]
    # print(sub_grid)

    surrounding_numbers = 0

    for i in range(sub_grid.shape[0]):
        prev_is_number = False
        for j in range(sub_grid.shape[1]):
            c = sub_grid[i, j]
            if c.isnumeric():
                if not prev_is_number:
                    surrounding_numbers += 1
                    prev_is_number = True
            else:
                prev_is_number = False

    # print(surrounding_numbers)
    return 2 == surrounding_numbers


def get_numbers_with_surrounding_symbols(grid):
    numbers = []
    number_starts = find_number_starts(grid)
    # [print(has_surrounding_symbol(grid, number_start), '\n') for number_start in number_starts]

    for number_start in number_starts:
        if has_surrounding_symbol(grid, number_start):
            number_list = find_number_starting_at(grid, number_start)
            number = 0
            for i, digit in enumerate(number_list[::-1]):
                number += digit * 10**i
            numbers.append(number)
    return numbers


def is_adjacent_to_gear(grid, number_start, gear):
    number_len = len(find_number_starting_at(grid, number_start))

    start_row = max(number_start[0]-1, 0)
    end_row = min(number_start[0]+2, grid.shape[0]+1)
    start_col = max(number_start[1]-1, 0)
    end_col = min(number_start[1]+number_len+1, grid.shape[1]+1)
    sub_grid = grid[start_row:end_row, start_col:end_col]
    # print(sub_grid)

    for i in range(sub_grid.shape[0]):
        for j in range(sub_grid.shape[1]):
            if (i+start_row, j+start_col) == gear:
                return True
    return False


def get_numbers_adjacent_to_gear(grid, number_starts, gear):
    numbers = []
    # [print(has_surrounding_symbol(grid, number_start), '\n') for number_start in number_starts]

    for number_start in number_starts:
        if is_adjacent_to_gear(grid, number_start, gear):
            number_list = find_number_starting_at(grid, number_start)
            number = 0
            for i, digit in enumerate(number_list[::-1]):
                number += digit * 10**i
            numbers.append(number)
    return numbers


def get_gears(grid):
    return [candidate for candidate in find_gear_candidates(grid) if has_two_surrounding_numbers(grid, candidate)]


if __name__ == '__main__':
    input_grid = parse_grid(INPUT)

    gears = get_gears(input_grid)
    number_starts = find_number_starts(input_grid)

    numbers_adjacent_to_gears = [get_numbers_adjacent_to_gear(input_grid, number_starts, gear) for gear in gears]

    # --- part 1 ---
    print(sum(get_numbers_with_surrounding_symbols(input_grid)))

    # --- part 2 ---
    print(sum([pair[0]*pair[1] for pair in numbers_adjacent_to_gears]))
