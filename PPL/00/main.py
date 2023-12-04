from timeit import default_timer as timer
import re


def puzzle_1():
    result = 0
    input_txt = open("input_test_1.txt", "r")
    lines = [line.rstrip() for line in input_txt]
    for line_index, line in enumerate(lines):
        pass
    return result


def puzzle_2():
    result = 0
    input_txt = open("input_test_2.txt", "r")
    lines = [line.rstrip() for line in input_txt]
    for line_index, line in enumerate(lines):
        pass
    return result


if __name__ == '__main__':
    start1 = timer()
    print(f"Puzzle 1: {puzzle_1()} (in {timer()-start1}sec)")
    # start2 = timer()
    # print(f"Puzzle 2: {puzzle_2()} (in {timer()-start2}sec)")