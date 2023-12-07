import re


def parse(path):
    with open(path) as f:
        lines = f.read().splitlines()

    res = []
    for l in lines:
        res.append(l.split(' '))
    return res


def parseSol(path):
    with open(path) as f:
        lines = f.read().splitlines()
    if len(lines) == 0:
        return []
    return lines[0]


def part1(data):
    if data == []:
        return "missing"
    sum = 0
    print(data)
    graded = sorted(data, key=grade)
    for indx, g in enumerate(graded):
        sum += (indx + 1) * int(g[1])
    print(sum)
    return sum


def part2(data):
    if data == []:
        return "missing"
    sum = 0
    graded = sorted(data, key=gradewithjokers)
    for indx, g in enumerate(graded):
        sum += (indx + 1) * int(g[1])
    print(sum)
    return sum

def grade(entry):
    cards = entry[0]
    s = {}
    ma = 0
    for c in cards:
        if c in s:
            s[c] += 1
            ma = max(s[c], ma)
        else:
            s[c] = 1
    typ = findtyp(s, ma)
    cc = {}
    cc[1] = 0
    cc[2] = 0
    cc[3] = 0
    cc[4] = 0
    cc[5] = 0
    for c, val in s.items():
        cc[val] += 1

    cardvals = ''.join([cardval(c) for c in cards])
    print("card: ", cards, "val", str(typ) + cardvals)

    if typ == 1:
        assert cc[1] > 0 and cc[2] == 0 and cc[3] == 0 and cc[4] == 0 and cc[5] == 0
    if typ == 2:
        assert cc[1] == 3 and cc[2] == 1 and cc[3] == 0 and cc[4] == 0 and cc[5] == 0
    if typ == 3:
        assert cc[1] == 1 and cc[2] == 2 and cc[3] == 0 and cc[4] == 0 and cc[5] == 0
    if typ == 4:
        assert cc[1] == 2 and cc[2] == 0 and cc[3] == 1 and cc[4] == 0 and cc[5] == 0
    if typ == 5:
        assert cc[1] == 0 and cc[2] == 1 and cc[3] == 1 and cc[4] == 0 and cc[5] == 0
    if typ == 6:
        assert cc[1] == 1 and cc[2] == 0 and cc[3] == 0 and cc[4] == 1 and cc[5] == 0
    if typ == 7:
        assert cc[1] == 0 and cc[2] == 0 and cc[3] == 0 and cc[4] == 0 and cc[5] == 1

    return int(str(typ) + cardvals)


def findtyp(cardset, maxnum):
    print(cardset, maxnum)
    typ = -1
    threeofa = 0
    if maxnum == 5:  # 5 ofa
        typ = 7
    elif maxnum == 4:  # 4 ofa
        typ = 6
    elif maxnum == 3:  #
        threeofa = 1
    if typ == -1:
        twos = 0
        for key, n in cardset.items():
            if n == 2:
                twos += 1
        if twos and threeofa:
            typ = 5
        elif threeofa:
            typ = 4
        elif twos == 2:
            typ = 3
        elif twos == 1:
            typ = 2
        #print("twos", twos)
    if typ == -1:
        typ = 1
    if typ == -1:
        raise "nope"
    return typ

def gradewithjokers(entry):
    cards = entry[0]
    countjokers = 0
    for c in cards:
        if c == 'J':
            countjokers += 1
    s = {}
    for c in cards:
        if c in s:
            s[c] += 1
        else:
            s[c] = 1
    modcard = s.copy()
    maxk = -1

    for k, v in s.items():
        if v > maxk and k != 'J':
            maxk = v
            maxloc = k

    if countjokers == 5:
        typ = 7
    else:
        modcard['J'] = 0
        modcard[maxloc] += countjokers
        typ = findtyp(modcard, modcard[maxloc])

    cardvals = ''.join([cardval(c) for c in cards])
    #print("card: ", cards, "val", str(typ) + cardvals)
    return int(str(typ) + cardvals)

def cardval(c):
    r = 0
    if c == 'A':
        r = str(14)
    elif c == 'K':
        r = str(13)
    elif c == 'Q':
        r = str(12)
    elif c == 'J':
        r = '0' + str(1)    # Todo, return str(11) if part1
    elif c == 'T':
        r = str(10)
    else:
        r = '0' + str(c)
    return r


def solvep(testNumber, skip_test=False):
    solver = part1 if testNumber == "1" else part2
    sampleIn = parse("sample-part" + testNumber + ".in")
    # sampleSolution = solver(sampleIn)
    testIn = parse("test.in")
    if (not skip_test and testIn != []):
        testSolution = solver(testIn)
        expectedTestSolution = parseSol("result-part" + testNumber + ".out")
        if (expectedTestSolution != []):
            if (not skip_test and expectedTestSolution == str(testSolution)):
                print("!!!!!!!!!Test " + testNumber + " successful!!!!!!!!  Calculating data:")
            else:
                print("Test unsuccessful. Expected " + expectedTestSolution + " but received: " +
                      str(testSolution))  # + ".\nSample result: " + str(sampleSolution))
                return
        else:
            print("Test output is: ", testSolution)

    else:
        print("No test data. Sample solution: ")  # , sampleSolution)
        return
    dataIn = parse("data.in")
    dataSolution = solver(dataIn)
    print("Final Result test " + testNumber + ": ", dataSolution)


def test(card, res):
    print(card, gradewithjokers([card, 2]), str(gradewithjokers([card, 2]))[0] == str(res))
    assert str(gradewithjokers([card, 2]))[0] == str(res)


#solvep("1")
test('KK442', 3)
test('KK442', 3)
test('KK44J', 5)
test('KK4JJ', 6)
test('KKKJJ', 7)
test('4KK4J', 5)
test('62345', 1)
test('JJ456', 4)

solvep("2")
