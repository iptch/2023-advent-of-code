import re
from timeit import default_timer as timer

from aocd import data

DAY = '03'
PART = 'b'


def extract_sub_schematic(row_idx, col_idx, engine_schematic, size):
    sub_schematic = []
    for sub_row_idx in range(row_idx - 1, row_idx + 2):
        line = ''
        for sub_col_idx in range(col_idx - size, col_idx + size + 1):
            try:
                line += engine_schematic[sub_row_idx][sub_col_idx]
            except IndexError:
                pass
        sub_schematic.append(line)
    return sub_schematic


def extend_part_numbers_of_sub_schematic(sub_schematic, part_numbers, size):
    if size >= 1:
        for line in sub_schematic:
            part_numbers.extend(re.findall(r'\d{' + str(size) + '}', line))
        sub_schematic = [re.sub(r'\d{' + str(size) + '}', '...', line) for line in sub_schematic]
        extend_part_numbers_of_sub_schematic([line[1:-1] for line in sub_schematic], part_numbers, size - 1)


def solve(lines):
    engine_schematic = [[value for value in row] for row in lines]
    gear_ratios = []

    for row_idx in range(len(engine_schematic)):
        for col_idx in range(len(engine_schematic[0])):
            if engine_schematic[row_idx][col_idx] == '*':
                part_numbers = []
                sub_schematic = extract_sub_schematic(row_idx, col_idx, engine_schematic, 3)
                extend_part_numbers_of_sub_schematic(sub_schematic, part_numbers, 3)

                if len(part_numbers) == 2:
                    gear_ratios.append(int(part_numbers[0]) * int(part_numbers[1]))

    return sum(gear_ratios)


def main():
    print(f'Advent of Code 2023 --- Day {DAY} --- Part {PART}')

    lines = data.splitlines()
    result = solve(lines)

    print(f'{str(result)}')


if __name__ == '__main__':
    start = timer()
    main()
    print(f"Completed in {timer() - start} sec")
