import re
import math
import networkx as nx
import numpy
import itertools

EQUAL_TESTS = [
 # ["test.in", 'part1(data)', 21],
  ["test.in", 'part2(data)', 21],
  #  ["data.in", 'part1(data)', None],
    ["test.in", 'part2(data)', 525152],
    ["data.in", 'part2(data)', None],
]

def parse(path):
    with open(path) as f:
        lines = f.read().splitlines()

    return lines

def part1(data):
    sums = []
    for l in data:
        signs, numsstr = l.split(' ')
        nums = [int(i) for i in numsstr.split(',')]
        signs = presolve(signs, nums)
        permutations = getpermutations(signs)
        validperms = [p for p in permutations if isvalid(p, nums)]
        sums.append(len(validperms))
    return sum(sums)

def presolve(s, nums):



def part2(data):
    sums = []
    for l in data:
        signs, numsstr = l.split(' ')
        nums = [int(i) for i in numsstr.split(',')]
        permutations = getfasterpermutations(signs, len(nums)-1)
        validperms = [p for p in permutations if isvalid(p, nums)]
        sums.append(len(validperms))
    return sum(sums)
def getpermutations(s):
    wildcards = s.count('?')
    allperms = []
    perms = list(itertools.product('#.', repeat=wildcards))
    for p in perms:
        res = list(str(s))
        placement = 0
        for i, c in enumerate(s):
            if c == '?':
                res[i] = p[placement]
                placement += 1
        allperms.append(''.join(res))

    return allperms

def getfasterpermutations(s, placedots):
    wildcards = s.count('?')
    dots = len(s.split('.'))
    toplace = placedots - dots
    allperms = []
    inpa = toplace*'.'+(wildcards-toplace)*'#'
    pr = list(itertools.permutations(inpa))
    permset = set(pr)
    for p in permset:
        res = list(str(s))
        placement = 0
        for i, c in enumerate(s):
            if c == '?':
                res[i] = p[placement]
                placement += 1
        allperms.append(''.join(res))

    return allperms

def isvalid(perm, nums):
    grps = [len(i) for i in perm.split('.') if i != '']
    return grps == nums

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
