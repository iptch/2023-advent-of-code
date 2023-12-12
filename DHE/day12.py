from __future__ import annotations
from timeit import default_timer as timer
from functools import cache
import re


class Parser:
    lines = None
    counts = None

    def __init__(self, day: int):
        input_file = open(f"input_{day}.txt", 'r')
        input_lines = input_file.readlines()
        self.lines = [line.split(' ')[0] for line in input_lines]
        self.counts = [[int(d) for d in re.findall(r'\d+', line)] for line in input_lines]


def line_without_leading(line, char_list):
    for i, c in enumerate(line):
        if c not in char_list:
            return line[i:]


# @cache
def solve(line, counts):

    if len(counts) == 0:
        if len(line) == 0:
            print(f'Solving line {line} for counts {counts}: 0')
            return 0
        if all([c in ['.', '?'] for c in line]):
            print(f'Solving line {line} for counts {counts}: 1')
            return 1
        else:
            print(f'Solving line {line} for counts {counts}: 0')
            return 0

    if len(line) < counts[0]:
        print(f'Solving line {line} for counts {counts}: 0')
        return 0

    if len(line) == 0 or len(counts) == 0:
        raise Exception(f"The case {line, counts} doesn't get handled properly")

    if line[0] == '.':
        result = solve(line_without_leading(line, ['.']), counts)
        print(f'Solving line {line} for counts {counts}: {result}')
        return result

    if line[0] == '?':
        if len(line) == counts[0]:
            if all([c in ['#', '?'] for c in line]):
                print(f'Solving line {line} for counts {counts}: 1')
                return 1
            else:
                print(f'Solving line {line} for counts {counts}: 0')
                return 0
        else:
            for i in range(counts[0]):
                if line[i] == '.':
                    if '#' in line[:i]:
                        print(f'Solving line {line} for counts {counts}: 0')
                        return 0
                    else:
                        result = solve(line[i:], counts)
                        print(f'Solving line {line} for counts {counts}: {result}')
                        return result
            if line[counts[0]] == '#':
                result = solve(line[1:], counts)
                print(f'Solving line {line} for counts {counts}: {result}')
                return result
            else:
                result = solve(line[1:], counts) + solve(line[counts[0]+1:], counts[1:])
                print(f'Solving line {line} for counts {counts}: {result}')
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
                return solve(line[counts[0]+1:], counts[1:])

    raise Exception(f"The case {line, counts} doesn't get handled properly")


if __name__ == '__main__':
    start = timer()
    parser = Parser(day=12)

    print(parser.lines)
    print(parser.counts)

    # print(solve("?????", [2, 1]))

    solutions = [solve(parser.lines[i], parser.counts[i]) for i in range(len(parser.lines))]
    print(solutions)

    print(f'Total time: {(timer() - start) * 1000} ms')
