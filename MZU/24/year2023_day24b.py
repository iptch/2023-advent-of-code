import re
from timeit import default_timer as timer

from aocd import data
from z3 import Int, Solver

DAY = '24'
PART = 'b'


def solve(lines):
    hailstones = []
    for line in lines:
        x, y, z, dx, dy, dz = [int(n) for n in re.findall(r'-?\d+', line)]
        hailstones.append((x, y, z, dx, dy, dz))

    solver = Solver()
    x_solution = Int('x_solution')
    y_solution = Int('y_solution')
    z_solution = Int('z_solution')
    dx_solution = Int('dx_solution')
    dy_solution = Int('dy_solution')
    dz_solution = Int('dz_solution')

    for i, h in enumerate(hailstones[:3]):
        x, y, z, dx, dy, dz = h
        t = Int(f't{i}')
        solver.add(x + t * dx == x_solution + t * dx_solution)
        solver.add(y + t * dy == y_solution + t * dy_solution)
        solver.add(z + t * dz == z_solution + t * dz_solution)

    solver.check()
    x_solution = solver.model()[x_solution].as_long()
    y_solution = solver.model()[y_solution].as_long()
    z_solution = solver.model()[z_solution].as_long()

    return x_solution + y_solution + z_solution


def main():
    print(f'Advent of Code 2023 --- Day {DAY} --- Part {PART}')

    lines = data.splitlines()
    result = solve(lines)

    print(f'{str(result)}')


if __name__ == '__main__':
    start = timer()
    main()
    print(f"Completed in {timer() - start} sec")
