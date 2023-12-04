INPUT = """two1nine
eightwothree
abcone2threexyz
xtwone3four
4nineeightseven2
zoneight234
7pqrstsixteen"""

DIGITSTRINGS = [
    'one',
    'two',
    'three',
    'four',
    'five',
    'six',
    'seven',
    'eight',
    'nine'
]


def get_subline_number(subline, starts=True):
    for i in range(9):
        if (starts):
            if subline.startswith(DIGITSTRINGS[i]):
                return i + 1, len(DIGITSTRINGS[i])
        else:
            if subline.endswith(DIGITSTRINGS[i]):
                return i + 1, len(DIGITSTRINGS[i])
    return 0, 0


def get_number_in_line(line):
    first_number = 0
    first_chars_left = ''

    for i, c in enumerate(line):

        n, digit_size = get_subline_number(line[i:], True)
        if n != 0:
            first_number = n
            if i == 0:
                first_chars_left = 'a'
            else:
                first_chars_left = line[:i]
            break

    if len(first_chars_left) == 0:
        first_chars_left = line

    for i, c in enumerate(first_chars_left):
        if c.isdigit():
            first_number = int(c)
            break

    # print(first_chars_left)

    last_number = 0
    chars_left = ''

    for i, c in enumerate(line):
        n, digit_size = get_subline_number(line[:len(line)-i], False)
        if n != 0:
            last_number = n
            chars_left = line[len(line)-i-digit_size:]
            break

    if len(chars_left) == 0:
        chars_left = line

    for i, c in enumerate(chars_left[::-1]):
        if c.isdigit():
            last_number = int(c)
            break

    return 10 * first_number + last_number


if __name__ == '__main__':
    lines = INPUT.split("\n")

    [print(line, get_number_in_line(line)) for line in lines]
    print(sum([get_number_in_line(line) for line in lines]))

