# aoc_template.py

import pathlib
import sys
import re

def get_hash(str):
    count = 0

    for character in str:
        count = (count + ord(character)) * 17 % 256

    return count

def parse(puzzle_input):
    """Parse input."""

    return puzzle_input.split(",")

def part1(data):
    """Solve part 1."""

    return sum([get_hash(step) for step in data])

def part2(data):
    """Solve part 2."""
    
    hashmap = [[] for _ in range(256)]

    for step in data:
        label = re.search(r"[a-z]+", step).group()
        box = hashmap[get_hash(label)]
        given_labels = [lens[0] for lens in box]
        i = given_labels.index(label) if label in given_labels else -1

        if step[len(label)] == "=":
            focal_length = int(step[-1])

            if i > -1:
                box[i] = (label ,focal_length)
            else:
                box.append((label, focal_length))
        elif i > -1:
            box.pop(i)

    count = 0

    for i, box in enumerate(hashmap):
        for j, lens in enumerate(box):
            count += (i + 1) * (j + 1) * lens[1]

    return count

def solve(puzzle_input):
    """Solve the puzzle for the given input."""
    data = parse(puzzle_input)
    solution1 = part1(data)
    solution2 = part2(data)

    return solution1, solution2

if __name__ == "__main__":
    for path in sys.argv[1:]:
        print(f"{path}:")
        puzzle_input = pathlib.Path(path).read_text().strip()
        solutions = solve(puzzle_input)
        print("\n".join(str(solution) for solution in solutions))