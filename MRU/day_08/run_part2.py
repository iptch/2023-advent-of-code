import math
from functools import reduce


def get_lines_from_file(filename="input.txt"):
    lines = []
    with open(filename, 'r') as file:
        line = file.readline()
        while line:
            lines.append(line.strip())
            line = file.readline()
    return lines


def parse(lines):
    instructions = ""
    world = {}
    for i, line in enumerate(lines):
        if i == 0:
            instructions = line
            continue
        if len(line) == 0:
            # skip
            continue

        parts = line.split(" = ")
        node = parts[0]
        left, right = parts[1].replace("(", "").replace(")", "").split(",")
        world[node] = (left.strip(), right.strip())

    return instructions, world


def get_index(counter, l):
    return counter % l


def gcd(a, b):
    if b == 0:
        return a
    else:
        return gcd(b, a % b)


if __name__ == '__main__':
    index = "LR"
    instr, world = parse(get_lines_from_file('input.txt'))

    STARTS = []
    for k in world.keys():
        if k[-1] == "A":
            STARTS.append(k)

    cycles = []
    for s in STARTS:
        current_node = s
        count = 0
        runs = 0
        while True:
            n = []
            options = world[current_node]
            move = index.find(instr[get_index(count, len(instr))])
            current_node = options[move]
            count += 1
            if current_node[-1] == "Z":
                cycles.append(count)
                break

    z_lcm = math.lcm(*cycles)
    z_gdc = reduce(gcd, cycles)
    print(z_lcm, z_gdc)
    print("part 2: ", z_lcm)
