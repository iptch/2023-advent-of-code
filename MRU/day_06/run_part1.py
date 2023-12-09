def get_lines_from_file(filename="input.txt"):
    lines = []
    with open(filename, 'r') as file:
        line = file.readline()
        while line:
            lines.append(line.strip())
            line = file.readline()
    return lines


def parse(lines):
    time_data = None
    distance_data = None

    for line in lines:

        words = line.split()

        # Check if the line contains time or distance data
        if words[0] == 'Time:':
            # Extract time values and convert them to integers
            time_data = [int(w) for w in words[1:]]
        elif words[0] == 'Distance:':
            # Extract distance values and convert them to integers
            distance_data = [int(w) for w in words[1:]]

    return time_data, distance_data


def f(time, time_max):
    return (time_max - time) * time


if __name__ == '__main__':
    lines = get_lines_from_file(filename='input.txt')
    time, distance = parse(lines)

    n = []
    for i in range(len(time)):
        t = time[i]
        d_max = distance[i]
        r = []
        for j in range(1, t):
            r.append(f(j, t))
        n.append(len([element for element in r if element > d_max]))

    s = 1
    for i in range(len(n)):
        s = s * n[i]

    print("part 1:", s)
