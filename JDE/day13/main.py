import re
import math
import networkx as nx
import numpy
import itertools

import numpy as np

EQUAL_TESTS = [
 # ["test.in", 'confirmSep("abcddcba", 4)', True],
   # ["test.in", 'confirmSep("##......#", 5)', True],
    ["test.in", 'part2(data)', 400],
    ["test.in", 'part1(data)', 405],
  ["data.in", 'part2(data)', None],
  #["data.in", 'part1(data)', None],
  #  ["data.in", 'part1(data)', None],
    #["test.in", 'part2(data)', 525152],
    #["data.in", 'part2(data)', None],
]

def parse(path):
    with open(path) as f:
        lines = f.read().splitlines()
    res  = []
    patt = []
    for l in lines:
        if l == '':
            res.append(np.array(patt))
            patt = []
        else:
            patt.append([0 if c == '.' else 1 for c in l])
    res.append(np.array(patt))
    return res

def part1(data):
    vertres = []
    horizontalres = []
    print(data)
    for k, p in enumerate(data):
        piter = list(p)
        vertfound = -1
        horfound  = -1
        seps = findvertseps(p[0])
        for s in seps:
            vertfound = True
            for l in p:
                if not confirmSep(l, s):
                    vertfound = False
                    break
            if vertfound:
                vertres.append(s)
                break
        if vertfound:
            continue
        ptransiter = np.transpose(p)
        seps = findvertseps(ptransiter[0])
        for s in seps:
            horfound = True
            for l in ptransiter:
                if not confirmSep(l, s):
                    horfound = False
                    break
            if horfound:
                horizontalres.append(s)
                break

    print(vertres)
    print(horizontalres)

    return sum(vertres) + sum(horizontalres) * 100


def findvertseps(line):
    st = []
    res = []
    for i, c in enumerate(line):
        if st != [] and st[-1] == c:
            res.append(i)
        st.append(c)
    return res


def confirmSep(line, s):
    st = []
    l = len(line)
    i = 0
    while i < s:
        st.append(line[i])
        i+=1
    j = i - 1
    while i < l and j >= 0 :
        c = line[i]
        cmirrored = st[j]
        if c != cmirrored:
            return False
        i+=1
        j-= 1
    return True

def part2(data):
    vertres = []
    horizontalres = []
    print(data)
    for k, p in enumerate(data):
        vertfound, res = forOneDim2(p)
        if vertfound:
            vertres.append(res)
            continue
        ptrans = np.transpose(p)
        horfound, res = forOneDim2(ptrans)
        if horfound:
            horizontalres.append(res)
        else:
            raise "exception"
    print(vertres)
    print(horizontalres)

    return sum(vertres) + sum(horizontalres) * 100

def forOneDim2(p):
    h = len(p)
    numseps = {}
    for x, row in enumerate(p):
        seps = findvertseps(row)
        for s in seps:
            if s in numseps:
                numseps[s].append(x)
            else:
                numseps[s] = [x]

    for k, v in list(numseps.items()):
        votes = len(v)
        if votes < h-1:
            continue
        missing = []

        for r in range(h):
            row = p[r]
            if not confirmSep(row, k):
                missing.append(r)
        if len(missing) == 1:
            return True, k
    return False, 0

def solveAll():
    for filename, expression, expected in EQUAL_TESTS:
        data = parse(filename)
        res = eval(expression)
        if expected is None:
            print("Result of", expression, "for", filename, ":", res)
        elif not eval(expression) == expected:
            print(filename, expression, "test failed. Resulted in:", res, "but expected", expected)
            break
        print(filename, expression, "test success!")


solveAll()
