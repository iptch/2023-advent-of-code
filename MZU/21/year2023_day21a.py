from timeit import default_timer as timer

from aocd import data

DAY = '21'
PART = 'a'


def get_neighbors(grid, max_row, max_col, row_idx, col_idx):
    neighbors = [(row_idx + 1, col_idx), (row_idx - 1, col_idx), (row_idx, col_idx - 1), (row_idx, col_idx + 1)]
    valid_neighbors = [n for n in neighbors if 0 <= n[0] <= max_row and 0 <= n[1] <= max_col and grid[n[0]][n[1]] != '#']
    return valid_neighbors


def solve(lines, steps):
    grid = [[tile for tile in row] for row in lines]
    possible_positions = set()
    max_row = len(grid) - 1
    max_col = len(grid[0]) - 1
    for row_idx, r in enumerate(grid):
        for col_index, c in enumerate(r):
            if c == 'S':
                possible_positions.add((row_idx, col_index))

    for _ in range(steps):
        new_positions = set()
        for r, c in possible_positions:
            neighbors = get_neighbors(grid, max_row, max_col, r, c)
            for n in neighbors:
                new_positions.add(n)
        possible_positions = new_positions

    return len(possible_positions)


def main():
    print(f'Advent of Code 2023 --- Day {DAY} --- Part {PART}')

    lines = data.splitlines()
    result = solve(lines, 64)

    print(f'{str(result)}')


if __name__ == '__main__':
    start = timer()
    main()
    print(f"Completed in {timer() - start} sec")
