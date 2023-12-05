import re


def parse(path):
    seeds = []
    seedsoil = []
    soilfert = []
    fertwater = []
    waterlight = []
    lighttemp = []
    temphumid = []
    humidloc = []
    with open(path) as f:
        lines = list(f.read().splitlines())
        lc = 0
        lmax = len(lines)
        print(lc, lmax)
        print(lines)
        for l in lines:
            lc += 1
            if 'seeds' in l:
                print(l.split(': ')[1])
                seeds = [int(c) for c in str(l.split(': ')[1]).split(' ')]
            elif 'd-to-soil' in l:
                print("break")
                break
        for i in range(lc, lmax):
            l = lines[i]
            print(i, l)
            lc += 1
            if 'map' in l:
                continue
            if l == '':
                break
            seedsoil.append([int(c) for c in l.split(' ') if c != ''])
        for i in range(lc, lmax):
            l = lines[i]
            lc += 1
            if 'map' in l:
                continue
            if l == '':
                break
            soilfert.append([int(c) for c in l.split(' ') if c != ''])
        for i in range(lc, lmax):
            l = lines[i]
            lc += 1
            if 'map' in l:
                continue
            if l == '':
                break
            fertwater.append([int(c) for c in l.split(' ') if c != ''])
        for i in range(lc, lmax):
            l = lines[i]
            lc += 1
            if 'map' in l:
                continue
            if l == '':
                break
            waterlight.append([int(c) for c in l.split(' ') if c != ''])
        for i in range(lc, lmax):
            l = lines[i]
            lc += 1
            if 'map' in l:
                continue
            if l == '':
                break
            lighttemp.append([int(c) for c in l.split(' ') if c != ''])
        for i in range(lc, lmax):
            l = lines[i]
            lc += 1
            if 'map' in l:
                continue
            if l == '':
                break
            temphumid.append([int(c) for c in l.split(' ') if c != ''])
        for i in range(lc, lmax):
            l = lines[i]
            lc += 1
            print(l.split(' '))
            if 'map' in l:
                continue
            if l == '':
                break
            humidloc.append([int(c) for c in l.split(' ') if c != ''])
    return seeds, seedsoil, soilfert, fertwater, waterlight, lighttemp, temphumid, humidloc


def parseSol(path):
    with open(path) as f:
        lines = f.read().splitlines()
    if len(lines) == 0:
        return []
    return lines[0]


def part1(data):
    if data == []:
        return "missing"
    seeds, seedsoil, soilfert, fertwater, waterlight, lighttemp, temphumid, humidloc = data
    for s in seeds:
        n = s
        n = mapthrough(seedsoil, n)
        n = mapthrough(soilfert, n)
        n = mapthrough(fertwater, n)
        n = mapthrough(waterlight, n)
        n = mapthrough(lighttemp, n)
        n = mapthrough(temphumid, n)
        n = mapthrough(humidloc, n)
        m = min(m, n)
    return m


def wmapthroughseed(data, dataMinMax, seed, cache, currmin):
    if seed in cache:
        return cache[seed]
    seeds, seedsoil, soilfert, fertwater, waterlight, lighttemp, temphumid, humidloc = data
    seedsMinMax, seedsoilMinMax, soilfertMinMax, fertwaterMinMax, waterlightMinMax, lighttempMinMax, temphumidMinMax, humidlocMinMax = dataMinMax

    n = seed
    n = mapthrough(seedsoil, seedsoilMinMax, n)
    n = mapthrough(soilfert, soilfertMinMax, n)
    n = mapthrough(fertwater, fertwaterMinMax, n)
    n = mapthrough(waterlight, waterlightMinMax, n)
    n = mapthrough(lighttemp, lighttempMinMax, n)
    n = mapthrough(temphumid, temphumidMinMax, n)
    n = mapthrough(humidloc, humidlocMinMax, n)
    cache[seed] = n
    return n

def foundpossibleseed(desiredResult, data, seeds):
    seeds, seedsoil, soilfert, fertwater, waterlight, lighttemp, temphumid, humidloc = data

    n = mapthroughReverse(humidloc, [], desiredResult)
    n = mapthroughReverse(temphumid, [], n)
    n = mapthroughReverse(lighttemp, [], n)
    n = mapthroughReverse(waterlight, [], n)
    n = mapthroughReverse(fertwater, [], n)
    n = mapthroughReverse(soilfert, [], n)
    n = mapthroughReverse(seedsoil, [], n)
    for i in range(0, len(seeds), 2):
        if n in range(seeds[i], seeds[i] + seeds[i + 1]):
            return True
    return False


def mapthrough(mtable, minmax, number):
    mn, mx = minmax
    if number < mn or number > mx:
        return number
    res = number
    for entry in mtable:
        if number >= entry[1] and number < entry[1] + entry[2]:
            res = number - entry[1] + entry[0]
            break
    return res

def mapthroughReverse(mtable, minmax, number):
    res = number
    for entry in mtable:
        if number >= entry[0] and number < entry[0] + entry[2]:
            res = number + entry[1] - entry[0]
            break
    return res

def part2(data):
    if data == []:
        return "missing"
    seeds, seedsoil, soilfert, fertwater, waterlight, lighttemp, temphumid, humidloc = data
    dataMinMax = additionaldata(data)
    seedsMinMax, seedsoilMinMax, soilfertMinMax, fertwaterMinMax, waterlightMinMax, lighttempMinMax, temphumidMinMax, humidlocMinMax = dataMinMax

    i = min(seedsoilMinMax[0], soilfertMinMax[0], fertwaterMinMax[0], waterlightMinMax[0], lighttempMinMax[0], temphumidMinMax[0], humidlocMinMax[0])
    print("startat: ", i)

    while not foundpossibleseed(i, data, seeds):
        i += 1
    return i

def part2backtrackingpossible(data):
    seeds, seedsoil, soilfert, fertwater, waterlight, lighttemp, temphumid, humidloc = data
    a = [True, findminmax(seedsoil), findminmax(soilfert), findminmax(fertwater), findminmax(waterlight),
            findminmax(lighttemp),
            findminmax(temphumid), findminmax(humidloc)]
    return any(a)

def backtrackingimpossible(maptable):

    for entry in maptable:
        mn = min(mn, entry[1])
        mx = max(mx, entry[1] + entry[2])
    print("minmax",  [mn, mx])
    return [mn, mx]


def additionaldata(data):
    seeds, seedsoil, soilfert, fertwater, waterlight, lighttemp, temphumid, humidloc = data
    return [[],findminmax(seedsoil), findminmax(soilfert), findminmax(fertwater), findminmax(waterlight), findminmax(lighttemp),
            findminmax(temphumid), findminmax(humidloc)]

def findminmax(maptable):
    mn = 1000000000000000
    mx = -1000000000000000
    for entry in maptable:
        mn = min(mn, entry[1])
        mx = max(mx, entry[1] + entry[2])
    print("minmax",  [mn, mx])
    return [mn, mx]


def solvep(testNumber, skip_test=False):
    solver = part1 if testNumber == "1" else part2
    sampleIn = parse("sample-part" + testNumber + ".in")
    #sampleSolution = solver(sampleIn)
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
