from timeit import default_timer as timer

from aocd import data

DAY = '15'
PART = 'a'


def calculate_single_hash(current_hash, character):
    current_hash += ord(character)
    current_hash *= 17
    current_hash %= 256
    return current_hash


def calculate_hash(step):
    current_hash = 0
    for c in step:
        current_hash = calculate_single_hash(current_hash, c)
    return current_hash


def solve(lines):
    steps = lines[0].split(',')
    hash_numbers = [calculate_hash(step) for step in steps]
    return sum(hash_numbers)


def main():
    print(f'Advent of Code 2023 --- Day {DAY} --- Part {PART}')

    lines = data.splitlines()
    result = solve(lines)

    print(f'{str(result)}')


if __name__ == '__main__':
    start = timer()
    main()
    print(f"Completed in {timer() - start} sec")
