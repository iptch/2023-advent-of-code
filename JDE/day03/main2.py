import re


def parse(path):
    with open(path) as f:
        lines = f.read().splitlines()
    # parse
    symbols = set()
    gears = {}
    nums = []
    notadjnums = []
    cleaned = [list(l) for l in lines]

    for x, l in enumerate(lines):
        for y, c in enumerate(l):
            if c != '.' and not isnum(c):
                symbols.add((x, y))
                cleaned[x][y] = '.'
                if c == '*':
                    gears[(x, y)] = []

    alln = []
    for x, l in enumerate(cleaned):
        alln += re.findall(r'\d+', ''.join(l))
    for x, l in enumerate(cleaned):
        currentnum = ''
        numf = False
        adjgears = set()
        for y, c in enumerate(l):
            if not numf and isnum(c):
                currentnum = c
                numf = True
                for ag in adjGear(x, y, gears):
                    adjgears.add(ag)
            elif numf:
                if isnum(c):
                    for ag in adjGear(x, y, gears):
                        adjgears.add(ag)
                    currentnum += c
                else:
                    for g in adjgears:
                        gears[g].append(int(currentnum))
                    numf = False
                    currentnum = ''
                    adjgears = set()
        for g in adjgears:
            gears[(g[0], g[1])].append(int(currentnum))
    for g, value in gears.items():
        if len(value) == 2:
            a = value[0] * value[1]
            nums.append(a)
    return notadjnums, nums


def isnum(c):
    return c in '1234567890'


def adjGear(x, y, symbols):
    res = []
    if (x, y - 1) in symbols:
        res.append((x, y - 1))
    if (x, y + 1) in symbols:
        res.append((x, y + 1))
    if (x - 1, y) in symbols:
        res.append((x - 1, y))
    if (x + 1, y) in symbols:
        res.append((x + 1, y))
    if (x - 1, y - 1) in symbols:
        res.append((x - 1, y - 1))
    if (x - 1, y + 1) in symbols:
        res.append((x - 1, y + 1))
    if (x + 1, y + 1) in symbols:
        res.append((x + 1, y + 1))
    if (x + 1, y - 1) in symbols:
        res.append((x + 1, y - 1))
    return res


def parseSol(path):
    with open(path) as f:
        lines = f.read().splitlines()
    # parse
    if len(lines) == 0:
        return []
    return lines[0]

def part2(data):
    notadjnums, gearnums = data
    print(gearnums)
    return sum(gearnums)


def solvep(testNumber, skip_test=False):
    solver = part1 if testNumber == "1" else part2
    sampleIn = parse("sample-part" + testNumber + ".in")
    sampleSolution = solver(sampleIn)
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


# solvep("1")
solvep("2")
