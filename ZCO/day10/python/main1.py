from pprint import pprint
import sys


class PipeMap:
    def __init__(self, rows: list[str]) -> None:
        self.rows = rows

    def find_start(self) -> tuple[int, int]:
        for i, row in enumerate(self.rows):
            for j, pipe in enumerate(row):
                if pipe == "S":
                    return (i, j)
        raise AssertionError

    def get_pipe(self, p: tuple[int, int]):
        return self.rows[p[0]][p[1]]

    def is_pipe(self, p: tuple[int, int]):
        return (
            0 <= p[0] < len(self.rows)
            and 0 <= p[1] < len(self.rows[0])
            and self.get_pipe(p) != "."
        )

    def maybe_neighbors(self, p: tuple[int, int]):
        pipe = self.get_pipe(p)
        if pipe == "S":
            ns = [
                (p[0] + 1, p[1]),
                (p[0], p[1] + 1),
                (p[0] - 1, p[1]),
                (p[0], p[1] - 1),
            ]
        elif pipe == "|":
            ns = [(p[0] - 1, p[1]), (p[0] + 1, p[1])]
        elif pipe == "-":
            ns = [(p[0], p[1] + 1), (p[0], p[1] - 1)]
        elif pipe == "L":
            ns = [(p[0] - 1, p[1]), (p[0], p[1] + 1)]
        elif pipe == "J":
            ns = [(p[0] - 1, p[1]), (p[0], p[1] - 1)]
        elif pipe == "7":
            ns = [(p[0] + 1, p[1]), (p[0], p[1] - 1)]
        elif pipe == "F":
            ns = [(p[0] + 1, p[1]), (p[0], p[1] + 1)]
        else:
            # not a pipe
            ns = []
        return filter(self.is_pipe, ns)

    def neighbors(self, p: tuple[int, int]):
        for n in self.maybe_neighbors(p):
            if p in self.maybe_neighbors(n):
                yield n

    def bfs(self) -> int:
        start = self.find_start()
        distances = [
            [None for _ in range(len(self.rows[0]))]
            for _ in range(len(self.rows))
        ]
        fringe = set([start])
        distance = 0
        while fringe:
            new_fringe = set()

            for p in fringe:
                distances[p[0]][p[1]] = distance

            for p in fringe:
                for np in self.neighbors(p):
                    if distances[np[0]][np[1]] is None:
                        # not yet visited
                        new_fringe.add(np)

            fringe = new_fringe
            distance += 1
        # pprint(distances)
        return distance - 1


def main():
    rows = sys.stdin.read().splitlines()
    print(PipeMap(rows).bfs())


if __name__ == "__main__":
    main()
