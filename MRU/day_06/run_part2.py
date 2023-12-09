import math


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
        if "Time:" in line:
            time_data = int(line.split(":")[1].replace(" ", ""))

        if "Distance:" in line:
            distance_data = int(line.split(":")[1].replace(" ", ""))

    return time_data, distance_data


if __name__ == '__main__':
    lines = get_lines_from_file('input.txt')
    time, distance = parse(lines)

    a = -1
    b = time
    c = - distance

    delta = math.sqrt(b ** 2 - 4 * a * c)

    x1 = (-b + delta) / (2 * a)
    x2 = (-b - delta) / (2 * a)
    print(int(x1), int(x2))
    print("part 2: ", int(x2) - int(x1))
