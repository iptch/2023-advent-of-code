import pathlib
import sys


def parse(path):
    with open(path) as f:
        lines = f.read().splitlines()
    # parse
    return [int(l) for l in lines]


def part1(data):
    if data == []:
        return "missing"

    for indx, d  in enumerate(data):
        for indx2, d2 in enumerate(data):
            if indx == indx2:
                continue
            if d2 + d == 2020:
                return d2 * d

    return -42


def part2(data):
    if data == []:
        return "missing"

    for indx, d in enumerate(data):
        for indx2, d2 in enumerate(data):
            for indx3, d3 in enumerate(data):
                if indx >= indx2 or indx >= indx3 or indx2 >= indx3:
                    continue
                if d2 + d + d3 == 2020:
                    return d2 * d * d3

    return -42


def solvep(testNumber, skip_test=False):
    solver = part1 if testNumber == "1" else part2
    sampleIn = parse("sample-part" + testNumber + ".in")
    sampleSolution = solver(sampleIn)
    testIn = parse("test.in")
    if (not skip_test and testIn != []):
        testSolution = solver(testIn)
        expectedTestSolution = parse("result-part" + testNumber + ".out")
        if (expectedTestSolution != []):
            expectedTestSol = solver(expectedTestSolution)
            if (not skip_test and expectedTestSol == testSolution):
                print("!!!!!!!!!Test " + testNumber + " successful!!!!!!!!  Calculating data:")
            else:
                print("Test unsuccessful. Expected " + expectedTestSol + "but received: " +
                      testSolution + ".\nSample result: " + sampleSolution)
                return
        else:
            print("Test output is: ", testSolution)

    else:
        print("No test data. Sample solution: ", sampleSolution)
        return
    dataIn = parse("data.in")
    dataSolution = solver(dataIn)
    print("Final Result test " + testNumber + ": ", dataSolution)


#solvep("1")
solvep("2")
