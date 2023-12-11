import re
import math
import networkx as nx
import numpy

EQUAL_TESTS = [
    ["test.in", 'part2(data, 2)', 374],
    ["test.in", 'part2(data, 10)', 1030],
    ["test.in", 'part2(data, 100)', 8410],
    ["data.in", 'part2(data, 1000000)', None],
]

def parse(path):
    colswithnogalaxies = set()
    rowswithnogalaxies = set()
    with open(path) as f:
        lines = f.read().splitlines()

    for x, c in enumerate(lines[0]):
        colswithnogalaxies.add(x)

    for y, l in enumerate(lines):
        hasgalaxy = False
        for x, c in enumerate(l):
            if c == '#':
                hasgalaxy = True
                colswithnogalaxies.discard(x)
        if not hasgalaxy:
            rowswithnogalaxies.add(y)

    return lines, colswithnogalaxies, rowswithnogalaxies

def part1(data):
    return part2(data, 2)

def part2(data, multifactor=1000000):
    if data == []:
        return "missing"
    lines, colswithnogalaxies, rowswithnogalaxies = data
    galaxies = []
    for y, l in enumerate(lines):
        for x, c in enumerate(l):
            if c == '#':
                galaxies.append((y, x))

    sum = 0
    for x, g in enumerate(galaxies):
        for y, h in enumerate(galaxies):
            if x >= y:
                continue
            count = 0

            smaller = min(g[0], h[0])
            larger = max(g[0], h[0])
            for i in range(smaller, larger):
                if i in rowswithnogalaxies:
                    count += multifactor
                else:
                    count += 1
            smaller = min(g[1], h[1])
            larger = max(g[1], h[1])
            for i in range(smaller, larger):
                if i in colswithnogalaxies:
                    count += multifactor
                else:
                    count += 1

            sum += count
    return sum


def solveAll():
    for filename, expression, expected in EQUAL_TESTS:
        data = parse(filename)
        res = eval(expression)
        if expected is None:
            print("Result of", expression, "for", filename, ":", res)
        elif not eval(expression) == expected:
            print(filename, expression, "test failed. Resulted in:", res, "but expected", expected)
            break

solveAll()
