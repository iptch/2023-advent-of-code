import re


def build_space_form_file(filename="input.txt"):
    number_space = {}
    with open(filename, 'r') as file:
        line = file.readline()
        y = 0
        while line:
            line = line.strip()
            number_space.update(build_space_by_line(line, y))
            line = file.readline()
            y += 1
    return number_space


def build_space_by_line(line, y):
    line_space = {}
    for n, i in zip(get_numbers(line), get_numbers_index(line)):
        for x in range(i, len(n) + i):
            line_space[f"{x}:{y}"] = int(n)

    return line_space


def sum_part_numbers(space, filename="input.txt"):
    with open(filename, 'r') as file:
        line = file.readline()
        total_sum = 0
        line_number = 0
        while line:
            line = line.strip()
            for i in get_marker_index(line):
                found = set()
                for x in range(i - 1, i + 2):
                    for y in range(line_number - 1, line_number + 2):
                        key = f"{x}:{y}"
                        if key in space:
                            n = space[key]
                            found.add(n)
                if len(found) == 2:
                    total_sum += (found.pop() * found.pop())

            line_number += 1
            line = file.readline()

    return total_sum


def get_numbers(text):
    return re.findall(r"\d+", text)


def get_numbers_index(text):
    return [m.start() for m in re.finditer(r"\d+", text)]


def get_marker_index(text):
    return [m.start() for m in re.finditer(r"\*", text)]


if __name__ == '__main__':
    file = 'input.txt'
    space = build_space_form_file(file)
    part2 = sum_part_numbers(space, file)
    print(f"sum part 2: {part2}")
