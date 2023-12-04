from timeit import default_timer as timer
import re


def puzzle_1():
    input_txt = open("input.txt", "r")
    total = 0
    for line in input_txt:
        if len(line) <= 0:
            continue
        numbers = re.findall(r"\d", line)
        if len(numbers) < 1:
            continue
        total += int(numbers[0] + numbers[-1])
    return total


def puzzle_2():
    input_txt = open("input.txt", "r")
    total = 0
    spelled = {"one": "1", "two": "2", "three": "3", "four": "4", "five": "5", "six": "6", "seven": "7", "eight": "8", "nine": "9", "1": "1", "2": "2", "3": "3", "4": "4", "5": "5", "6": "6", "7": "7", "8": "8", "9": "9"}
    for line in input_txt:
        if len(line) <= 0:
            continue
        i = 0
        numbers = []
        while i < len(line):
            for k, v in spelled.items():
                if line[i:].startswith(k):
                    numbers.append(v)
            i += 1
        if len(numbers) < 1:
            continue
        total += int(numbers[0] + numbers[-1])
    return total


if __name__ == '__main__':
    start1 = timer()
    print(f"Puzzle 1: {puzzle_1()} (in {timer()-start1}sec)")
    start2 = timer()
    print(f"Puzzle 2: {puzzle_2()} (in {timer()-start2}sec)")