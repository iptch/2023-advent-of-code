import functools
import re
from timeit import default_timer as timer

from aocd import data

DAY = '12'
PART = 'b'


@functools.cache
def count_possible_arrangements(spring_groups, template):
    if len(spring_groups) == 0 and '#' not in template:
        return 1  # finished with valid end
    elif len(spring_groups) == 0 or len(template) < spring_groups[0] or sum(spring_groups) + (len(spring_groups) - 1) > len(template):
        return 0  # invalid paths
    elif len(spring_groups) == 1 and len(template) == spring_groups[0]:
        if all(l in '#?' for l in template):
            return 1  # it matches exactly once, and we are at the end now
        else:
            return 0  # it does not match and we are done here
    elif template[0] == '.':
        return count_possible_arrangements(spring_groups, template[1:])  # move on to the next position
    elif template[0] == '#':
        if all(l in '#?' for l in template[0:spring_groups[0]]) and template[spring_groups[0]] in '.?':
            return count_possible_arrangements(spring_groups[1:], template[spring_groups[0] + 1:])  # this group matches and I continue with the next
        else:
            return 0  # ended up in an invalid path
    elif template[0] == '?':
        if all(l in '#?' for l in template[:spring_groups[0]]) and template[spring_groups[0]] in '.?':
            # we can match it and also not match it -> continue with both possibilities
            return count_possible_arrangements(spring_groups[1:], template[spring_groups[0] + 1:]) + count_possible_arrangements(spring_groups, template[1:])
        else:
            # we can not match now and continue with the next position
            return count_possible_arrangements(spring_groups, template[1:])


def solve(lines):
    possible_arrangements = 0
    for line in lines:
        template = re.findall(r'[.?#]+', line)[0]
        spring_groups = [int(group_length) for group_length in re.findall(r'[\d]+', line)] * 5
        unfolded_template = (template + '?') * 4 + template
        possible_arrangements += count_possible_arrangements(tuple(spring_groups), unfolded_template)

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
