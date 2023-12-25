import re
from timeit import default_timer as timer

from aocd import data

DAY = '24'
PART = 'a'


def solve(lines, area_start, area_end):
    hailstones = []
    for line in lines:
        x, y, z, dx, dy, dz = [int(n) for n in re.findall(r'-?\d+', line)]
        m = dy / dx
        b = y - (m * x)
        hailstones.append((x, y, dx, dy, m, b))

    number_of_intersections = 0
    for i1, h1 in enumerate(hailstones):
        for i2, h2 in enumerate(hailstones[i1 + 1:]):
            x1, y1, dx1, dy1, m1, b1 = h1
            x2, y2, dx2, dy2, m2, b2 = h2
            if m1 == m2:  # parallel
                continue
            xs = (b2 - b1) / (m1 - m2)
            ys = m1 * xs + b1
            intersection_is_within_area = area_start <= xs <= area_end and area_start <= ys <= area_end
            is_in_future_h1 = (dx1 >= 0 and xs >= x1 or dx1 < 0 and xs < x1) and (dy1 >= 0 and ys >= y1 or dy1 < 0 and ys < y1)
            is_in_future_h2 = (dx2 >= 0 and xs >= x2 or dx2 < 0 and xs < x2) and (dy2 >= 0 and ys >= y2 or dy2 < 0 and ys < y2)
            if intersection_is_within_area and is_in_future_h1 and is_in_future_h2:
                number_of_intersections += 1

    return number_of_intersections


def main():
    print(f'Advent of Code 2023 --- Day {DAY} --- Part {PART}')

    lines = data.splitlines()
    result = solve(lines, 200000000000000, 400000000000000)

    print(f'{str(result)}')


if __name__ == '__main__':
    start = timer()
    main()
    print(f"Completed in {timer() - start} sec")
