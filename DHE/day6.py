import re
import numpy as np
from timeit import default_timer as timer

INPUT_STRING = """Time:        48     93     85     95
Distance:   296   1928   1236   1391"""


class Parser:
    times = None
    distances = None

    def __init__(self, input_string):
        input_lines = input_string.splitlines()
        self.times = re.findall(r'\d+', input_lines[0])
        self.distances = re.findall(r'\d+', input_lines[1])

    def parse_input_for_a(self):
        return np.array(self.times, dtype=float), np.array(self.distances, dtype=float)

    def parse_input_for_b(self):
        return np.array(''.join(self.times), dtype=float), np.array(''.join(self.distances), dtype=float)


def solve(times, distances):
    discriminant = times ** 2 - 4 * distances
    if np.any(discriminant <= 0):
        return 0
    sqrt_discriminant = np.sqrt(discriminant)

    t1 = 0.5 * times - 0.5 * sqrt_discriminant
    t2 = 0.5 * times + 0.5 * sqrt_discriminant

    min_time_exclusive = np.floor(t1) + np.equal((t1 - np.floor(t1)), np.zeros_like(t1))
    max_time_inclusive = np.floor(t2)

    return int(np.prod(max_time_inclusive - min_time_exclusive))


if __name__ == '__main__':
    parser = Parser(INPUT_STRING)

    # --- part 1 ---
    start1 = timer()
    times_a, distances_a = parser.parse_input_for_a()
    print(f"Puzzle 1: {solve(times_a, distances_a)} (in {(timer() - start1) * 1000} ms)")

    # --- part 2 ---
    start2 = timer()
    times_b, distances_b = parser.parse_input_for_b()
    print(f"Puzzle 2: {solve(times_b, distances_b)} (in {(timer() - start2) * 1000} ms)")
