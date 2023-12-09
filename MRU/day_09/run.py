def get_lines_from_file(filename="input.txt"):
    lines = []
    with open(filename, 'r') as file:
        line = file.readline()
        while line:
            lines.append(line.strip())
            line = file.readline()
    return lines


def get_div(values):
    out = []
    for i, x in enumerate(values):
        if i < len(values) - 1:
            out.append(values[i + 1] - x)
    return out


def get_sequences(values, state=[]):
    if len(state) == 0:
        state.append(values)

    n = get_div(values)
    state.append(n)

    if seq_finished(n):
        return state
    return get_sequences(n, state)


def seq_finished(values):
    return sum(values) == 0


def calc_next_values(squences):
    r = []
    for i, s in enumerate(reversed(squences)):
        # print(i, s, r)
        if len(r) > 0:
            r.append(s[-1] + r[i - 1])
        else:
            r.append(s[-1])
    return r[-1]


def calc_previous_values(squences):
    r = []
    for i, s in enumerate(reversed(squences)):
        if len(r) > 0:
            r.append(s[0] - r[i - 1])
        else:
            r.append(s[0])
    return r[-1]


def parse(lines):
    out = []
    for line in lines:
        out.append([int(x) for x in line.split(" ")])
    return out


if __name__ == '__main__':
    data = parse(get_lines_from_file(filename="input.txt"))

    next_v = []
    prev_v = []
    for d in data:
        s = get_sequences(d, state=[])
        next_v.append(calc_next_values(s))
        prev_v.append(calc_previous_values(s))

        # print(t[-1])
    print("part 1:", sum(next_v))
    print("part 2:", sum(prev_v))



