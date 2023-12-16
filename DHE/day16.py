from __future__ import annotations

from timeit import default_timer as timer

import numpy as np


class Parser:
    grid = None

    def __init__(self, day: int):
        input_file = open(f"input_{day}.txt", 'r')
        self.grid = np.array([[c for c in line.strip()] for line in input_file.readlines()])


class Solver:
    ray_grid = None
    mirror_grid = None
    candidates = None
    directions = {'>': (0, 1), '<': (0, -1), 'v': (1, 0), '^': (-1, 0)}
    backslash_map = {'>': 'v', '<': '^', 'v': '>', '^': '<'}
    slash_map = {'>': '^', '<': 'v', 'v': '<', '^': '>'}

    def __init__(self, mirror_grid):
        self.mirror_grid = mirror_grid
        self.ray_grid = np.array([['' for _ in range(mirror_grid.shape[1])] for __ in range(mirror_grid.shape[0])])
        self.candidates = []

    def _mark_new_point(self, point, dir_str):
        new_point = (point[0] + self.directions[dir_str][0], point[1] + self.directions[dir_str][1])

        if new_point[0] >= self.mirror_grid.shape[0] or new_point[1] >= self.mirror_grid.shape[1] \
                or new_point[0] < 0 or new_point[1] < 0:
            return None

        if dir_str in self.ray_grid[new_point]:
            return None

        self.ray_grid[new_point] += dir_str
        return dir_str, new_point

    def _step(self):
        new_candidates = []
        for c in self.candidates:
            dir_str = c[0]
            point = c[1]

            if dir_str in ['>', '<'] and self.mirror_grid[point] == '|':
                new_candidates.append(self._mark_new_point(point, '^'))
                new_candidates.append(self._mark_new_point(point, 'v'))
            elif dir_str in ['v', '^'] and self.mirror_grid[point] == '-':
                new_candidates.append(self._mark_new_point(point, '>'))
                new_candidates.append(self._mark_new_point(point, '<'))
            elif self.mirror_grid[point] == '\\':
                dir_str = self.backslash_map[dir_str]
                new_candidates.append(self._mark_new_point(point, dir_str))
            elif self.mirror_grid[point] == '/':
                dir_str = self.slash_map[dir_str]
                new_candidates.append(self._mark_new_point(point, dir_str))
            else:
                new_candidates.append(self._mark_new_point(point, dir_str))

        self.candidates = list(filter(lambda item: item is not None, new_candidates))

    def _solve_for_start(self, start):
        self.candidates.append(start)
        self.ray_grid[start[1]] += '>'

        while len(self.candidates) > 0:
            self._step()
        result = np.sum(self.ray_grid != '')
        self.ray_grid[self.ray_grid != ''] = ''
        return result

    def solve_part_1(self):
        return self._solve_for_start(('>', (0, 0)))

    def solve_part_2(self):
        curr_max = 0
        for j in range(self.mirror_grid.shape[1]):
            candidate_solution = self._solve_for_start(('v', (0, j)))
            if candidate_solution > curr_max:
                curr_max = candidate_solution
            candidate_solution = self._solve_for_start(('^', (self.mirror_grid.shape[1]-1, j)))
            if candidate_solution > curr_max:
                curr_max = candidate_solution

        for i in range(self.mirror_grid.shape[0]):
            candidate_solution = self._solve_for_start(('>', (i, 0)))
            if candidate_solution > curr_max:
                curr_max = candidate_solution
            candidate_solution = self._solve_for_start(('<', (i, self.mirror_grid.shape[0]-1)))
            if candidate_solution > curr_max:
                curr_max = candidate_solution

        return curr_max


if __name__ == '__main__':
    start = timer()
    parser = Parser(day=16)
    solver = Solver(parser.grid)

    print(f"Puzzle 1: {solver.solve_part_1()}")
    print(f"Puzzle 2: {solver.solve_part_2()}")

    print(f'Total time: {(timer() - start)} sec')
