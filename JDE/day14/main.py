import re
import math
import networkx as nx
import numpy
import itertools

import numpy as np

EQUAL_TESTS = [
    ["test.in", 'part1(data)', 136],
    ["data.in", 'part1(data)', 110274],

    ["test.in", 'part2(data)', 64],
    ["data.in", 'part2(data)', None],
]

def parse(path):
    with open(path) as f:
        lines = f.read().splitlines()
    res = []
    for l in lines:
        res.append(list(l))
    return np.array(res)

def part1(data):
    resulting = rollAllNorth(data)
    return scored(resulting)

def scored(data):
    h = len(data)
    score = 0
    for y, l in enumerate(data):
        print(''.join(l))
        for x, c in enumerate(l):
            if c == 'O':
                score += h-y
    print(score)
    return score


def part2(data):
    i = 0
    cycles = 1000000000
    cache = {}
    while i < cycles:
        i += 1
        for d in range(4):
            data = rollAllInDir(data, d)
        if i == 1 or i == 2 or i == 3:
            print("----------> after ", i)
            scored(data)
        hdata = hashData(data)
        if hdata in cache:
            lastStateI = cache[(hdata)]
            loopLength = i - lastStateI
            if loopLength == 1:
                 print("found loop length 1! how lucky")
                 break
            print("found! curr i ", i, " cache i:", lastStateI, "loop length: ", loopLength)
            remaining = cycles - i
            newi = cycles - (remaining % loopLength)
            print("prev i ", i, "new i", newi)
            i = newi
        else:
            hdata = hashData(data)
            cache[(hdata)] = i

    return scored(data)


def hashData(data):
    st = ''
    for y, l in enumerate(data):
        for x, c in enumerate(l):
            if c == 'O':
                st += "(" + str(y) + "," + str(x) + ")"
    return hash(st)

# 0: north, 1: east, 2: south, 3: west
def rollAllInDir(data, ind):
    dir = ind
    if ind == 1:
        dir = 3
    elif ind == 3:
        dir = 1
    data = np.rot90(data, k=dir)
    data = rollAllNorth(data)
    return np.rot90(data, k=(4-dir) % 4)

def rollAllNorth(data):
    w = len(data[0])
    limits = w * [-1]
    counts = w * [0]
    resulting = []
    for y, l in enumerate(data):
        resulting.append(l.copy())
        for x, c in enumerate(l):
            resulting[y][x] = '.'
    for y,  l in enumerate(data):
        for x, c in enumerate(l):
            if c == 'O':
                counts[x] += 1
                resulting[limits[x] + counts[x]][x] = 'O'
            elif c == '#':
                limits[x] = y
                resulting[y][x] = '#'
                counts[x] = 0
    return resulting

def solveAll():
    for filename, expression, expected in EQUAL_TESTS:
        data = parse(filename)
        res = eval(expression)
        if expected is None:
            print("Result of", expression, "for", filename, ":", res)
        elif not res == expected:
            print(filename, expression, "test failed. Resulted in:", res, "but expected", expected)
            break
        print(filename, expression, "test success!")

solveAll()
