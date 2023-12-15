import re
from timeit import default_timer as timer

from aocd import data

DAY = '12'
PART = 'a'


def arrangement_is_valid(arrangement, template):
    return all(
        arrangement[idx] == '#' and template[idx] in '#?' or arrangement[idx] == '.' and template[idx] in '.?' for idx
        in range(len(arrangement)))


def calculate_possible_arrangements(spring_groups, template, possible_arrangements, prefix):
    if len(spring_groups) == 1:
        for initial_space_length in range(0, len(template) - spring_groups[0] + 1, 1):
            arrangement = '.' * initial_space_length + spring_groups[0] * '#' \
                          + (len(template) - spring_groups[0] - initial_space_length) * '.'
            if arrangement_is_valid(arrangement, template):
                possible_arrangements.add(prefix + arrangement)
    else:
        max_first_part_length = len(template) - sum(spring_groups[1:]) - (len(spring_groups) - 2)
        for first_part_length in range(spring_groups[0] + 1, max_first_part_length + 1):
            for initial_space_length in range(0, first_part_length - spring_groups[0] + 1, 1):
                first_part_of_arrangement = '.' * initial_space_length + spring_groups[0] * '#' \
                                            + (first_part_length - spring_groups[0] - initial_space_length) * '.'
                if first_part_of_arrangement.endswith('.') and arrangement_is_valid(first_part_of_arrangement, template):
                    calculate_possible_arrangements(spring_groups[1:], template[len(first_part_of_arrangement):], possible_arrangements, prefix + first_part_of_arrangement)

    return possible_arrangements


def solve(lines):
    possible_arrangements = 0
    for line in lines:
        template = re.findall(r'[.?#]+', line)[0]
        spring_groups = [int(group_length) for group_length in re.findall(r'[\d]+', line)]
        possible_arrangements += len(calculate_possible_arrangements(spring_groups, template, set(), ''))

    return possible_arrangements


def main():
    print(f'Advent of Code 2023 --- Day {DAY} --- Part {PART}')

    lines = data.splitlines()
    result = solve(lines)

    print(f'{str(result)}')


if __name__ == '__main__':
    start = timer()
    main()
    print(f"Completed in {timer() - start} sec")
