# aoc_template.py

import pathlib
import sys

def parse_map(lines):
    map_data = []

    for line in lines:
        map_data.append(list(map(int, line.split())))

    return map_data

def get_destination(source, map):
    for line in map:
        if source >= line[1] and source < line[1] + line[2]:
            return line[0] + source - line[1]

    return source

def get_location(range, data):
    soil = get_destination(range, data["seed_to_soil"])
    fertilizer = get_destination(soil, data["soil_to_fertilizer"])
    water = get_destination(fertilizer, data["fertilizer_to_water"])
    light = get_destination(water, data["water_to_light"])
    temperature = get_destination(light, data["light_to_temperature"])
    humidity = get_destination(temperature, data["temperature_to_humidity"])
    location = get_destination(humidity, data["humidity_to_location"])

    return location

def parse(puzzle_input):
    """Parse input."""
    lines = puzzle_input.splitlines()

    maps = {
        "seeds": [],
        "seed_to_soil": [],
        "soil_to_fertilizer": [],
        "fertilizer_to_water": [],
        "water_to_light": [],
        "light_to_temperature": [],
        "temperature_to_humidity": [],
        "humidity_to_location": []
    }

    current_map = None

    for line in lines:
        if line.startswith("seeds:"):
            maps["seeds"] = list(map(int, line.split()[1:]))
        elif line.startswith("seed-to-soil map:"):
            current_map = "seed_to_soil"
        elif line.startswith("soil-to-fertilizer map:"):
            current_map = "soil_to_fertilizer"
        elif line.startswith("fertilizer-to-water map:"):
            current_map = "fertilizer_to_water"
        elif line.startswith("water-to-light map:"):
            current_map = "water_to_light"
        elif line.startswith("light-to-temperature map:"):
            current_map = "light_to_temperature"
        elif line.startswith("temperature-to-humidity map:"):
            current_map = "temperature_to_humidity"
        elif line.startswith("humidity-to-location map:"):
            current_map = "humidity_to_location"
        elif line.strip():
            maps[current_map].append(list(map(int, line.split())))

    return maps

def check_overlap(range1, range2):
    return not (range1[1] < range2[0] or range2[1] < range1[0])

def part1(data):
    """Solve part 1."""

    locations = []

    for seed in data["seeds"]:
        locations.append(get_location(seed, data))

    return min(locations)

def part2(data):
    """Solve part 2."""

    ranges = [(data["seeds"][i], data["seeds"][i] + data["seeds"][i+1] - 1) for i in range(0, len(data["seeds"]), 2)]
    sorted_ranges = sorted(ranges, key=lambda x: x[0])

    non_overlapping = []

    for i in range(len(sorted_ranges)):
        is_overlapping = False

        for j in range(i + 1, len(sorted_ranges)):
            if check_overlap(sorted_ranges[i], sorted_ranges[j]):
                is_overlapping = True
                break
        if not is_overlapping:
            non_overlapping.append(sorted_ranges[i])

    locations = []

    for seed_range in non_overlapping:
        for seed in range(seed_range[0], seed_range[1] + 1):
            locations.append(get_location(seed, data))

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