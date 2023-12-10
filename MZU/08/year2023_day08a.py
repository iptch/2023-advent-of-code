import re
from timeit import default_timer as timer

from aocd import data

DAY = '08'
PART = 'a'


def solve(lines):
    instructions = lines[0]
    desert_map = {}
    for line in lines[2:]:
        location, next_left, next_right = re.findall('[A-Z]+', line)
        desert_map[location] = [next_left, next_right]

    location = 'AAA'
    instruction_position = 0
    steps = 0
    while location != 'ZZZ':
        if instructions[instruction_position] == 'L':
            location = desert_map[location][0]
        else:
            location = desert_map[location][1]
        instruction_position = (instruction_position + 1) % len(instructions)
        steps = steps + 1
    return steps


def main():
    print(f'Advent of Code 2023 --- Day {DAY} --- Part {PART}')

    lines = data.splitlines()
    result = solve(lines)

    print(f'{str(result)}')


if __name__ == '__main__':
    start = timer()
    main()
    print(f"Completed in {timer() - start} sec")
