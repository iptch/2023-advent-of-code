from __future__ import annotations
from timeit import default_timer as timer
import numpy as np


class Universe:
    input_grid = None

    def __init__(self, day: int) -> None:
        input_file = open(f"input_{day}.txt", 'r')
        self.input_grid = np.array([[c for c in line.strip()] for line in input_file.readlines()])

    def _get_expanded_rows(self) -> list:
        expanded_rows = []
        for i in range(self.input_grid.shape[0])[::-1]:
            if np.all(self.input_grid[i, :] == '.'):
                expanded_rows.append(i)
        return expanded_rows

    def _get_expanded_columns(self) -> list:
        expanded_columns = []
        for j in range(self.input_grid.shape[1])[::-1]:
            if np.all(self.input_grid[:, j] == '.'):
                expanded_columns.append(j)
        return expanded_columns

    def solve(self, expansion_factor: int) -> int:
        galaxies = np.argwhere(self.input_grid == '#')
        sum_of_distances = 0

        # the rows are ordered descending because of how they were computed
        for expanded_row in self._get_expanded_rows():
            for galaxy in galaxies:
                if galaxy[0] > expanded_row:
                    galaxy[0] += expansion_factor - 1

        # the columns are ordered descending because of how they were computed
        for expanded_col in self._get_expanded_columns():
            for galaxy in galaxies:
                if galaxy[1] > expanded_col:
                    galaxy[1] += expansion_factor - 1

        for i in range(len(galaxies)):
            if i < len(galaxies) - 1:
                for j in range(i+1, len(galaxies)):
                    sum_of_distances += abs(galaxies[i][0] - galaxies[j][0]) + abs(galaxies[i][1] - galaxies[j][1])

        return sum_of_distances


if __name__ == '__main__':
    start = timer()
    universe = Universe(day=11)

    print(f'Part 1: {universe.solve(expansion_factor=2)}')
    print(f'Part 2: {universe.solve(expansion_factor=1000000)}')

    print(f'Total time: {(timer() - start) * 1000} ms')
