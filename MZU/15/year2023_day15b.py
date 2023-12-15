import re
from timeit import default_timer as timer

from aocd import data

DAY = '15'
PART = 'b'


def calculate_single_hash(current_hash, character):
    current_hash += ord(character)
    current_hash *= 17
    current_hash %= 256
    return current_hash


def calculate_hash(label):
    current_hash = 0
    for c in label:
        current_hash = calculate_single_hash(current_hash, c)
    return current_hash


def solve(lines):
    steps = lines[0].split(',')
    boxes = [{} for _ in range(256)]
    for step in steps:
        label = re.findall(r'[a-z]+', step)[0]
        box_nr = calculate_hash(label)
        operation = re.findall(r'[-=]', step)[0]
        if operation == '=':
            focal_length = int(re.findall(r'[0-9]', step)[0])
            boxes[box_nr][label] = focal_length
        else:
            boxes[box_nr].pop(label, None)

    focal_powers = []
    for box_idx, box in enumerate(boxes):
        for lens_idx, lens in enumerate(box.items()):
            _, focal_length = lens
            focal_powers.append((box_idx + 1) * (lens_idx + 1) * focal_length)
    return sum(focal_powers)


def main():
    print(f'Advent of Code 2023 --- Day {DAY} --- Part {PART}')

    lines = data.splitlines()
    result = solve(lines)

    print(f'{str(result)}')


if __name__ == '__main__':
    start = timer()
    main()
    print(f"Completed in {timer() - start} sec")
