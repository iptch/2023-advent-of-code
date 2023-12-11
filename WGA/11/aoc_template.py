# aoc_template.py

import pathlib
import sys

def get_y_expansion_pts(image):
    y_expansion_pts = []

    for i, line in enumerate(image):
        if line.count(".") == len(line):
            y_expansion_pts.append(i)

    return y_expansion_pts

def get_x_expansion_pts(image):
    x_expansion_pts = []

    for i in range(0, len(image[0])):
        col = [x[i] for x in image]

        if col.count(".") == len(col):
            x_expansion_pts.append(i)

    return x_expansion_pts

def get_galaxies(image):
    galaxies = []
    
    for i, line in enumerate(image):
        for j, item in enumerate(line):
            if item == "#":
                galaxies.append((i, j))

    return galaxies

def get_galaxy_pairs(galaxies):
    pairs = []

    for i, galaxy_1 in enumerate(galaxies):
        if i + 1 < len(galaxies):
            for galaxy_2 in galaxies[i + 1:]:
                pairs.append([galaxy_1, galaxy_2])

    return pairs

def get_shortest_dist(galaxy_1, galaxy_2, y_expansion_pts, x_expansion_pts, factor):
    x = [x for x in x_expansion_pts if x in range(galaxy_1[1] + 1, galaxy_2[1]) or x in range(galaxy_2[1] + 1, galaxy_1[1])]
    y = [y for y in y_expansion_pts if y in range(galaxy_1[0] + 1, galaxy_2[0]) or y in range(galaxy_2[0] + 1, galaxy_2[0])]
    
    return abs(galaxy_1[0] - galaxy_2[0]) + abs(galaxy_1[1] - galaxy_2[1]) + (factor - 1) * (len(x) + len(y))

def parse(puzzle_input):
    """Parse input."""

    return [list(line) for line in puzzle_input.splitlines()]

def part1(data):
    """Solve part 1."""

    galaxies = get_galaxies(data)
    y_expansion_pts = get_y_expansion_pts(data)
    x_expansion_pts = get_x_expansion_pts(data)
    pairs = get_galaxy_pairs(galaxies)

    return sum([get_shortest_dist(pair[0], pair[1], y_expansion_pts, x_expansion_pts, 2) for pair in pairs])

def part2(data):
    """Solve part 2."""

    galaxies = get_galaxies(data)
    y_expansion_pts = get_y_expansion_pts(data)
    x_expansion_pts = get_x_expansion_pts(data)
    pairs = get_galaxy_pairs(galaxies)

    return sum([get_shortest_dist(pair[0], pair[1], y_expansion_pts, x_expansion_pts, 1000000) for pair in pairs])

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