from __future__ import annotations

import copy
from timeit import default_timer as timer
from functools import cache
import numpy as np


class Parser:
    grid = None

    def __init__(self, day: int):
        input_file = open(f"input_{day}.txt", 'r')
        self.grid = np.array([[c for c in line.strip()] for line in input_file.readlines()])


@cache
def tilt(row_tuple):
    row = np.array(list(row_tuple))
    for i in range(row.shape[0]):
        if row[i] == 'O':
            row[i] = '.'
            for k in list(range(i + 1))[::-1]:
                if k == 0 or row[k - 1] != '.':
                    row[k] = 'O'
                    break
    return row


class Solver:
    grid = None

    def __init__(self, grid):
        self.grid = copy.deepcopy(grid)

    def _compute_weight(self):
        row_positions = np.argwhere(self.grid == 'O')[:, 0]
        weights = self.grid.shape[0] * np.ones_like(row_positions) - row_positions
        return sum(weights)

    def _do_circle(self):
        # north
        for j in range(self.grid.shape[1]):
            self.grid[:, j] = tilt(tuple(self.grid[:, j]))
        # west
        for i in range(self.grid.shape[0]):
            self.grid[i, :] = tilt(tuple(self.grid[i, :]))
        # south
        for j in range(self.grid.shape[1]):
            self.grid[:, j] = tilt(tuple(self.grid[:, j][::-1]))[::-1]
        # west
        for i in range(self.grid.shape[0]):
            self.grid[i, :] = tilt(tuple(self.grid[i, :][::-1]))[::-1]

    def _movables_repr(self):
        movables = np.argwhere(self.grid == 'O')
        string_repr = ""
        for movable in movables:
            string_repr += str(movable[0]) + ' ' + str(movable[1]) + '  '
        return string_repr

    def _compute_weight_from_repr(self, string_repr):
        pos = [self.grid.shape[0] - int(p.split(' ')[0]) for p in string_repr.split('  ')[:-1]]
        return sum(pos)

    def solve_part_1(self):
        for j in range(self.grid.shape[1]):
            self.grid[:, j] = tilt(tuple(self.grid[:, j]))

        return self._compute_weight()

    def solve(self, cycles):
        visited_states = []
        loop_length = -1
        loop_start = -1

        for i in range(cycles):
            state_rep = self._movables_repr()
            if state_rep not in visited_states:
                visited_states.append(state_rep)
            else:
                loop_length = i - visited_states.index(state_rep)
                loop_start = visited_states.index(state_rep)
                break

            self._do_circle()

        if loop_length > -1 and loop_start > -1:
            # print(f'Loop detected: length {loop_length} with start at {loop_start}')
            target_index = loop_start + ((cycles - loop_start) % loop_length)
            final_repr = visited_states[target_index]
        else:
            final_repr = self._movables_repr()

        return self._compute_weight_from_repr(final_repr)


if __name__ == '__main__':
    parser = Parser(day=14)
    solver = Solver(parser.grid)

    start = timer()
    print(f"Puzzle 1: {solver.solve_part_1()}")
    print(f"Puzzle 2: {solver.solve(cycles=1000000000)}")

    print(f'Total time: {(timer() - start)} sec')
