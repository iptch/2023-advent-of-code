# aoc_template.py

import pathlib
import sys
import copy

class Direction:
    NORTH = (-1, 0)
    WEST = (0, -1)
    SOUTH = (1, 0)
    EAST = (0, 1)

def add_tupels(a, b):
    return (a[0] + b[0], a[1] + b[1])

def get_arrow(dir):
    if dir == Direction.NORTH:
        return "^"
    if dir == Direction.WEST:
        return "<"
    if dir == Direction.SOUTH:
        return "v"
    if dir == Direction.EAST:
        return ">"

def move(pos, dir, tiles, energized):
    y, x = pos

    if y < 0 or y > len(tiles) - 1 or x < 0 or x > len(tiles[0]) - 1:
        return energized
    
    energized[y][x] = "#"
    tile = tiles[y][x]

    if tile == ".":
        tiles[y][x] = get_arrow(dir)
        move(add_tupels(pos, dir), dir, tiles, energized)
    
    if tile == "/":
        if dir == Direction.NORTH:
            move(add_tupels(pos, Direction.EAST), Direction.EAST, tiles, energized)
        if dir == Direction.WEST:
            move(add_tupels(pos, Direction.SOUTH), Direction.SOUTH, tiles, energized)
        if dir == Direction.SOUTH:
            move(add_tupels(pos, Direction.WEST), Direction.WEST, tiles, energized)
        if dir == Direction.EAST:
            move(add_tupels(pos, Direction.NORTH), Direction.NORTH, tiles, energized)

    if tile == "\\":
        if dir == Direction.NORTH:
            move(add_tupels(pos, Direction.WEST), Direction.WEST, tiles, energized)
        if dir == Direction.WEST:
            move(add_tupels(pos, Direction.NORTH), Direction.NORTH, tiles, energized)
        if dir == Direction.SOUTH:
            move(add_tupels(pos, Direction.EAST), Direction.EAST, tiles, energized)
        if dir == Direction.EAST:
            move(add_tupels(pos, Direction.SOUTH), Direction.SOUTH, tiles, energized)
    
    if tile == "|":
        if dir in [Direction.NORTH, Direction.SOUTH]:
            move(add_tupels(pos, dir), dir, tiles, energized)
        if dir in [Direction.WEST, Direction.EAST]:
            move(add_tupels(pos, Direction.NORTH), Direction.NORTH, tiles, energized)
            move(add_tupels(pos, Direction.SOUTH), Direction.SOUTH, tiles, energized)
        
    if tile == "-":
        if dir in [Direction.WEST, Direction.EAST]:
            move(add_tupels(pos, dir), dir, tiles, energized)
        if dir in [Direction.NORTH, Direction.SOUTH]:
            move(add_tupels(pos, Direction.WEST), Direction.WEST, tiles, energized)
            move(add_tupels(pos, Direction.EAST), Direction.EAST, tiles, energized)

    if tile in ["^", "<", "v", ">"]:
        if tile == get_arrow(dir):
            return energized
        else:
            tiles[y][x] = "2"
            move(add_tupels(pos, dir), dir, tiles, energized)

    if tile.isdigit():
        tiles[y][x] = str(int(tile) + 1)
        move(add_tupels(pos, dir), dir, tiles, energized)

    return energized

def parse(puzzle_input):
    """Parse input."""

    return [list(line) for line in puzzle_input.splitlines()]

def part1(data):
    """Solve part 1."""

    energized = move((0, 0), Direction.EAST, copy.deepcopy(data), copy.deepcopy(data))

    return sum([line.count("#") for line in energized])

def part2(data):
    """Solve part 2."""

    count = []

    for y in range(len(data)):
        energized = move((y, 0), Direction.EAST, copy.deepcopy(data), copy.deepcopy(data))
        count.append(sum([line.count("#") for line in energized]))

        energized = move((y, len(data[0]) - 1), Direction.WEST, copy.deepcopy(data), copy.deepcopy(data))
        count.append(sum([line.count("#") for line in energized]))

    for x in range(len(data[0])):
        energized = move((0, x), Direction.SOUTH, copy.deepcopy(data), copy.deepcopy(data))
        count.append(sum([line.count("#") for line in energized]))

        energized = move((len(data) - 1, x), Direction.NORTH, copy.deepcopy(data), copy.deepcopy(data))
        count.append(sum([line.count("#") for line in energized]))

    return max(count)

def solve(puzzle_input):
    """Solve the puzzle for the given input."""
    data = parse(puzzle_input)
    solution1 = part1(data)
    solution2 = part2(data)

    return solution1, solution2

if __name__ == "__main__":
    sys.setrecursionlimit(2500)

    for path in sys.argv[1:]:
        print(f"{path}:")
        puzzle_input = pathlib.Path(path).read_text().strip()
        solutions = solve(puzzle_input)
        print("\n".join(str(solution) for solution in solutions))