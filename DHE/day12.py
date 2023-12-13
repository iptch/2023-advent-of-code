from __future__ import annotations
from timeit import default_timer as timer
from functools import cache
import copy
import re


class Parser:
    lines = None
    counts = None

    def __init__(self, day: int):
        input_file = open(f"input_{day}.txt", 'r')
        input_lines = input_file.readlines()
        self.lines = [line.split(' ')[0] for line in input_lines]
        self.counts = [[int(d) for d in re.findall(r'\d+', line)] for line in input_lines]

    def get_input_for_part_2(self):
        lines_2 = self.lines.copy()

        for i, line in enumerate(self.lines):
            for j in range(4):
                lines_2[i] += '?' + self.lines[i]

        counts_2 = copy.deepcopy(self.counts)

        for i, count in enumerate(self.counts):

            for j in range(4):
                counts_2[i].extend(self.counts[i])

        return lines_2, counts_2


def line_without_leading(line, char_list):
    for i, c in enumerate(line):
        if c not in char_list:
            return line[i:]


@cache
def solve(line, counts_tuple):
    counts = list(counts_tuple)
    if len(counts) == 0:
        if len(line) == 0:
            return 1
        if all([c in ['.', '?'] for c in line]):
            return 1
        else:
            return 0

    if line is None or len(line) < counts[0]:
        return 0

    if len(line) == 0 or len(counts) == 0:
        raise Exception(f"The case {line, counts} doesn't get handled properly")

    if line[0] == '.':
        result = solve(line_without_leading(line, ['.']), tuple(counts))
        return result

    if line[0] == '?':
        if len(line) == counts[0]:
            if len(counts) == 1:
                if all([c in ['#', '?'] for c in line]):
                    return 1
                else:
                    return 0
            else:
                return 0
        else:
            for i in range(counts[0]):
                if line[i] == '.':
                    if '#' in line[:i]:
                        return 0
                    else:
                        result = solve(line[i:], tuple(counts))
                        return result
            if line[counts[0]] == '#':
                result = solve(line[1:], tuple(counts))
                return result
            else:
                result = solve(line[1:], tuple(counts)) + solve(line[counts[0] + 1:], tuple(counts[1:]))
                return result

    if line[0] == '#':
        if len(line) == counts[0]:
            if len(counts) == 1:
                if all([c in ['?', '#'] for c in line]):
                    return 1
                else:
                    return 0
            else:
                return 0
        else:
            if any([c == '.' for c in line[:counts[0]]]):
                return 0
            if line[counts[0]] == '#':
                return 0
            else:
                return solve(line[counts[0] + 1:], tuple(counts[1:]))


if __name__ == '__main__':
    start = timer()
    parser = Parser(day=12)

    print(f'Part 1: {sum([solve(parser.lines[i], tuple(parser.counts[i])) for i in range(len(parser.lines))])}')
    lines_for_2, counts_for_2 = parser.get_input_for_part_2()
    print(f'Intermediate time: {(timer() - start) * 1000} ms')
    # print(f'Part 2: {sum([solve(lines_for_2[i], tuple(counts_for_2[i])) for i in range(len(counts_for_2))])}')
    print(f'Part 2: {sum(solve(lines_for_2[0], tuple(counts_for_2[0])))}')

    print(f'Total time: {(timer() - start) * 1000} ms')
