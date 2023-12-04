from timeit import default_timer as timer
import re


def check_for_symbol(line_index, char_index, lines):
    surroundings = [
        (-1, -1), (-1, 0), (-1, 1),
        (0, -1), (0, 1),
        (1, -1), (1, 0), (1, 1)
    ]
    for s in surroundings:
        try:
            if re.search(r"[^\d\.]", lines[line_index+s[0]][char_index+s[1]]):
                return True
        except IndexError:
            pass
    return False


def puzzle_1():
    input_txt = open("input.txt", "r")
    lines = [line.rstrip() for line in input_txt]
    total = 0
    for line_index, line in enumerate(lines):
        digits = []
        has_symbol = False
        for char_index, char in enumerate(line):
            if re.search(r"\d", char):
                digits.append(char)
                has_symbol = has_symbol or check_for_symbol(line_index, char_index, lines)
                if char_index+1 < len(line) and re.search(r"\d", line[char_index+1]):
                    continue
                if has_symbol:
                    total += int("".join(digits))
                digits = []
                has_symbol = False
    return total


def check_for_gear(line_index, char_index, lines):
    surroundings = [
        (-1, -1), (-1, 0), (-1, 1),
        (0, -1), (0, 1),
        (1, -1), (1, 0), (1, 1)
    ]
    potential_gear_coordinates = set()
    for s in surroundings:
        try:
            if re.search(r"[*]", lines[line_index+s[0]][char_index+s[1]]):
                potential_gear_coordinates.add((line_index+s[0], char_index+s[1]))
        except IndexError:
            pass
    return potential_gear_coordinates


def puzzle_2():
    input_txt = open("input.txt", "r")
    lines = [line.rstrip() for line in input_txt]
    potential_gears = {}
    for line_index, line in enumerate(lines):
        digits = []
        potential_gear_coordinates = set()
        for char_index, char in enumerate(line):
            if re.search(r"\d", char):
                digits.append(char)
                potential_gear_coordinates.update(check_for_gear(line_index, char_index, lines))
                if char_index+1 < len(line) and re.search(r"\d", line[char_index+1]):
                    continue
                if len(potential_gear_coordinates) > 0:
                    for potential_gear_coordinate in potential_gear_coordinates:
                        if potential_gear_coordinate in potential_gears:
                            potential_gears[potential_gear_coordinate].append(int("".join(digits)))
                        else:
                            potential_gears[potential_gear_coordinate] = [int("".join(digits))]
                digits = []
                potential_gear_coordinates = set()
    total = 0
    for potential_gear in potential_gears.values():
        if len(potential_gear) == 2:
            total += potential_gear[0] * potential_gear[1]
    return total


if __name__ == '__main__':
    start1 = timer()
    print(f"Puzzle 1: {puzzle_1()} (in {timer()-start1}sec)")
    start2 = timer()
    print(f"Puzzle 2: {puzzle_2()} (in {timer()-start2}sec)")