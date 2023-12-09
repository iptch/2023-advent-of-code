from __future__ import annotations
from timeit import default_timer as timer
import numpy as np


class Parser:
    directions = None
    maps = None

    def __init__(self, day: int):
        input_file = open(f"input_{day}.txt", 'r')
        input_lines = input_file.readlines()
        self.directions = [int(i) for i in input_lines[0].strip().replace('L', '0').replace('R', '1')]
        self.maps = {}
        for map_part in input_lines[2:]:
            self.maps[map_part[:3]] = (map_part[7:10], map_part[12:15])

    def get_startpoints_ending_in_a(self):
        return [start_point for start_point in self.maps.keys() if start_point[2] == 'A']


class Solver:
    maps = None
    directions = None
    puzzle_part = None

    def __init__(self, maps, directions, puzzle_part):
        self.maps = maps
        self.directions = directions
        if puzzle_part != 0 and puzzle_part != 1:
            raise Exception(f'puzzle part needs to be 0 or 1 but is {puzzle_part}')
        self.puzzle_part = puzzle_part

    def _compute_length_of_path(self, start_value):
        location = start_value
        steps = 0
        while True:
            location = self.maps[location][self.directions[steps % len(self.directions)]]
            steps += 1
            if self._is_end_position(location):
                return steps

    def _is_end_position(self, location):
        if self.puzzle_part == 0:
            return 'ZZZ' == location
        else:
            return location[-1] == 'Z'

    def _get_start_positions(self):
        if self.puzzle_part == 0:
            return ['AAA']
        else:
            return parser.get_startpoints_ending_in_a()

    def solve(self):
        start_positions = self._get_start_positions()
        path_lengths = [self._compute_length_of_path(start_position) for start_position in start_positions]
        return np.lcm.reduce(path_lengths)


if __name__ == '__main__':
    parser = Parser(8)

    start1 = timer()
    solver_part_1 = Solver(parser.maps, parser.directions, 0)
    print(f'Part 1: {solver_part_1.solve()} (in {(timer() - start1) * 1000} ms)')
    start2 = timer()
    solver_part_2 = Solver(parser.maps, parser.directions, 1)
    print(f'Part 2: {solver_part_2.solve()} (in {(timer() - start2) * 1000} ms)')
