import re


def parse(path):
    with open(path) as f:
        lines = f.read().splitlines()
    # parse
    symbols = set()
    nums = []
    notadjnums = []
    cleaned = [list(l) for l in lines]

    for x, l in enumerate(lines):
        for y, c in enumerate(l):
            if c != '.' and not isnum(c):
                symbols.add((x, y))
                cleaned[x][y] = '.'
    allnums = []
    for x, l in enumerate(cleaned):
        allnums += re.findall(r'\d+', ''.join(l))
    for x, l in enumerate(cleaned):
        currentnum = ''
        numf = False
        found = 0
        for y, c in enumerate(l):
            if not numf and isnum(c):
                currentnum += c
                numf = True
                found = isadjacent(x, y, symbols)
            elif numf:
                if isnum(c):
                    found = found or isadjacent(x, y, symbols)
                    currentnum += c
                else:
                    if c != '.':
                        print("wtf: ", c)
                    if found:
                        nums.append(int(currentnum))
                    else:
                        notadjnums.append(int(currentnum))
                    found = 0
                    numf = False
                    currentnum = ''
        if found:
            nums.append(int(currentnum))

    joined = notadjnums + nums
    print("len joined: ", len(joined), "len all: ", len(allnums))
    print(allnums)
    print(joined)
    print("setdiff ", set(allnums) - set(joined))
    subs = [i for i in allnums if not i in joined or joined.remove(i)]
    print("subs:", subs)
    return notadjnums, nums


def isnum(c):
    return c in '1234567890'


def isadjacent(x, y, symbols):
    a = (x, y - 1) in symbols
    e = (x, y + 1) in symbols
    c = (x - 1, y) in symbols
    i = (x + 1, y) in symbols

    b = (x - 1, y - 1) in symbols
    d = (x - 1, y + 1) in symbols
    f = (x + 1, y + 1) in symbols
    g = (x + 1, y - 1) in symbols
    return a or b or c or d or e or f or g or i


def parseSol(path):
    with open(path) as f:
        lines = f.read().splitlines()
    # parse
    if len(lines) == 0:
        return []
    return lines[0]


def part1(data):
    notadjnums, nums = data
    print("total nums: ", len(notadjnums) + len(nums))
    print("two numbers: ", notadjnums)
    return sum(nums)


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


solvep("1")
# solvep("2")
