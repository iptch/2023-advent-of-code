import re
import sys
from dataclasses import dataclass
from typing import Iterator, Tuple


def iter_stdin():
    while True:
        yield sys.stdin.readline()


@dataclass
class Range:
    destination_start: int
    source_start: int
    length: int


@dataclass()
class Map:
    from_: str
    to: str
    ranges: list[Range]

    def translate_value(self, v: int):
        for r in self.ranges:
            difference = v - r.source_start
            if 0 <= difference < r.length:
                return r.destination_start + difference
        return v


def parse_seeds_line(lines: Iterator[str]) -> list[int]:
    return [int(i) for i in next(lines).removeprefix("seeds:").split()]


MAP_HEADER = re.compile(r"([a-z]+)-to-([a-z]+) map:")


def parse_map(lines: Iterator[str]) -> Tuple[Map, bool]:
    from_, to = MAP_HEADER.match(next(lines)).groups()

    ranges = []
    while True:
        next_line = next(lines)
        if not next_line.strip():
            break
        destination_start, source_start, length = next_line.split()
        ranges.append(
            Range(int(destination_start), int(source_start), int(length))
        )
    return Map(from_, to, ranges), bool(next_line)


def main():
    lines = iter_stdin()

    seeds = parse_seeds_line(lines)
    print(seeds)
    next(lines)

    maps_by_from: dict[str, Map] = {}

    remaining_maps = True
    while remaining_maps:
        map, remaining_maps = parse_map(lines)
        maps_by_from[map.from_] = map

    from_ = "seed"
    values = seeds

    while from_ != "location":
        map = maps_by_from[from_]
        # translate values
        new_values = []
        for v in values:
            new_values.append(map.translate_value(v))
        # update
        from_ = map.to
        values = new_values

    print(min(values))


if __name__ == "__main__":
    main()
