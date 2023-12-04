import re


def parse(path):
    with open(path) as f:
        lines = f.read().splitlines()
    # parse
    return lines


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
        winning = set()
        my = []
        mymode = False
        wins = 0
        asd = line.split(' ')[2:]
        print(asd)
        for l in asd:

            if l == '|':
                mymode = True
            elif ':' in l or 'Card' in l:
                continue
            elif l == '':
                continue

            elif not mymode :
                winning.add(int(l))
            else:
                num = int(l)
                my.append(int(l))
                if num in winning:
                    wins += 1
        if not wins:
            score = 0
        else:
            score = 2**(wins-1)
        print(score)
        sum += score
    return sum

def part2(data):
    if data == []:
        return "missing"
    queue = len(data) * [1]
    numcards = 0
    for line in data:
        winning = set()
        my = []
        mymode = False
        wins = 0
        asd = line.split(' ')[2:]
        for l in asd:
            if l == '|':
                mymode = True
            elif ':' in l or 'Card' in l:
                continue
            elif l == '':
                continue

            elif not mymode:
                winning.add(int(l))
            else:
                num = int(l)
                my.append(int(l))
                if num in winning:
                    wins += 1
        addcards = 0
        if len(queue):
            addcards += queue.pop(0)
        numcards += addcards

        newqueue = wins*[addcards]
        for indx, s in enumerate(newqueue):
            if indx >= len(queue):
                break
            else:
                queue[indx] += addcards
    return numcards


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
