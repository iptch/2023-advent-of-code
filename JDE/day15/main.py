import re
import math
import networkx as nx
import numpy
import itertools

import numpy as np

EQUAL_TESTS = [
    ["test.in", 'hash("HASH")', 52],
    ["test.in", 'part1(data)', 1320],
    ["data.in", 'part1(data)', None],
    ["test.in", 'part2(data)', 145],
    ["data.in", 'part2(data)', None],
]

def parse(path):
    with open(path) as f:
        lines = f.read().splitlines()
    return lines

def hash(str):
    sum = 0
    for c in str:
        sum += int(ord(c))
        sum *= 17
        sum = sum % 256
    return sum

def part1(data):
    grps = data[0].split(',')
    grpshashed = [hash(g) for g in grps]
    print(grpshashed)
    return sum(grpshashed)


def part2(data):
    boxesLabels = []
    for i in range(256):
        boxesLabels.append([])
    grps = data[0].split(',')
    for g in grps:
        if '-' in g:
            label = g.split('-')[0]
            box = hash(label)
            labels = boxesLabels[box]
            deli = -1
            for i, l in enumerate(labels):
                if l[0] == label:
                    deli = i
            if deli != -1:
                labels.pop(deli)
        if '=' in g:
            label, val = g.split('=')
            box = hash(label)
            labels = boxesLabels[box]
            entry = [label, val ]
            deli = -1
            for i, l in enumerate(labels):
                if l[0] == label:
                    deli = i
            if deli != -1:
                labels[deli] = entry
            else:
                labels.append(entry)

    sums = []
    nonempty = [a for a in boxesLabels if a != []]
    for i, b in enumerate(boxesLabels):
        for j, l in enumerate(b):
            bx = i + 1
            slot = j + 1
            sums.append(bx * slot * int(l[1]))
    print(sums)
    return sum(sums)


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
