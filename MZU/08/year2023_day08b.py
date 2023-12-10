import math
import re
from timeit import default_timer as timer

from aocd import data

DAY = '08'
PART = 'b'


def solve(lines):
    instructions = lines[0]
    desert_map = {}
    for line in lines[2:]:
        location, next_left, next_right = re.findall('[A-Z0-9]+', line)
        desert_map[location] = [next_left, next_right]

    locations = list(filter(lambda key: key[2] == 'A', desert_map.keys()))
    steps = [0 for _ in range(len(locations))]

    for i in range(len(locations)):
        instruction_position = 0
        while locations[i][2] != 'Z':
            if instructions[instruction_position] == 'L':
                locations[i] = desert_map[locations[i]][0]
            else:
                locations[i] = desert_map[locations[i]][1]
            steps[i] = steps[i] + 1
            instruction_position = (instruction_position + 1) % len(instructions)

    return math.lcm(*steps)


def main():
    print(f'Advent of Code 2023 --- Day {DAY} --- Part {PART}')

    lines = data.splitlines()
    result = solve(lines)

    print(f'{str(result)}')


if __name__ == '__main__':
    start = timer()
    main()
    print(f"Completed in {timer() - start} sec")
