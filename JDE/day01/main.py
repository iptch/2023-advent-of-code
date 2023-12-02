
def parse(path):
    with open(path) as f:
        lines = f.read().splitlines()
    # parse
    return [l for l in lines]

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
    sum = 0
    for line in data:
        if not line:
            continue
        first = -1
        last = ''
        print(line)
        for d in line:
            if first == -1 and d in '1234567890':
                first = d
                last = d
            elif first != -1 and d in '1234567890':
                last = d
        print(first + last)
        sum += int(first + last)
    return sum


def part2(data):
    print("go")
    if data == []:
        return "missing"
    sum = 0
    for line in data:
        if not line:
            continue
        line = str(line)
        line = line.replace('one', 'o1ne')
        line = line.replace("two", 't2wo')
        line = line.replace('three', 'th3ree')
        line = line.replace('four', 'fo4ur')
        line = line.replace('five', 'fi5ve')
        line = line.replace('six', 'si6x')
        line = line.replace('seven', 'sev7en')
        line = line.replace('eight', 'eig8ht')
        line = line.replace('nine', 'ni9ne')
        line = line.replace('zero', 'ze0ro')
        first = -1
        last = ''
        print(line)
        for d in line:
            if first == -1 and d in '1234567890':
                first = d
                last = d
            elif first != -1 and d in '1234567890':
                last = d
        print(first + last)
        sum += int(first + last)
    return sum

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
