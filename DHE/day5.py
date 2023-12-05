INPUT = """seeds: 79 14 55 13

seed-to-soil map:
50 98 2
52 50 48

soil-to-fertilizer map:
0 15 37
37 52 2
39 0 15

fertilizer-to-water map:
49 53 8
0 11 42
42 0 7
57 7 4

water-to-light map:
88 18 7
18 25 70

light-to-temperature map:
45 77 23
81 45 19
68 64 13

temperature-to-humidity map:
0 69 1
1 0 69

humidity-to-location map:
60 56 37
56 93 4"""


class Map:
    source_entity = None
    target_entity = None
    ranges = []

    def __init__(self, map_string):
        self.ranges = []
        lines = map_string.splitlines()
        self.source_entity = lines[0].split(' ')[0].split('-')[0]
        self.target_entity = lines[0].split(' ')[0].split('-')[2]
        for mapping_string in lines[1:]:
            self.ranges.append(Range(mapping_string))

    def __str__(self):
        return f'Source entity: {self.source_entity}, target entity: {self.target_entity}, ranges:{self.ranges}'

    def apply(self, from_value):
        for number_range in self.ranges:
            if from_value in range(number_range.source_start, number_range.source_start + number_range.length):
                return from_value - number_range.source_start + number_range.destination_start

        else:
            return from_value

    def apply_reverse(self, to_value):
        for number_range in self.ranges:
            if to_value in range(number_range.destination_start, number_range.destination_start + number_range.length):
                return to_value - number_range.destination_start + number_range.source_start

        else:
            return to_value


class Range:
    source_start = None
    destination_start = None
    length = None

    def __init__(self, map_string):
        [self.destination_start, self.source_start, self.length] = [int(number_string) for number_string in map_string.split(' ')]


def parse_seeds_1(seed_string):
    return [int(number_string) for number_string in seed_string.split(': ')[1].split(' ')]


def parse_seeds_2(seed_string):
    prelim = [int(number_string) for number_string in seed_string.split(': ')[1].split(' ')]
    starts = prelim[::2]
    lengths = prelim[1:][::2]

    return list(zip(starts, lengths))


def find_map_for_previous_entity(target_entity, maps):
    for map in maps:
        if map.target_entity == target_entity:
            return map
    raise Exception("not found")


def map_location_reverse(location, maps):
    entity = "location"
    value = location
    while entity != "seed":
        map = find_map_for_previous_entity(entity, maps)
        value = map.apply_reverse(value)
        entity = map.source_entity
    return value


def is_seed_a(seed_candidate, seeds):
    return seed_candidate in seeds


def is_seed_b(seed_candidate, seed_ranges):
    for seed_range in seed_ranges:
        if seed_candidate >= seed_range[0] and seed_candidate < seed_range[0] + seed_range[1]:
            return True
    return False


if __name__ == '__main__':
    map_strings = INPUT.split('\n\n')
    maps = [Map(map_string) for map_string in map_strings[1:]]

    # --- part 1 ---
    seeds = parse_seeds_1(map_strings[0])
    is_seed = False
    location = -1

    while not is_seed:
        location += 1
        is_seed = is_seed_a(map_location_reverse(location, maps), seeds)

    print(location)

    # --- part 2 ---
    seeds = parse_seeds_2(map_strings[0])
    is_seed = False
    location = -1

    while not is_seed:
        location += 1
        is_seed = is_seed_b(map_location_reverse(location, maps), seeds)

    print(location)
