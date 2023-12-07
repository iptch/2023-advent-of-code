import math
import re
from timeit import default_timer as timer

from aocd import data

DAY = '06'
PART = 'a'


def solve(lines):
    times = [int(time) for time in re.findall(r'\d+', lines[0])]
    record_distances = [int(distance) for distance in re.findall(r'\d+', lines[1])]

    possibilities_to_win = []
    for time, distance in zip(times, record_distances):
        wins = 0
        for ms in range(time):
            possible_distance = ms * (time - ms)
            if possible_distance > distance:
                wins = wins + 1
        possibilities_to_win.append(wins)

    return math.prod(possibilities_to_win)


def main():
    print(f'Advent of Code 2023 --- Day {DAY} --- Part {PART}')

    lines = data.splitlines()
    result = solve(lines)

    print(f'{str(result)}')


if __name__ == '__main__':
    start = timer()
    main()
    print(f"Completed in {timer() - start} sec")
