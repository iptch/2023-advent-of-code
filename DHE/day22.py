from __future__ import annotations

from timeit import default_timer as timer
import numpy as np


class Bricks:
    coordinates = None
    depends_on = None
    x_dim = None
    y_dim = None
    n_bricks = None
    grid = None
    heights = None

    def __init__(self, day):
        input_file = open(f"input_{day}.txt", 'r')
        coordinate_strs = [line.strip().split('~') for line in input_file.readlines()]

        self.depends_on = {}
        self.coordinates = [([int(c) for c in c_str[0].split(',')], [int(c) for c in c_str[1].split(',')]) for c_str in coordinate_strs]
        upper_limits = [c[1] for c in self.coordinates]

        self.x_dim = max(upper_limits, key=lambda x: x[0])[0] + 1
        self.y_dim = max(upper_limits, key=lambda x: x[1])[1] + 1
        z_dim = max(upper_limits, key=lambda x: x[2])[2]
        self.n_bricks = len(self.coordinates)
        self.grid = np.zeros((self.x_dim, self.y_dim, z_dim))
        self.heights = np.zeros((self.x_dim, self.y_dim))

        self._fall()

    def _fall(self):
        brick_nbr = 1
        while len(self.coordinates) > 0:
            ([x_start, y_start, z_start], [x_end, y_end, z_end]) = min(self.coordinates, key=lambda x: x[0][2])

            start_height = int(np.max(self.heights[x_start:x_end + 1, y_start:y_end + 1]))
            brick_height = z_end - z_start + 1

            if start_height > 0 and not np.all(self.grid[x_start:x_end + 1, y_start:y_end + 1] == 0):
                self.depends_on[brick_nbr] = [int(d) for d in
                                              np.unique(self.grid[x_start:x_end + 1, y_start:y_end + 1, start_height - 1]) if d != 0]

            self.grid[x_start:x_end + 1, y_start:y_end + 1, start_height:start_height+brick_height] = brick_nbr
            self.heights[x_start:x_end + 1, y_start:y_end + 1] = start_height + brick_height

            self.coordinates.remove(([x_start, y_start, z_start], [x_end, y_end, z_end]))
            brick_nbr += 1

    def bricks_without_dependencies(self):
        candidates_for_removal = list(range(1, self.n_bricks + 1))

        for key in self.depends_on.keys():
            if len(self.depends_on[key]) == 1 and self.depends_on[key][0] in candidates_for_removal:
                candidates_for_removal.remove(self.depends_on[key][0])

        return candidates_for_removal

    def print(self):
        for k in range(self.grid.shape[2]):
            print(self.grid[:, :, k])

    def how_many_other_disintegrate(self, bricks_without_dependencies):
        n_others_disintegrate = []
        for i in range(1, self.n_bricks + 1):
            if i in bricks_without_dependencies:
                continue

            to_disintegrate = [i]
            disintegrated = []
            to_check = list(self.depends_on.keys())

            while len(to_disintegrate) > 0:
                current = to_disintegrate.pop()
                disintegrated.append(current)

                for brick in to_check:
                    if (all([d in disintegrated for d in self.depends_on[brick]])
                            and brick not in disintegrated
                            and brick not in to_disintegrate):
                        to_check.remove(brick)
                        to_disintegrate.append(brick)
                        # print(f'Disintegrate {key}')

            n_others_disintegrate.append(len(disintegrated) - 1)
        return n_others_disintegrate


if __name__ == '__main__':
    start = timer()

    bricks = Bricks(day=22)

    bricks_without_dependencies = bricks.bricks_without_dependencies()
    others_disintegrate = bricks.how_many_other_disintegrate(bricks_without_dependencies)

    print(f'Part 1: {len(bricks_without_dependencies)} (in {(timer() - start)} sec)')
    print(f'Part 2: {sum(others_disintegrate)} (in {(timer() - start)} sec)')
