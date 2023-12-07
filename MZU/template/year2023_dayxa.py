from timeit import default_timer as timer

from aocd import data

DAY = 'x'
PART = 'a'


def solve(lines):
    result = 0
    return result


def main():
    print(f'Advent of Code 2023 --- Day {DAY} --- Part {PART}')

    lines = data.splitlines()
    result = solve(lines)

    print(f'{str(result)}')


if __name__ == '__main__':
    start = timer()
    main()
    print(f"Completed in {timer() - start} sec")
