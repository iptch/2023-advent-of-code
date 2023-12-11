import itertools
import sys


def expand(rows):
    for row in rows:
        if all(c == "." for c in row):
            yield row
        yield row


def galaxies(rows):
    for i, row in enumerate(rows):
        for j, c in enumerate(row):
            if c == "#":
                yield i, j


def transpose(rows):
    return [list(r) for r in zip(*rows)]


def main():
    rows = sys.stdin.read().splitlines()
    rows = list(expand(rows))
    rows = transpose(rows)
    rows = list(expand(rows))
    rows = transpose(rows)
    s = 0
    for g1, g2 in itertools.combinations(galaxies(rows), 2):
        s += abs(g1[0] - g2[0]) + abs(g1[1] - g2[1])
    print(s)


if __name__ == "__main__":
    main()
