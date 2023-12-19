from __future__ import annotations
from timeit import default_timer as timer

import numpy as np


class Parser:
    instructions = None
    decoded_instructions = None
    directions = ['R', 'D', 'L', 'U']

    def __init__(self, day: int):
        input_file = open(f"input_{day}.txt", 'r')
        input_lines = [line.strip().split(' ') for line in input_file.readlines()]
        self.instructions = [Instruction(line[0], int(line[1])) for line in input_lines]
        self.decoded_instructions = [self._decode_color(line[2][1:-1]) for line in input_lines]

    def _decode_color(self, color):
        return Instruction(self.directions[int(color[-1])], int(color[1:-1], 16))


class Instruction:
    def __init__(self, direction, distance):
        self.direction = direction
        self.distance = distance

    def __repr__(self):
        return f'{self.direction} {self.distance}'


def solve(instructions):
    right = []

    for instruction in parser.instructions:
        right.append(instruction.distance if 'R' == instruction.direction else 0)
        right.append(-1 * instruction.distance if 'L' == instruction.direction else 0)
    cumulative_right = np.cumsum(right)

    count = 0
    pos_x = -1 * min(cumulative_right)

    for i, instr in enumerate(instructions[:-1]):
        next_instr = instructions[i + 1]
        prev_instr = instructions[i - 1]

        if instr.direction == 'D':
            count += (pos_x + 1) * (instr.distance - 1 + (prev_instr.direction == 'R') + (next_instr.direction == 'L'))
        elif instr.direction == 'U':
            count -= (pos_x) * (instr.distance - 1 + (prev_instr.direction == 'L') + (next_instr.direction == 'R'))
        elif instr.direction == 'L':
            pos_x -= instr.distance
        elif instr.direction == 'R':
            pos_x += instr.distance
    return count


if __name__ == '__main__':
    start = timer()

    parser = Parser(day=18)

    # ensure manually that the first entry in the list of instructions is 'U' or 'D'
    # (for my input that means that I move the last row to the beginning)

    print(f'Puzzle 1: {solve(parser.instructions)}')
    print(f'Puzzle 1: {solve(parser.decoded_instructions)}')

    print(f'Total time: in {(timer() - start) * 1000} ms)')
