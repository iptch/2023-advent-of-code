import re
import math

EXPECTED_SOLUTION_P1 = 114
EXPECTED_SOLUTION_P2 = 2

EQUAL_TESTS = [
    ['1', 1]
]

def parse(path):
    with open(path) as f:
        lines = f.read().splitlines()
    res = []
    instructions = -1
    for l in lines:
        res.append([int(i.lstrip().rstrip()) for i in l.split(' ')])
    return res

def part1(data):
    if data == []:
        return "missing"
    print(data)
    results = []
    for l in data:
        res = solveRec(l)
        print(res)
        results.append(res)
    return sum(results)

def solveRec(nums):
    diffs = [nums[i+1]-nums[i] for i in range(len(nums)-1)]
    if len(diffs) == 0:
        raise "unexpected"
    n = 0
    if all(i == n for i in diffs):
        return nums[-1] + n
    return nums[-1] + solveRec(diffs)

def solvePrev(nums):
    print(nums)
    diffs = [nums[i+1]-nums[i] for i in range(len(nums)-1)]
    if len(diffs) == 0:
        raise "unexpected"
    if all(i == 0 for i in diffs):
        return nums[0]
    return nums[0] - solvePrev(diffs)

def part2(data):
    if data == []:
        return "missing"
    print(data)
    results = []
    resultsPrev = []
    for l in data:
        res = solveRec(l)
        prevres = solvePrev(l)
        print(res, prevres)
        results.append(res)
        resultsPrev.append(prevres)
    return sum(resultsPrev)

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


#solvep("1")
solvep("2")
