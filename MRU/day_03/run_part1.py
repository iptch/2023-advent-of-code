import re


def build_space_form_file(filename="input.txt"):
    marker_space = []
    with open(filename, 'r') as file:
        line = file.readline()
        y = 0
        while line:
            line = line.strip()
            marker_space.extend(build_space_by_line(line, y))
            line = file.readline()
            y += 1
    return marker_space


def build_space_by_line(line, y):
    markers = get_marker(line)
    line_space = []
    for m in markers:
        xs = get_start_index(re.escape(m), line)
        for x in xs:
            line_space.append((x, y))

    return line_space


def sum_part_numbers(space, filename="input.txt"):
    with open(filename, 'r') as file:
        line = file.readline()
        total_sum = 0
        y = 0
        while line:
            line = line.strip()
            print(line)
            for n, i in zip(get_numbers(line), get_numbers_index(line)):
                for x in range(i, len(n) + i):
                    # print(f"check: x={x}, y={y}", is_adjacent(x, y, space))
                    if is_adjacent(x, y, space):
                        total_sum += int(n)
                        break
            line = file.readline()
            y += 1
    return total_sum


def get_numbers(text):
    return re.findall(r"\d+", text)


def get_numbers_index(text):
    return [m.start() for m in re.finditer(r"\d+", text)]


def get_marker(text):
    return re.findall(r"[^\d|.]", text)


def get_start_index(text, line):
    return [m.start() for m in re.finditer(text, line)]


def is_adjacent(x, y, space):
    # space = [(1, 2), (2, 2), (2, 3)]
    # Check if (x, y) is adjacent to any coordinate in the space
    for coord in space:
        other_x, other_y = coord
        # Check if the coordinates differ by at most 1 in either x or y direction
        if abs(x - other_x) <= 1 and abs(y - other_y) <= 1 and (x != other_x or y != other_y):
            return True
    # If no adjacent coordinates are found, return False
    return False


if __name__ == '__main__':
    file = 'input.txt'
    space = build_space_form_file(file)
    part1 = sum_part_numbers(space, file)
    print(f"sum part 1: {part1}")
