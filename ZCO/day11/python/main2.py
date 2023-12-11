import math
import itertools
import sys

DISTANCE = 1000000


def is_empty(row):
    return all(c == "." for c in row)


def galaxies(rows):
    for i, row in enumerate(rows):
        for j, c in enumerate(row):
            if c == "#":
                yield i, j


def my_range(from_, to):
    return range(from_, to, int(math.copysign(1, to - from_)))


def main():
    rows = sys.stdin.read().splitlines()
    empty_i = {i for i, row in enumerate(rows) if is_empty(row)}
    empty_j = {j for j, col in enumerate(zip(*rows)) if is_empty(col)}

    s = 0
    for g1, g2 in itertools.combinations(galaxies(rows), 2):
        s += abs(g1[0] - g2[0]) + abs(g1[1] - g2[1])
        for i in my_range(g1[0], g2[0]):
            if i in empty_i:
                s += DISTANCE - 1
        for j in my_range(g1[1], g2[1]):
            if j in empty_j:
                s += DISTANCE - 1
    print(s)


if __name__ == "__main__":
    main()
