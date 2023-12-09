from __future__ import annotations
import re
from timeit import default_timer as timer
import numpy as np


class Parser:
    inputs = None

    def __init__(self, day: int):
        input_file = open(f"input_{day}.txt", 'r')
        input_lines = [re.findall(r'-?\d+\.?\d*', input_line) for input_line in input_file.readlines()]
        self.inputs = [np.array(line, dtype=int) for line in input_lines]


def solve(input_arr):
    new_last = input_arr[-1]
    new_first = input_arr[0]
    sign = -1
    current_arr = np.copy(input_arr)
    while not np.all(current_arr == 0):
        current_arr = np.diff(current_arr)
        new_last += current_arr[-1]
        new_first += sign * current_arr[0]
        sign *= -1

    return new_first, new_last


if __name__ == '__main__':
    start = timer()
    parser = Parser(9)
    results = [solve(line) for line in parser.inputs]

    print(f'Part 1: {sum([result[0] for result in results])}')
    print(f'Part 2: {sum([result[1] for result in results])}')
    print(f'Total time: {(timer() - start) * 1000} ms')
