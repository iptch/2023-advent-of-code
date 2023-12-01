import re


def process(function, filename="input.txt"):
    total = 0
    with open(filename, 'r') as file:
        line = file.readline()
        while line:
            line = line.strip()
            n = function(line)
            total = total + n
            line = file.readline()
    return total


def extract_calibration_values_number(line):
    first_digit = None
    last_digit = None

    try:
        first_digit = int(next(char for char in line if char.isdigit()))
    except StopIteration as e:
        pass

    try:
        last_digit = int(next(char for char in reversed(line) if char.isdigit()))
    except StopIteration as e:
        pass

    return first_digit, last_digit


def extract_calibration_values_text(line):
    matches = re.findall(r'(?=(one|two|three|four|five|six|seven|eight|nine))', line)
    return matches


def str_to_int(value):
    digit_mapping = {'zero': '0', 'one': '1', 'two': '2', 'three': '3', 'four': '4',
                     'five': '5', 'six': '6', 'seven': '7', 'eight': '8', 'nine': '9'}
    return int(digit_mapping[value])


def get_index(line, value):
    return [m.start() for m in re.finditer(str(value), line)]


def part_1(line):
    n1, n2 = extract_calibration_values_number(line)
    return n1 * 10 + n2


def part_2(line):
    index = {}

    n1, n2 = extract_calibration_values_number(line)
    if n1 is not None:
        for i in get_index(line, n1):
            index[i] = n1

    if n2 is not None:
        for i in get_index(line, n2):
            index[i] = n2

    matches = extract_calibration_values_text(line)
    for m in matches:
        for i in get_index(line, m):
            index[i] = str_to_int(m)

    min_entry = min(index.keys())
    max_entry = max(index.keys())
    return index[min_entry] * 10 + index[max_entry]


if __name__ == '__main__':
    t1 = process(part_1)
    print(f"total 1: {t1}")

    t2 = process(part_2)
    print(f"total 2: {t2}")