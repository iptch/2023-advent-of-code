# aoc_template.py

import pathlib
import sys
from enum import IntEnum
 
class Map(IntEnum):
    SEED_TO_SOIL = 0
    SOIL_TO_FERTILIZER = 1
    FERTILIZER_TO_WATER = 2
    WATER_TO_LIGHT = 3
    LIGHT_TO_TEMPERATURE = 4
    TEMPERATURE_TO_HUMIDITY = 5
    HUMIDITY_TO_LOCATION = 6

def parse_map(lines):
    map_data = []

    for line in lines:
        map_data.append(list(map(int, line.split())))

    return map_data

def get_dest(src, map_ranges):
    for line in map_ranges:
        if src >= line[1] and src < line[2]:
            return line[0] + src - line[1]

    return src

def get_location(seed, maps):
    dest = seed

    for map_ranges in maps:
        dest = get_dest(dest, map_ranges)

    return dest

def get_dest_ranges(src_ranges, map_ranges):
    dest_ranges = []

    for src_range in src_ranges:
        if src_range[0] < map_ranges[0][1]:
            dest_ranges.append((src_range[0], min(src_range[1], map_ranges[0][1])))
        
        if src_range[1] > map_ranges[-1][2]:
            dest_ranges.append((max(src_range[0], map_ranges[-1][2]), src_range[1]))

        for map_range in map_ranges:
            if src_range[0] < map_range[2] and src_range[1] > map_range[1]:
                offset = map_range[0] - map_range[1]
                dest_ranges.append((max(src_range[0], map_range[1]) + offset, min(src_range[1], map_range[2]) + offset))

    return dest_ranges

def get_location_ranges(seed_range, maps):

    ranges = [seed_range]
    
    for map_ranges in maps:
        ranges = get_dest_ranges(ranges, map_ranges)

    return ranges

def parse(puzzle_input):
    """Parse input."""

    data = {
        "seeds": None,
        "maps": [[] for _ in range(len(Map))]
    }

    current_map = None

    for line in puzzle_input.splitlines():
        if line.startswith("seeds:"):
            data["seeds"] = list(map(int, line.split()[1:]))
        elif line.startswith("seed-to-soil map:"):
            current_map = Map.SEED_TO_SOIL
        elif line.startswith("soil-to-fertilizer map:"):
            current_map = Map.SOIL_TO_FERTILIZER
        elif line.startswith("fertilizer-to-water map:"):
            current_map = Map.FERTILIZER_TO_WATER
        elif line.startswith("water-to-light map:"):
            current_map = Map.WATER_TO_LIGHT
        elif line.startswith("light-to-temperature map:"):
            current_map = Map.LIGHT_TO_TEMPERATURE
        elif line.startswith("temperature-to-humidity map:"):
            current_map = Map.TEMPERATURE_TO_HUMIDITY
        elif line.startswith("humidity-to-location map:"):
            current_map = Map.HUMIDITY_TO_LOCATION
        elif line.strip():
            numbers = list(map(int, line.split()))
            data["maps"][current_map].append((numbers[0], numbers[1], numbers[1] + numbers[2]))

    for maps in data["maps"]:
        maps.sort(key=lambda x: x[1])

    return data

def part1(data):
    """Solve part 1."""

    locations = []

    for seed in data["seeds"]:
        locations.append(get_location(seed, data["maps"]))

    return min(locations)

def part2(data):
    """Solve part 2."""

    seeds = data["seeds"]
    seed_ranges = [(seeds[i], seeds[i] + seeds[i+1]) for i in range(0, len(seeds), 2)]

    locations = []

    for seed_range in seed_ranges:
        locations += [location_range[0] for location_range in get_location_ranges(seed_range, data["maps"])]

    return min(locations)

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