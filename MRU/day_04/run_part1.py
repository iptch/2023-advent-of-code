import re


def get_lines_from_file(filename="input.txt"):
    lines = []
    with open(filename, 'r') as file:
        line = file.readline()
        while line:
            lines.append(line.strip())
            line = file.readline()
    return lines


def double_points(n):
    if n == 0:
        return 0
    return 2 ** (n - 1)


def process_input(lines):
    total = 0
    for line in lines:
        winning, numbers = extract_numbers(line)
        n = winning.intersection(numbers)
        r = double_points(len(n))
        total += r
    return total


def get_numbers(text):
    return re.findall(r"\d+", text)


def extract_numbers(line):
    w, n = line.split(":")[1].split("|")
    return set(get_numbers(w)), set(get_numbers(n))


if __name__ == '__main__':
    lines = get_lines_from_file(filename='input.txt')
    part1 = process_input(lines)
    print(f"total part 1: {part1}")
