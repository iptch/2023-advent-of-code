import re
import operator
import functools

def parse(path):
    with open(path) as f:
        lines = f.read().splitlines()

    times = []
    distances = []
    for line in lines:

        if 'Time' in line:
            times = [int(s.lstrip()) for s in line.split(':')[1].split(' ') if s != ' ' and s != '']
        elif 'Distance' in line:
            distances = [int(s.lstrip()) for s in line.split(':')[1].split(' ') if s != ' ' and s != '']
    data = [times, distances]
    print("len data", len(data))
    return data


def parseSol(path):
    with open(path) as f:
        lines = f.read().splitlines()
    if len(lines) == 0:
        return []
    return lines[0]


def part1(data):
    print(data)
    times, distances = data
    if data == []:
        return "missing"
    sum = []
    for i, t in enumerate(times):
        wins = 0
        maxtime = times[i]
        speedtime = 0
        while speedtime < t:
            winner = winrance(speedtime, t, distances[i])
            if winner:
                wins += 1
            speedtime += 1
        print(wins)
        sum.append(wins)
    print(sum)
    return functools.reduce(operator.mul, sum, 1)

def part2(data):
    print(data)
    times, distances = data
    maxt = int(''.join([str(t) for t in times]))
    distance = int(''.join([str(t) for t in distances]))
    if data == []:
        return "missing"
    wins = 0
    speedtime = 0
    while speedtime < maxt:
        winner = winrance(speedtime, maxt, distance)
        if wins > 0 and not winner:
            break
        if winner:
            wins += 1
        speedtime += 1
    return wins
def winranceacc(speedtime, goal):
    dist = 0.5 * speedtime * speedtime
    return dist > goal

def winrance(speedtime, totaltime, goal):
    if (speedtime > totaltime):
        print("error")
    dist = (totaltime - speedtime) * speedtime
    return dist > goal

def solvep(testNumber, skip_test=False):
    solver = part1 if testNumber == "1" else part2
    sampleIn = parse("sample-part" + testNumber + ".in")
    sampleSolution = -42 #solver(sampleIn)
    testIn = parse("test.in")
    if (not skip_test and testIn != []):
        testSolution = solver(testIn)
        expectedTestSolution = parseSol("result-part" + testNumber + ".out")
        if (expectedTestSolution != []):
            if (not skip_test and expectedTestSolution == str(testSolution)):
                print("!!!!!!!!!Test " + testNumber + " successful!!!!!!!!  Calculating data:")
            else:
                print("Test unsuccessful. Expected " + expectedTestSolution + " but received: " +
                      str(testSolution) + ".\nSample result: " + str(sampleSolution))
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
