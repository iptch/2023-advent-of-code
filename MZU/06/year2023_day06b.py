import re
from timeit import default_timer as timer

from aocd import data

DAY = '06'
PART = 'b'


def solve(lines):
    time = [int(time) for time in re.findall(r'\d+', lines[0].replace(' ', ''))][0]
    record_distance = [int(distance) for distance in re.findall(r'\d+', lines[1].replace(' ', ''))][0]

    wins = 0
    for ms in range(time):
        possible_distance = ms * (time - ms)
        if possible_distance > record_distance:
            wins = wins + 1

    return wins


def main():
    print(f'Advent of Code 2023 --- Day {DAY} --- Part {PART}')

    lines = data.splitlines()
    result = solve(lines)

    print(f'{str(result)}')


if __name__ == '__main__':
    start = timer()
    main()
    print(f"Completed in {timer() - start} sec")
