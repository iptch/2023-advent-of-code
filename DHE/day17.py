from __future__ import annotations

from timeit import default_timer as timer

import numpy as np


class Parser:
    grid = None

    def __init__(self, day: int):
        input_file = open(f"input_{day}.txt", 'r')
        self.grid = np.array([[int(c) for c in line.strip()] for line in input_file.readlines()])


class Candidate:
    def __init__(self, position, direction, dir_count, curr_distance):
        self.position = position
        self.direction = direction
        self.dir_count = dir_count
        self.curr_distance = curr_distance

    def __repr__(self):
        return f'{self.position}: {self.dir_count}{self.direction} - {self.curr_distance}'


class Distance:
    def __init__(self, direction, distance, dir_count):
        self.direction = direction
        self.distance = distance
        self.dir_count = dir_count

    def __repr__(self):
        return f'{self.dir_count}{self.direction}: {self.distance}'

    def __ge__(self, other: Distance):
        if self.direction != other.direction or self.dir_count != other.dir_count:
            return False
        return self.distance >= other.distance


class Solver:
    map = None
    distances = None
    candidates = None
    minimum_turns = None
    maximum_turns = None
    allowed_turns = {'>': ['^', 'v', '>'], '<': ['^', 'v', '<'], '^': ['<', '>', '^'], 'v': ['<', '>', 'v']}

    def __init__(self, maps, minimum_turns, maximum_turns):
        self.map = maps
        self.minimum_turns = minimum_turns
        self.maximum_turns = maximum_turns
        self.distances = [[[] for _ in range(maps.shape[1])] for __ in range(maps.shape[0])]
        self.candidates = []

    def _step_in_one_dir(self, c, i, j, direction):
        proposed_distance = Distance(direction, c.curr_distance + self.map[i, j],
                                     1 if direction != c.direction else c.dir_count + 1)

        if not any([proposed_distance >= d for d in self.distances[i][j]]):
            self.distances[i][j].append(proposed_distance)
            return Candidate((i, j), proposed_distance.direction, proposed_distance.dir_count, proposed_distance.distance)
        else:
            return None

    def _get_allowed_turns(self, c: Candidate):
        if c.dir_count < self.minimum_turns:
            return [c.direction]
        else:
            allowed = [d for d in self.allowed_turns[c.direction]]
            if c.dir_count >= self.maximum_turns and c.direction in allowed:
                allowed.remove(c.direction)

            return allowed

    def _step(self):
        new_candidates = []
        c = self._select_next_candidate()

        if c.position[0] > 0 and '^' in self._get_allowed_turns(c):
            new_candidates.append(self._step_in_one_dir(c, c.position[0] - 1, c.position[1], '^'))
        if c.position[0] < self.map.shape[0] - 1 and 'v' in self._get_allowed_turns(c):
            new_candidates.append(self._step_in_one_dir(c, c.position[0] + 1, c.position[1], 'v'))
        if c.position[1] > 0 and '<' in self._get_allowed_turns(c):
            new_candidates.append(self._step_in_one_dir(c, c.position[0], c.position[1] - 1, '<'))
        if c.position[1] < self.map.shape[1] - 1 and '>' in self._get_allowed_turns(c):
            new_candidates.append(self._step_in_one_dir(c, c.position[0], c.position[1] + 1, '>'))

        self.candidates.extend([c for c in new_candidates if c is not None])

    def _select_next_candidate(self):
        if len(self.candidates) > 0:
            c = min(self.candidates, key=lambda x: x.curr_distance)
            self.candidates.remove(c)
            return c

    def _find_minimal_distance_at(self, pos):
        dist_list = [d for d in self.distances[pos[0]][pos[1]] if d.dir_count >= self.minimum_turns]
        return min(dist_list, key=lambda x: x.distance)

    def solve(self):
        self.candidates.append(Candidate((0, 1), '>', 1, self.map[0, 1]))
        self.candidates.append(Candidate((1, 0), 'v', 1, self.map[1, 0]))

        self.distances[0][1].append(Distance('>', self.map[0, 1], 1))
        self.distances[1][0].append(Distance('v', self.map[1, 0], 1))

        r, c = self.map.shape
        while len(self.candidates) > 0:
            if len(self.distances[r-1][c-1]) > 0:
                if max(self.distances[r-1][c-1], key=lambda x: x.dir_count).dir_count >= self.minimum_turns:
                    break
            self._step()

        return self._find_minimal_distance_at((self.map.shape[0]-1, self.map.shape[1]-1))


if __name__ == '__main__':
    parser = Parser(day=17)

    start1 = timer()
    solver1 = Solver(parser.grid, 0, 3)
    print(f'Puzzle 1: {solver1.solve()} (in {(timer() - start1)} sec)')

    start2 = timer()
    solver2 = Solver(parser.grid, 4, 10)
    print(f'Puzzle 2: {solver2.solve()} (in {(timer() - start2)} sec)')
