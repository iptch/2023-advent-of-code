import re
import math
import matplotlib.pyplot as plt
import imageio

EXPECTED_SOLUTION_P1 = 4
EXPECTED_SOLUTION_P2 = 8

EQUAL_TESTS = [
    ['1', 1]
]

def parse(path):
    with open(path) as f:
        lines = f.read().splitlines()
    res = {}
    w = len(lines[0])
    h = len(lines)
    starttile = 0
    for x in range(w):
        for y in range(h):
            tile = lines[y][x]
            if tile == 'S':
                starttile = (y, x)
            res[(y, x)] = lines[y][x]
    return res, lines, starttile, w, h

def part1(data):
    res, lines, starttile, w, h = data
    maxnum = nexttile(starttile, (-1, -1), starttile, 0, res)
    print(maxnum)
    return maxnum // 2

def nexttile(current, previous, origin, currlength, net, binmap=set(), connections={}):
    curr = current
    prev = previous
    cl = currlength
    while True:
        if cl > 1 and conv(curr) == origin:
            print("found end")
            return cl
        binmap.add(conv(curr))

        currsign = net[conv(curr)]
        next = [curr[0]-1, curr[1]]

        if conv(next) in net and next != prev and iscompatiblewith(currsign, net[conv(next)], 0, cl):
            cl += 1
            prev = curr
            curr = next
            connections[conv(prev)] = conv(next)
            continue
        next = [curr[0], curr[1]+1]
        if conv(next) in net and next != prev and iscompatiblewith(currsign, net[conv(next)], 1, cl):
            cl += 1
            prev = curr
            curr = next
            connections[conv(prev)] = conv(next)
            continue
        next = [curr[0]+1, curr[1]]
        if conv(next) in net and next != prev and iscompatiblewith(currsign, net[conv(next)], 2, cl):
            cl += 1
            prev = curr
            curr = next
            connections[conv(prev)] = conv(next)
            continue
        next = [curr[0], curr[1]-1]
        if conv(next) in net and next != prev and iscompatiblewith(currsign, net[conv(next)], 3, cl):
            cl += 1
            prev = curr
            curr = next
            connections[conv(prev)] = conv(next)
            continue
        print("found nothing for ", curr, currsign, cl)


def iscompatiblewith(curr, next, direction, cl):
    if cl < 3 and next == 'S':
        return False
    if direction == 0: #up
        if curr == 'S':
            return next in 'S|F7'
        if curr == 'F':
            return False
        if curr == 'L':
            return next in 'S|F7'
        if curr == 'J':
            return next in 'S|F7'
        if curr == '7':
            return  False
        if curr == '|':
            return next in 'S|F7'
        if curr == '-':
            return False
    if direction == 1: #right
        if curr == 'S':
            return next in 'S-7J'
        if curr == 'F':
            return next in 'S-7J'
        if curr == 'L':
            return next in 'S-7J'
        if curr == 'J':
            return False
        if curr == '7':
            return False
        if curr == '|':
            return False
        if curr == '-':
            return next in 'S-7J'
    if direction == 2: #down
        if curr == 'S':
            return next in 'S|LJ'
        if curr == 'F':
            return  next in 'S|LJ'
        if curr == 'L':
            return False
        if curr == 'J':
            return False
        if curr == '7':
            return  next in 'S|LJ'
        if curr == '|':
            return next in 'S|LJ'
        if curr == '-':
            return False
    if direction == 3: #left
        if curr == 'S':
            return next in 'S-FL'
        if curr == 'F':
            return False
        if curr == 'L':
            return False
        if curr == 'J':
            return next in 'S-FL'
        if curr == '7':
            return next in 'S-FL'
        if curr == '|':
            return False
        if curr == '-':
            return next in 'S-FL'
    raise "not found any dir"

def neighbors(x, w, h):
    return [(t[0], t[1]) for t in [(x[0]-1, x[1]),(x[0]+1, x[1]),(x[0], x[1]-1),(x[0], x[1]+1)] if 0 <= t[0] < h and 0 <= t[1] < w ]

def conv(t):
    return (t[0], t[1])

def part2(data):
    net, lines, starttile, w, h = data
    todo = []
    pipemap = set()
    connections = {}
    nexttile(starttile, (-1, -1), starttile, 0, net, pipemap, connections)



    ## Extensions in order to model the links

    originaltiles = set()
    for x in range(w):
        for y in range(h):
            t = (y, x)
            newp = (2 * t[0], 2 * t[1])
            originaltiles.add(newp)

    w = 2*w-1
    h = 2*h-1
    extpipemap = set()
    outmap = set()
    for t in pipemap:
        newp = (2 * t[0], 2 * t[1])
        extpipemap.add(newp)
        conn = connections[t]
        newconn = (2 * conn[0], 2 * conn[1])
        if newconn[0] == newp[0]:
            extpipemap.add((newconn[0], (newp[1] + newconn[1]) /2))
        elif newconn[1] == newp[1]:
            extpipemap.add(((newp[0] + newconn[0]) / 2, newconn[1]))

    for x in extpipemap:
        plt.plot(x[1], h - x[0], '.b')
    plt.savefig("0")

    for i in range(w):
        outmap.add((-1, i))
        todo.append((-1, i))
        outmap.add((h, i))
        todo.append((h, i))
    for i in range(h):
        outmap.add((i, -1))
        todo.append((i, -1))
        outmap.add((i, w))
        todo.append((i, w))

    while len(todo) > 0:
        outt = todo.pop()
        for n in neighbors(outt, w, h):
            if n in extpipemap:
                continue
            if n in outmap:
                continue
            outmap.add(n)
            todo.append(n)


    filteredoutmap = [(t[0], t[1]) for t in outmap if  0 <= t[0] < h and  0 <= t[1] < w ]
    for x in extpipemap:
        plt.plot(x[1], h - x[0], '.b')
    plt.savefig("a")
    for x in filteredoutmap:
        plt.plot(x[1], h - x[0], '.r')

    plt.savefig("b")
    print(len(filteredoutmap))
    intiles = 0

    for x in range(w):
        for y in range(h):
            t = (y, x)
            if t in outmap:
                continue
            if t in extpipemap:
                continue
            if t in originaltiles:
                intiles += 1
                plt.plot(t[1], h - t[0], '.g')

    plt.savefig("c")
    plt.show()

    print(w*h, len(pipemap), len(outmap)-2*w-2*h, intiles)
    return intiles

def solvep(testNumber):
    solver = part1 if testNumber == "1" else part2
    testIn = parse("test3.in")  # NOTE: 1 and 2 have different tests. My template did not support that
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


#solvep("1")
solvep("2")
