import re
import math
import networkx as nx
import numpy


EXPECTED_SOLUTION_P1 = 374
EXPECTED_SOLUTION_P2 = -1

EQUAL_TESTS = [
    ['1', 1]
]

def parse(path):
    expandedlines = []

    additionalrows = 0
    colswithnogalaxies = set()
    rowswithnogalaxies = set()
    with open(path) as f:
        lines = f.read().splitlines()
    print("before: ", len(lines), len(lines[0]))

    for y, l in enumerate(lines):
        hasgalaxy = False
        expline = []
        for x, c in enumerate(l):
            expline.append(c)
            if c == '#':
                colswithnogalaxies.add(x)
                hasgalaxy = True
        expandedlines.append(expline)
        if not hasgalaxy:
            rowswithnogalaxies.add(y)
            additionalrows += 1
            expline = []
            for x, c in enumerate(l):
                expline.append(c)
            expandedlines.append(expline)

    print("middle: ", len(expandedlines), len(expandedlines[0]))

    res = []
    for y, l in enumerate(expandedlines):
        resline = []
        for x, c in enumerate(l):
            resline.append(c)
            if x not in colswithnogalaxies:
                resline.append(c)
        res.append(resline)

    return res

def part1(data):
    if data == []:
        return "missing"
    lines = data
    G = nx.DiGraph()
    edges = []
    w = len(lines[0])
    h = len(lines)
    print("expanded: ", h, w)
    nodes = []
    galaxies = []
    for y, l in enumerate(lines):
        nodeline = []
        for x, c in enumerate(l):
            nodeline.append((y, x))
            name = (y, x)
            if c == '#':
                galaxies.append((y, x))
        nodes.append(nodeline)

    for y, nodeline in enumerate(nodes):
        for x, t in enumerate(nodeline):
            G.add_node(t)
            for n in neighbors(t, w, h):
                edges.append((t, n, {'weight': 1}))

    G.add_edges_from(edges)

    sum = 0
    cnt = 0
    #allpaths = dict(nx.all_pairs_shortest_path(G))
    for x, g in enumerate(galaxies):
        for y, h in enumerate(galaxies):
            if x >= y:
                continue
            # print("add for ", g, h, cnt)
            # path = allpaths[g][h]
            # cnt += 1
            sum += dist(g, h)
           #length = nx.shortest_path_length(G, source=g, target=h, weight="weight")
            #print(g, h, "len: ", length)
            #sum += length
    print(sum)
    return sum
    # T = nx.minimum_spanning_tree(G)
    # sorted(T.edges(data=True))
    # length = nx.shortest_path_length(G, source=SName, target=EName, weight="weight")

def dist(a, b):
    return abs(a[0]-b[0]) + abs(a[1] - b[1])


def part2(data):
    if data == []:
        return "missing"
    lines = data
    G = nx.DiGraph()
    edges = []
    w = len(lines[0])
    h = len(lines)
    print("expanded: ", h, w)
    nodes = []
    galaxies = []
    for y, l in enumerate(lines):
        nodeline = []
        for x, c in enumerate(l):
            nodeline.append((y, x))
            name = (y, x)
            if c == '#':
                galaxies.append((y, x))
        nodes.append(nodeline)

    for y, nodeline in enumerate(nodes):
        for x, t in enumerate(nodeline):
            G.add_node(t)
            for n in neighbors(t, w, h):
                edges.append((t, n, {'weight': 1}))

    G.add_edges_from(edges)

    sum = 0
    cnt = 0
    multifactor = 10
    #allpaths = dict(nx.all_pairs_shortest_path(G))
    for x, g in enumerate(galaxies):
        for y, h in enumerate(galaxies):
            if x >= y:
                continue
            for i in range(g[0], h[0]):
                break
            sum += dist(g, h)
           #length = nx.shortest_path_length(G, source=g, target=h, weight="weight")
            #print(g, h, "len: ", length)
            #sum += length
    print(sum)
    return sum

def neighbors(x, w, h):
    return [(t[0], t[1]) for t in [(x[0]-1, x[1]),(x[0]+1, x[1]),(x[0], x[1]-1),(x[0], x[1]+1)] if 0 <= t[0] < h and 0 <= t[1] < w ]


def solvep(testNumber):
    solver = part1 if testNumber == "1" else part2
    testIn = parse("test.in")  # NOTE: 1 and 2 have different tests. My template did not support that
    if ( testIn == []):
        raise "Parsed data is empty"
    testSolution = solver(testIn)
    expectedTestSolution = eval("EXPECTED_SOLUTION_P" + testNumber)
    if expectedTestSolution != -1:
        if (expectedTestSolution == testSolution):
            print("!!!!!!!!!Test " + testNumber + " successful!!!!!!!!")
        else:
            print("Test unsuccessful. Expected " + str(expectedTestSolution) + " but received: " + str(testSolution))
            return
    else:
        print("Test output is: ", testSolution)
    testsuccess = True
    for expression, expected in EQUAL_TESTS:
        res = eval(expression)
        if not eval(expression) == expected:
            testsuccess = False
            print(expression, " test failed. Rsulted in: ", res, "but expected", expected)
    if testsuccess :
        print("Additional tests successful.")
    else:
        print("Additional tests failed.")
        return 
    dataIn = parse("data.in")
    dataSolution = solver(dataIn)
    print("Full Data run ", testNumber, " resulted in: ", dataSolution)


#olvep("1")
solvep("2")
