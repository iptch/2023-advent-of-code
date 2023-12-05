import re
import sys
from dataclasses import dataclass
from typing import Iterable, Iterator, Tuple


def iter_stdin():
    while True:
        yield sys.stdin.readline()


@dataclass(eq=True, frozen=True, order=True)
class Range:
    start: int
    end: int

    def is_empty(self) -> bool:
        return self.end <= self.start



@dataclass()
class Map:
    from_: str
    to: str
    ranges: list[Tuple[Range, int]]

    def translate_value(self, v: Range) -> Iterable[Range]:
        for r, d in self.ranges:
            # overlap left
            yield Range(v.start, min(r.start, v.end))
            # intersection
            yield Range(max(v.start, r.start) + d, min(r.end, v.end) + d)
            # update
            v = Range(max(r.end, v.start), v.end)
            if v.is_empty():
                # processing done
                return
        # remaining
        yield v


def parse_seeds_line(lines: Iterator[str]) -> list[Range]:
    ranges = []
    ints = [int(n) for n in next(lines).removeprefix("seeds:").split()]
    for i in range(len(ints) // 2):
        ranges.append(Range(ints[2 * i], ints[2 * i] + ints[2 * i + 1]))
    return ranges



MAP_HEADER = re.compile(r"([a-z]+)-to-([a-z]+) map:")


def parse_map(lines: Iterator[str]) -> Tuple[Map, bool]:
    from_, to = MAP_HEADER.match(next(lines)).groups()

    ranges = []
    while True:
        next_line = next(lines)
        if not next_line.strip():
            break
        destination_start, source_start, length = map(int, next_line.split())
        ranges.append(
            (Range(source_start, source_start + length), destination_start - source_start)
        )
    ranges.sort()
    return Map(from_, to, ranges), bool(next_line)


def main():
    lines = iter_stdin()

    seeds = parse_seeds_line(lines)
    next(lines)

    maps_by_from: dict[str, Map] = {}

    remaining_maps = True
    while remaining_maps:
        map, remaining_maps = parse_map(lines)
        maps_by_from[map.from_] = map

    from_ = "seed"
    ranges = set(seeds)

    while from_ != "location":
        map = maps_by_from[from_]
        # translate values
        new_ranges = set()
        for r in ranges:
            new_ranges.update(r for r in map.translate_value(r) if not r.is_empty())
        # update
        from_ = map.to
        ranges = new_ranges

    print(min(r.start for r in ranges))


if __name__ == "__main__":
    main()
