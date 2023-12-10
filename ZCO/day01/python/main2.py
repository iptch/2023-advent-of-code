import sys

identifiers = {
        "one": 1,
        "two": 2,
        "three": 3,
        "four": 4,
        "five": 5,
        "six": 6,
        "seven": 7, 
        "eight": 8,
        "nine": 9,
        "1": 1,
        "2": 2,
        "3": 3,
        "4": 4,
        "5": 5,
        "6": 6,
        "7": 7,
        "8": 8,
        "9": 9,
}

s = 0
for line in sys.stdin:
    min_index = float('inf')
    max_index = -1

    first_digit, last_digit = None, None
    for identifier, value in identifiers.items():
        try:
            index = line.index(identifier)
            if index < min_index:
                min_index = index
                first_digit = value
            index = line.rindex(identifier)
            if index > max_index:
                max_index = index
                last_digit = value
        except ValueError:
            pass

    s += first_digit * 10 + last_digit

print(s)
