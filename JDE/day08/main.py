import re
import math

EXPECTED_SOLUTION_P1 = 6
EXPECTED_SOLUTION_P2 = 6

EQUAL_TESTS = [
    ['1', 1]
]

def parse(path):
    with open(path) as f:
        lines = f.read().splitlines()
    res = []
    instructions = -1
    for l in lines:
        if l == '':
            continue
        elif not '=' in l:
            instructions = l
        else:
            groups = [group for group in
                  re.match(r"(-?\w+) = \((-?\w+), (-?\w+)\)", l).groups()]
            print(groups)
            key = groups[0]
            val = [groups[1], groups[2]]
            res.append([key, val])
    return instructions, res

def part1(data):
    if data == []:
        return "missing"
    inst, netw = data
    net = {}
    for k, v in netw:
        net[k] = v

    pos = 'AAA'
    return solveforStart(pos, inst, net)[1]

def solveforStart(start, inst, net):

    instr = list(inst)
    lenstr = len(instr)
    pos = start
    steps = 0
    while pos != 'ZZZ':
        ii = instr[steps % lenstr]
        i = 0 if ii == 'L' else 1
        pos = net[pos][i]
        steps += 1
    return pos, steps

def takeStep(startpos, steps, inst, net):
    instr = list(inst)
    lenstr = len(instr)
    ii = instr[steps % lenstr]
    i = 0 if ii == 'L' else 1
    pos = net[startpos][i]
    return pos

def part2(data):
    if data == []:
        return "missing"
    inst, netw = data
    print(inst, netw)
    net = {}
    nodepositions = []
    for k, v in netw:
        net[k] = v
        if k[-1] == 'A':
            nodepositions.append(k)
    numnodes = len(nodepositions)

    step = 0
    endpoints = numnodes * [['a', 0]]
    nodesloops = numnodes * [0]
    while True:

        for s in range(numnodes):
            if endpoints[s][0] == nodepositions[s]:
                loop = step - endpoints[s][1]
                nodesloops[s] = loop
                print("loop found", loop, s)
            if nodepositions[s][-1] == 'Z':
                endpoints[s] = [nodepositions[s], step]
            nodepositions[s] = takeStep(nodepositions[s], step, inst, net)

        step += 1
        if all(loop != 0 for loop in nodesloops):
            return math.lcm(*nodesloops)
    return step


def part2tooslow(data):
    if data == []:
        return "missing"
    inst, netw = data
    print(inst, netw)
    net = {}
    nodepositions = []
    for k, v in netw:
        net[k] = v
        if k[-1] == 'A':
            nodepositions.append(k)
    numnodes = len(nodepositions)

    step = 0
    while not allHome(nodepositions):
        for s in range(numnodes):
            nodepositions[s] = takeStep(nodepositions[s], step, inst, net)
        step += 1

    return step


def allHome(nodepositions):
    return all(pos[-1] == 'Z' for pos in nodepositions)

def solvep(testNumber):
    solver = part1 if testNumber == "1" else part2
    testIn = parse("test2.in")  # NOTE: 1 and 2 have different tests. My template did not support that
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
