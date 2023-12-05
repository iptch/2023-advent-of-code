from timeit import default_timer as timer

from aocd import data

DAY = '03'
PART = 'a'


def solve(lines):
    engine_schematic = [[value for value in row] for row in lines]
    part_numbers = []
    current_part_number = ''
    current_part_number_start_idx = None
    symbol_coordinates = []
    for row_idx in range(len(engine_schematic)):
        for col_idx in range(len(engine_schematic[0])):
            if not engine_schematic[row_idx][col_idx].isdigit() and engine_schematic[row_idx][col_idx] != '.':
                symbol_coordinates.append((col_idx, row_idx))

    for row_idx in range(len(engine_schematic)):
        for col_idx in range(len(engine_schematic[0])):
            if current_part_number and (
                    col_idx == 0 or not engine_schematic[row_idx][col_idx].isdigit()):
                part_end_row_idx = row_idx - 1 if col_idx == 0 else row_idx
                part_end_col_idx = col_idx - 1 if col_idx != 0 else len(engine_schematic[0]) - 1
                adjacent_coordinates = [(col, row) for row in range(part_end_row_idx - 1, part_end_row_idx + 2)
                                        for col in range(current_part_number_start_idx - 1, part_end_col_idx + 2)]
                if any(coordinate in symbol_coordinates for coordinate in adjacent_coordinates):
                    part_numbers.append(int(current_part_number))
                current_part_number = ''
                current_part_number_start_idx = None
            if engine_schematic[row_idx][col_idx].isdigit():
                current_part_number += engine_schematic[row_idx][col_idx]
                if current_part_number_start_idx is None:
                    current_part_number_start_idx = col_idx

    return sum(part_numbers)


def main():
    print(f'Advent of Code 2023 --- Day {DAY} --- Part {PART}')

    lines = data.splitlines()
    result = solve(lines)

    print(f'{str(result)}')


if __name__ == '__main__':
    start = timer()
    main()
    print(f"Completed in {timer() - start} sec")
