import re
from timeit import default_timer as timer

from aocd import data

DAY = '02'
PART = 'a'

NUMBER_OF_RED_CUBES = 12
NUMBER_OF_BLUE_CUBES = 14
NUMBER_OF_GREEN_CUBES = 13


def solve(lines):
    possible_game_ids = []

    for line in lines:
        game_id = re.findall(r'\d+', line)[0]
        reds = re.findall(r'\d+(?= red)', line)
        blues = re.findall(r'\d+(?= blue)', line)
        greens = re.findall(r'\d+(?= green)', line)

        if any(int(r) > NUMBER_OF_RED_CUBES for r in reds) \
                or any(int(b) > NUMBER_OF_BLUE_CUBES for b in blues) \
                or any(int(g) > NUMBER_OF_GREEN_CUBES for g in greens):
            continue

        possible_game_ids.append(int(game_id))
    return sum(possible_game_ids)


def main():
    print(f'Advent of Code 2023 --- Day {DAY} --- Part {PART}')

    lines = data.splitlines()
    result = solve(lines)

    print(f'{str(result)}')


if __name__ == '__main__':
    start = timer()
    main()
    print(f"Completed in {timer() - start} sec")
