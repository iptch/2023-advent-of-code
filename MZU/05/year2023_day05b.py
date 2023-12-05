import re
from timeit import default_timer as timer

from aocd import data

DAY = '05'
PART = 'b'


def solve(lines):
    seed_ranges = [int(seed) for seed in re.findall(r'\d+', lines[0])]
    almanac = [[] for _ in range(7)]
    map_idx = 0
    for line in lines[3:]:
        numbers = re.findall(r'\d+', line)
        if numbers:
            almanac[map_idx].append({
                'dest_start': int(numbers[0]),
                'source_start': int(numbers[1]),
                'range_length': int(numbers[2])
            })
        elif not line:
            map_idx = map_idx + 1
    almanac.reverse()

    for location in range(999999999):
        position = location
        for almanac_map in almanac:
            for almanac_range in almanac_map:
                if almanac_range['dest_start'] <= \
                        position < almanac_range['dest_start'] + almanac_range['range_length']:
                    position = almanac_range['source_start'] + (position - almanac_range['dest_start'])
                    break
        for i in range(0, len(seed_ranges) - 2, 2):
            start_seed, seed_range_length = seed_ranges[i:i + 2]
            if start_seed <= position < start_seed + seed_range_length:
                return location


def main():
    print(f'Advent of Code 2023 --- Day {DAY} --- Part {PART}')

    lines = data.splitlines()
    result = solve(lines)

    print(f'{str(result)}')


if __name__ == '__main__':
    start = timer()
    main()
    print(f"Completed in {timer() - start} sec")
