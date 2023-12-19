from __future__ import annotations

from timeit import default_timer as timer

import numpy as np
import matplotlib.pyplot as plt


class Parser:
    instructions = None

    def __init__(self, day: int):
        input_file = open(f"input_{day}.txt", 'r')
        input_lines = [line.strip().split(' ') for line in input_file.readlines()]
        self.instructions = [Instructions(line[0], int(line[1]), line[2][1:-1]) for line in input_lines]


class Instructions:
    def __init__(self, direction, distance, color):
        self.direction = direction
        self.distance = distance
        self.color = color

    def __repr__(self):
        return f'{self.direction} {self.distance} ({self.color})'


class Solver:
    instructions = None
    grid = None
    start_pos = None

    def __init__(self, instructions):
        self.instructions = instructions

        right = []
        down = []
        for instruction in self.instructions:
            right.append(instruction.distance if 'R' == instruction.direction else 0)
            right.append(-1 * instruction.distance if 'L' == instruction.direction else 0)
            down.append(-1 * instruction.distance if 'U' == instruction.direction else 0)
            down.append(instruction.distance if 'D' == instruction.direction else 0)
        cumulative_right = np.cumsum(right)
        cumulative_down = np.cumsum(down)

        self.grid = np.zeros(
            (max(cumulative_down) - min(cumulative_down) + 1, max(cumulative_right) - min(cumulative_right) + 1))
        self.start_pos = -1 * min(cumulative_down), -1 * min(cumulative_right)

    def _paint_boundary(self):
        pos = self.start_pos

        for instruction in self.instructions:
            if instruction.direction == 'R':
                self.grid[pos[0], pos[1] + 1: pos[1] + instruction.distance + 1] = 1
                pos = (pos[0], pos[1] + instruction.distance)
            elif instruction.direction == 'D':
                self.grid[pos[0] + 1: pos[0] + instruction.distance + 1, pos[1]] = 1
                pos = (pos[0] + instruction.distance, pos[1])
            elif instruction.direction == 'L':
                self.grid[pos[0], pos[1] - instruction.distance: pos[1]] = 1
                pos = (pos[0], pos[1] - instruction.distance)
            elif instruction.direction == 'U':
                self.grid[pos[0] - instruction.distance: pos[0], pos[1]] = 1
                pos = (pos[0] - instruction.distance, pos[1])

    def _paint_interior(self, good_initial_guess_for_point_inside):
        neighbors = [good_initial_guess_for_point_inside]
        while len(neighbors) > 0:
            new_neighbors = []
            for n in neighbors:
                self.grid[n] = 2
                if n[0] > 0 and self.grid[n[0] - 1, n[1]] == 0 and (n[0] - 1, n[1]) not in new_neighbors:
                    new_neighbors.append((n[0] - 1, n[1]))
                if n[0] < self.grid.shape[0] - 1 and self.grid[n[0] + 1, n[1]] == 0 and (
                n[0] + 1, n[1]) not in new_neighbors:
                    new_neighbors.append((n[0] + 1, n[1]))
                if n[1] > 0 and self.grid[n[0], n[1] - 1] == 0 and (n[0], n[1] - 1) not in new_neighbors:
                    new_neighbors.append((n[0], n[1] - 1))
                if n[1] < self.grid.shape[1] - 1 and self.grid[n[0], n[1] + 1] == 0 and (
                n[0], n[1] + 1) not in new_neighbors:
                    new_neighbors.append((n[0], n[1] + 1))
            neighbors = new_neighbors

    def solve(self, good_initial_guess_for_point_inside):
        self._paint_boundary()
        self._paint_interior(good_initial_guess_for_point_inside)

        return np.sum(self.grid != 0)

    def display_grid(self):
        plt.imshow(self.grid)
        plt.show()


if __name__ == '__main__':
    start1 = timer()

    parser = Parser(day=18)
    solver = Solver(parser.instructions)

    # print(f'Puzzle 1: {solver.solve((1, 1))} (in {(timer() - start1) * 1000} ms)') # Example
    print(f'Puzzle 1: {solver.solve((solver.start_pos[0]-1, solver.start_pos[1]))} (in {(timer() - start1) * 1000} ms)')

    solver.grid[solver.start_pos[0]-3:solver.start_pos[0]+3, solver.start_pos[1]-3:solver.start_pos[1]+3] = 10
    solver.display_grid()

    start2 = timer()
    # print(f'Puzzle 2: {solver2.solve()} (in {(timer() - start2)} sec)')
