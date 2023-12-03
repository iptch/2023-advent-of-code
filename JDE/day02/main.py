
def parse(path):
    with open(path) as f:
        lines = f.read().splitlines()
    res = []
    for l in lines:
        possibilities = l.split(':')[1].split(';')
        poss = []
        for p in possibilities:
            rgb = [0, 0, 0]
            print(p)
            for part in p.split(','):
                if 'red' in part:
                    rgb[0] = int(part.lstrip().split(' ')[0])
                elif 'green' in part:
                    rgb[1] =int(part.lstrip().split(' ')[0])
                elif 'blue' in part:
                    rgb[2] = int(part.lstrip().split(' ')[0])
            poss.append(rgb)
        res.append(poss)
    return res

def parseSol(path):

    with open(path) as f:
        lines = f.read().splitlines()
    # parse
    if len(lines) == 0:
        return []
    return lines[0]


def part1(data):
    if data == []:
        return "missing"
    print(data)
    res = 0

    for indx, game in enumerate(data):
        gameadded = False
        for part in game:
            if part[0] > 12 or part[1] > 13 or part[2] > 14:
                gameadded = True
        if not gameadded:
            print("add ", indx + 1)
            res += indx + 1
    return res


def part2(data):
    if data == []:
        return "missing"
    print(data)
    res = 0

    for indx, game in enumerate(data):
        minR=0
        minG=0
        minB=0
        for part in game:
            minR = max(part[0], minR)
            minG = max(part[1], minG)
            minB = max(part[2], minB)
        res += minB * minR * minG
    return res

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


#solvep("1")
solvep("2")
