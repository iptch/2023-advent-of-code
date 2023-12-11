# aoc_template.py

import pathlib
import sys
import copy

def expand_image(image):
    expanded_image = copy.deepcopy(image)

    y_offset = x_offset = 0

    for i, line in enumerate(image):
        if line.count(".") == len(line):
            expanded_image.insert(i + y_offset, line)
            y_offset += 1

    for i in range(0, len(image[0])):
        col = [x[i] for x in image]

        if col.count(".") == len(col):
            for line in expanded_image:
                line.insert(i + x_offset, ".")

            x_offset += 1

    return expanded_image

def get_galaxies(image):
    galaxies = []
    
    for i, line in enumerate(image):
        for j, item in enumerate(line):
            if item == "#":
                galaxies.append((i, j))

    return galaxies

def get_galaxy_pairs(galaxies):
    galaxy_pairs = []

    for i, galaxy_1 in enumerate(galaxies):
        if i + 1 < len(galaxies):
            for galaxy_2 in galaxies[i + 1:]:
                galaxy_pairs.append([galaxy_1, galaxy_2])

    return galaxy_pairs

def get_shortest_dist(galaxy_1, galaxy_2):
    return abs(galaxy_1[0] - galaxy_2[0]) + abs(galaxy_1[1] - galaxy_2[1])

def parse(puzzle_input):
    """Parse input."""

    return [list(line) for line in puzzle_input.splitlines()]

def part1(data):
    """Solve part 1."""

    expanded_image = expand_image(data)
    galaxies = get_galaxies(expanded_image)
    galaxy_pairs = get_galaxy_pairs(galaxies)

    return sum([get_shortest_dist(pair[0], pair[1]) for pair in galaxy_pairs])

def part2(data):
    """Solve part 2."""

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