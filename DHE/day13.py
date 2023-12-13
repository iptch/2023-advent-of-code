from __future__ import annotations
from timeit import default_timer as timer
import numpy as np


class Parser:
    grids = None

    def __init__(self, day: int):
        input_file = open(f"input_{day}.txt", 'r')
        input_lines = input_file.readlines()
        input_lines.append('\n')

        self.grids = []

        curr_grid = []
        for line in input_lines:
            if line != '\n':
                curr_grid.append([c for c in line.strip()])
            else:
                self.grids.append(np.array(curr_grid))
                curr_grid = []


def solve(grid, number_of_smudges):
    row_candidates = []
    for i in range(grid.shape[0]-1):
        if np.sum(grid[i, :] != grid[i+1, :]) <= number_of_smudges:
            row_candidates.append(i)

    for r in row_candidates:
        # row is closer to end than to start
        if grid.shape[0] - r - 1 < r + 1:
            if np.sum(grid[r+1:grid.shape[0], :] != grid[2*(r+1) - grid.shape[0]:r+1, :][::-1, :]) == number_of_smudges:
                return 100 * (r + 1)
        else:
            if np.sum(grid[:r+1, :] != grid[r+1:2*(r+1), :][::-1, :]) == number_of_smudges:
                return 100 * (r + 1)

    col_candidates = []
    for j in range(grid.shape[1]-1):
        if np.sum(grid[:, j] != grid[:, j + 1]) <= number_of_smudges:
            col_candidates.append(j)

    for c in col_candidates:
        # col is closer to end than to start
        if grid.shape[1] - c - 1 < c + 1:
            if np.sum(grid[:, c+1:grid.shape[1]] != grid[:, 2*(c+1) - grid.shape[1]:c+1][:, ::-1]) == number_of_smudges:
                return c + 1
        else:
            if np.sum(grid[:, :c+1] != grid[:, c+1:2*(c+1)][:, ::-1]) == number_of_smudges:
                return c + 1


if __name__ == '__main__':
    start = timer()
    parser = Parser(day=13)

    print(f"Puzzle 1: {sum([solve(grid, number_of_smudges=0) for grid in parser.grids])}")
    print(f"Puzzle 2: {sum([solve(grid, number_of_smudges=1) for grid in parser.grids])}")

    print(f'Total time: {(timer() - start) * 1000} ms')
