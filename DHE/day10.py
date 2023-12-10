from __future__ import annotations
from timeit import default_timer as timer
import numpy as np


class Parser:
    input_grid = None

    def __init__(self, day: int):
        input_file = open(f"input_{day}.txt", 'r')
        self.input_grid = np.array([[Pipe(c) for c in line.strip()] for line in input_file.readlines()])


class Pipe:
    c = None
    directions = {
        '|': [(-1, 0), (1, 0)],
        '7': [(0, -1), (1, 0)],
        'F': [(0, 1), (1, 0)],
        'L': [(-1, 0), (0, 1)],
        'J': [(0, -1), (-1, 0)],
        '-': [(0, -1), (0, 1)]
    }

    def __init__(self, c):
        if c not in ['.', '|', 'S', '7', 'F', 'L', 'J', '-']:
            raise Exception(f"Invalid pipe character {c}")
        self.c = c

    def __repr__(self):
        return self.c

    def __eq__(self, other: Pipe):
        return self.c == other.c

    def get_next_directions(self):
        if self.directions.get(self.c) is None:
            raise Exception(f"Invalid pipe to get directions: {self.c}")
        else:
            return self.directions[self.c]

    def has_next_directions(self):
        return self.directions.get(self.c) is not None


class Solver:
    input_grid = None
    distances_grid = None
    next_candidates = None

    def __init__(self, input_grid):
        self.input_grid = input_grid
        self.distances_grid = -1 * np.ones_like(input_grid, dtype=int)
        self.next_candidates = []

    @staticmethod
    def _add_positions(a, b):
        return tuple(map(lambda i, j: i + j, a, b))

    @staticmethod
    def _count_occurrences_of_pipe(subgrid):
        pipes = {'-': 0, 'F': 0, '7': 0, 'L': 0, 'J': 0}
        for pipe in subgrid:
            if pipe.c in pipes.keys():
                pipes[pipe.c] += 1
        return pipes

    def _get_start_pos(self):
        grid_shape = self.input_grid.shape
        for i in range(grid_shape[0]):
            for j in range(grid_shape[1]):
                if self.input_grid[i, j] == Pipe('S'):
                    return (i, j)
        raise Exception("Start character not found")

    def _is_initial_direction(self, start_pos, direction):
        new_pos = self._add_positions(start_pos, direction)
        if 0 <= new_pos[0] < self.input_grid.shape[0] and 0 <= new_pos[1] < self.input_grid.shape[1]:
            if self.input_grid[new_pos].has_next_directions():
                directions = self.input_grid[new_pos].get_next_directions()
                for direction in directions:
                    if self._add_positions(new_pos, direction) == start_pos:
                        return True
        return False

    def _get_initial_directions(self, start_pos):
        self.distances_grid[start_pos] = 0
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        return [d for d in directions if self._is_initial_direction(start_pos, d)]

    def _replace_start(self, start_pos, start_directions):
        for k in Pipe.directions.keys():
            if start_directions[0] in Pipe.directions[k] and start_directions[1] in Pipe.directions[k]:
                self.input_grid[start_pos] = Pipe(k)

    def _do_first_step(self, start_pos, initial_dirs):
        self.distances_grid[start_pos] = 0
        new_evaluation_points = [self._add_positions(start_pos, d) for d in initial_dirs]
        for position in new_evaluation_points:
            self.distances_grid[position] = 1

        return new_evaluation_points

    def _do_step(self, next_evaluation_points):
        new_next_evaluation_points = []
        for candidate in next_evaluation_points:
            pipe = self.input_grid[candidate]
            if not pipe.has_next_directions():
                raise Exception(f"Pipe {pipe} should not have become candidate")
            next_directions = pipe.get_next_directions()

            for p in next_directions:
                neighbor = self._add_positions(candidate, p)
                if 0 <= neighbor[0] < self.input_grid.shape[0] and 0 <= neighbor[1] < self.input_grid.shape[1] and \
                        self.distances_grid[neighbor] == -1:
                    new_next_evaluation_points.append(neighbor)
                    self.distances_grid[neighbor] = self.distances_grid[candidate] + 1
        return new_next_evaluation_points

    def _get_loop_candidates(self):
        return np.argwhere(self.distances_grid == -1)

    def _is_contained_in_loop(self, candidate_pos):
        """
        candidate_pos is contained in the loop if and only if you cross the loop an odd number of times when you walk
        straight up until you reach the boundary (or in any other direction).
        """
        north = self.input_grid[:candidate_pos[0], candidate_pos[1]].copy()
        relevant_pipes = self._count_occurrences_of_pipe(north)
        crossings = relevant_pipes['-'] + abs(relevant_pipes['F'] - relevant_pipes['L'])
        return crossings % 2 == 1

    def solve_distances(self):
        start_pos = self._get_start_pos()
        initial_directions = self._get_initial_directions(start_pos)
        self._replace_start(start_pos, initial_directions)
        next_evaluation_points = self._do_first_step(start_pos, initial_directions)
        while len(next_evaluation_points) > 0:
            next_evaluation_points = self._do_step(next_evaluation_points)

    def solve_inside(self):
        inside_candidates = self._get_loop_candidates()
        for c in inside_candidates:
            self.input_grid[c[0], c[1]] = Pipe('.')

        inside_characters = 0
        for c in inside_candidates:
            inside_characters += self._is_contained_in_loop(c)
        return inside_characters


if __name__ == '__main__':
    start = timer()
    parser = Parser(10)
    solver = Solver(parser.input_grid)
    solver.solve_distances()

    print(f'Part 1: {np.max(solver.distances_grid)}')
    print(f'Part 2: {solver.solve_inside()}')
    print(f'Total time: {(timer() - start) * 1000} ms')
