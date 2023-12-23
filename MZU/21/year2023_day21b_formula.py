from timeit import default_timer as timer

DAY = '21'
PART = 'b'


def solve(steps):
    pattern_start = 128  # from excel sheet
    pattern_length = 131  # from excel sheet

    index = (steps - pattern_start) % pattern_length
    pattern_repetitions = int((steps - pattern_start) / pattern_length)
    print(index)

    current_value = 96471  # from excel sheet
    diff = 61686  # from excel sheet
    magic_number = 30794  # from excel sheet
    for i in range(pattern_repetitions - 1):
        diff += magic_number
        current_value += diff

    return current_value


def main():
    print(f'Advent of Code 2023 --- Day {DAY} --- Part {PART}')

    result = solve(26501365)

    print(f'{str(result)}')


if __name__ == '__main__':
    start = timer()
    main()
    print(f"Completed in {timer() - start} sec")
