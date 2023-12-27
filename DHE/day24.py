from __future__ import annotations
from timeit import default_timer as timer

from sympy import solve
from sympy.abc import x, y, z, a, b, c, u, v, w


class Storm:
    area = None
    particles = None

    def __init__(self, day, area):
        input_file = open(f"input_{day}.txt", 'r')
        self.particles = [Line(line.strip()) for line in input_file.readlines()]
        self.area = area

    def compute_crossings_in_xy(self):
        n = len(self.particles)
        crossings = []
        for i in range(n):
            for j in range(i + 1, n):
                if self.particles[i].crosses_in_area_xy(self.particles[j], self.area):
                    crossings.append((self.particles[i], self.particles[j]))
        return crossings

    def hit_all(self):
        la = self.particles[0]
        lb = self.particles[1]
        lc = self.particles[2]

        equations = [x + u * a - la.x - la.vx * a,
                     y + v * a - la.y - la.vy * a,
                     z + w * a - la.z - la.vz * a,
                     x + u * b - lb.x - lb.vx * b,
                     y + v * b - lb.y - lb.vy * b,
                     z + w * b - lb.z - lb.vz * b,
                     x + u * c - lc.x - lc.vx * c,
                     y + v * c - lc.y - lc.vy * c,
                     z + w * c - lc.z - lc.vz * c]

        result = solve(equations, [x, y, z, u, v, w, a, b, c], dict=True)[0]
        return [result[x], result[y], result[z]]


class Line:
    x = None
    y = None
    z = None
    vx = None
    vy = None
    vz = None

    def __init__(self, line_str):
        pos, vel = line_str.split(' @ ')
        [self.x, self.y, self.z] = [float(p) for p in pos.split(', ')]
        [self.vx, self.vy, self.vz] = [float(v) for v in vel.split(', ')]

    def __repr__(self):
        return f'({self.x}, {self.y}, {self.z} @ {self.vx}, {self.vy}, {self.vz})'

    def crosses_in_area_xy(self, other: Line, area):
        if self.vx / other.vx == self.vy / other.vy:
            return False

        nom = self.y - other.y - self.x * self.vy / self.vx + other.x * other.vy / other.vx
        denom = other.vy / other.vx - self.vy / self.vx

        x_cross = nom / denom

        if x_cross < area[0] or x_cross > area[1]:
            return False

        y_cross = self.y + (x_cross - self.x) * self.vy / self.vx

        if y_cross < area[0] or y_cross > area[1]:
            return False

        ta = (x_cross - self.x) / self.vx
        tb = (x_cross - other.x) / other.vx

        return ta > 0 and tb > 0


if __name__ == '__main__':
    start = timer()

    storm = Storm(day=24, area=(200000000000000, 400000000000000))
    crossings = storm.compute_crossings_in_xy()

    print(f'Part 1: {len(crossings)} (in {(timer() - start) * 1000} ms)')
    print(f'Part 2: {sum(storm.hit_all())} (in {(timer() - start) * 1000} ms)')
