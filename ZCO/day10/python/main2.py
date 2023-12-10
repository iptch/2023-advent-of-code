import sys
from dataclasses import dataclass


@dataclass(frozen=True, eq=True)
class Position:
    i: int
    j: int

    def north(self):
        return Position(self.i - 1, self.j)

    def south(self):
        return Position(self.i + 1, self.j)

    def east(self):
        return Position(self.i, self.j + 1)

    def west(self):
        return Position(self.i, self.j - 1)


class PipeMap:
    def __init__(self, rows: list[str]) -> None:
        self.rows = rows

    def count_tiles(self) -> int:
        return len(self.rows) * len(self.rows[0])

    def get_char(self, p: Position):
        return self.rows[p.i][p.j]

    def is_valid(self, p: Position):
        return 0 <= p.i < len(self.rows) and 0 <= p.j < len(self.rows[0])

    def maybe_neighbors(self, p: Position):
        pipe = self.get_char(p)
        if pipe == "S":
            ns = [
                p.north(),
                p.south(),
                p.east(),
                p.west(),
            ]
        elif pipe == "|":
            ns = [p.north(), p.south()]
        elif pipe == "-":
            ns = [p.east(), p.west()]
        elif pipe == "L":
            ns = [p.east(), p.north()]
        elif pipe == "J":
            ns = [p.north(), p.west()]
        elif pipe == "7":
            ns = [p.south(), p.west()]
        elif pipe == "F":
            ns = [p.east(), p.south()]
        else:
            # not a pipe
            ns = []
        return filter(self.is_valid, ns)

    def neighbors(self, p: Position):
        for n in self.maybe_neighbors(p):
            if p in self.maybe_neighbors(n):
                yield n

    def are_connected(self, p1: Position, p2: Position):
        if not self.is_valid(p1) and not self.is_valid(p2):
            # both are out of bounds, so we return True in order to block the "wiggler" from
            # going out of bounds.
            return True
        if not self.is_valid(p1) or not self.is_valid(p2):
            # only one is out of bounds
            return False
        return p1 in self.neighbors(p2)

    def wiggle(self) -> int:
        # this "wiggler" as I call it, starts at (0, 0), which is not in reference to a tile
        # but rather to a position between tiles.
        start = Position(0, 0)
        visiting = {start}
        marked_tiles = set()
        # dfs
        stack = [start]
        while stack:
            p = stack.pop()
            # mark surrounding tiles
            for tile in [p, p.north(), p.north().west(), p.west()]:
                if self.is_valid(tile):
                    marked_tiles.add(tile)
            # calculate neighboring positions
            neighbors = []
            if not self.are_connected(p.north(), p.north().west()):
                neighbors.append(p.north())
            if not self.are_connected(p, p.west()):
                neighbors.append(p.south())
            if not self.are_connected(p, p.north()):
                neighbors.append(p.east())
            if not self.are_connected(p.west(), p.west().north()):
                neighbors.append(p.west())

            for n in neighbors:
                if n not in visiting:
                    visiting.add(n)
                    stack.append(n)

        return self.count_tiles() - len(marked_tiles)


def main():
    rows = sys.stdin.read().splitlines()
    print(PipeMap(rows).wiggle())


if __name__ == "__main__":
    main()
