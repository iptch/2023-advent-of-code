import re
from timeit import default_timer as timer

from aocd import data

DAY = '02'
PART = 'b'


def solve(lines):
    power_of_minimal_set_of_cubes = []

    for line in lines:
        reds = [int(r) for r in re.findall(r'\d+(?= red)', line)]
        blues = [int(b) for b in re.findall(r'\d+(?= blue)', line)]
        greens = [int(g) for g in re.findall(r'\d+(?= green)', line)]

        power_of_minimal_set_of_cubes.append(max(reds) * max(blues) * max(greens))
    return sum(power_of_minimal_set_of_cubes)


def main():
    print(f'Advent of Code 2023 --- Day {DAY} --- Part {PART}')

    lines = data.splitlines()
    result = solve(lines)

    print(f'{str(result)}')


if __name__ == '__main__':
    start = timer()
    main()
    print(f"Completed in {timer() - start} sec")
