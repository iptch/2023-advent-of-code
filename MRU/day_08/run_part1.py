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


if __name__ == '__main__':
    index = "LR"
    instr, world = parse(get_lines_from_file('input.txt'))
    count = 0
    END = "ZZZ"
    START = "AAA"

    current_node = START
    while True:

        options = world[current_node]

        i = instr[get_index(count, len(instr))]
        move = index.find(i)
        print(f"current node {current_node}, next move: {move}, count: {count}, i: {get_index(count, len(instr))}")
        current_node = options[move]
        count += 1
        if current_node == END:
            print(f"solution {count}")
            break
