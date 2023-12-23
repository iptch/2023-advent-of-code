from timeit import default_timer as timer

from aocd import data

DAY = '21'
PART = 'b'


def get_neighbors(grid, max_row, max_col, mx, my, row_idx, col_idx):
    neighbors = [(row_idx + 1, col_idx), (row_idx - 1, col_idx), (row_idx, col_idx - 1), (row_idx, col_idx + 1)]
    mapped_neighbors = []
    for r, c in neighbors:
        x, y = mx, my
        if r < 0:
            y -= 1
            r = max_row
        elif r > max_row:
            y += 1
            r = 0
        elif c < 0:
            x -= 1
            c = max_col
        elif c > max_col:
            x += 1
            c = 0
        mapped_neighbors.append((x, y, r, c))
    valid_neighbors = [n for n in mapped_neighbors if grid[n[2]][n[3]] != '#']

    return valid_neighbors


def solve(lines, steps):
    grid = [[tile for tile in row] for row in lines]
    possible_positions = set()
    max_row = len(grid) - 1
    max_col = len(grid[0]) - 1
    for row_idx, r in enumerate(grid):
        for col_index, c in enumerate(r):
            if c == 'S':
                possible_positions.add((0, 0, row_idx, col_index))

    for _ in range(steps):
        new_positions = set()
        for mx, my, r, c in possible_positions:
            neighbors = get_neighbors(grid, max_row, max_col, mx, my, r, c)
            for n in neighbors:
                new_positions.add(n)
        possible_positions = new_positions
        print(len(possible_positions))

    return len(possible_positions)


def main():
    print(f'Advent of Code 2023 --- Day {DAY} --- Part {PART}')

    lines = data.splitlines()
    result = solve(lines, 1000)

    print(f'{str(result)}')


if __name__ == '__main__':
    start = timer()
    main()
    print(f"Completed in {timer() - start} sec")
