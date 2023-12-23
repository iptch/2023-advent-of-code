import re
from timeit import default_timer as timer

from aocd import data

DAY = '18'
PART = 'a'


def get_new_position(row, col, direction):
    if direction == 'R':
        return row, col + 1
    elif direction == 'D':
        return row + 1, col
    elif direction == 'L':
        return row, col - 1
    elif direction == 'U':
        return row - 1, col


def get_neighbors(row, col, grid):
    neighbors = []
    for r in range(-1, 2, 1):
        for c in range(-1, 2, 1):
            if c != 0 or r != 0:
                neighbors.append((row + r, col + c, grid[row + r][col + c]))
    return neighbors


def mark_inside(grid, row, col):
    still_working = True
    stuck_nodes = set()
    while still_working:
        neighbors = get_neighbors(row, col, grid)
        can_continue = False
        still_working = False
        for r, c, value in neighbors:
            if value == '.':
                n = get_neighbors(r, c, grid)
                if any(nn[2] == '#' for nn in n):
                    grid[r][c] = 'X'
                    row, col = r, c
                    can_continue = True
                    stuck_nodes = set()
                    still_working = True
                    break

        if not can_continue:
            stuck_nodes.add((row, col))
            for n in neighbors:
                if n[2] in 'X.':
                    nn = get_neighbors(n[0], n[1], grid)
                    if any(nnn[2] == '#' for nnn in nn) and any(nnn[2] == '.' for nnn in nn) and (n[0], n[1]) not in stuck_nodes:
                        if n[2] == '.':
                            grid[n[0]][n[1]] = 'X'
                        row, col = n[0], n[1]
                        still_working = True
                        break


def fill_in_loop(loop_list, grid):
    for row_idx in range(len(grid)):
        for col_idx in range(1, len(grid[0]), 1):
            if (row_idx, col_idx) not in loop_list and (grid[row_idx][col_idx - 1] == 'X' or grid[row_idx - 1][col_idx] == 'X'):
                grid[row_idx][col_idx] = 'X'

    for row_idx in range(len(grid) - 2, 0, -1):
        for col_idx in range(len(grid[0]) - 2, 0, -1):
            if (row_idx, col_idx) not in loop_list and (grid[row_idx][col_idx + 1] == 'X' or grid[row_idx + 1][col_idx] == 'X'):
                grid[row_idx][col_idx] = 'X'


def solve(lines):
    grid = [['.' for _ in range(1000)] for _ in range(1000)]
    row = 500
    col = 500
    grid[row][col] = '#'
    loop_list = []
    for line in lines:
        direction = re.findall(r'[A-Z]', line)[0]
        distance = int(re.findall(r'\d+', line)[0])
        for _ in range(distance):
            row, col = get_new_position(row, col, direction)
            grid[row][col] = '#'
            loop_list.append((row, col))

    # mark first block inside manually to indicate the inside, then start marking
    # inside along the loop with 'X'
    row = 501
    col = 501
    grid[row][col] = 'X'
    mark_inside(grid, row, col)

    # after marking the inside it is easy to fill it
    fill_in_loop(loop_list, grid)

    # finally, let's count all X and #
    lagoon_size = 0
    for row in grid:
        lagoon_size += row.count('#') + row.count('X')
    for row in grid:
        print(''.join(row))

    return lagoon_size


def main():
    print(f'Advent of Code 2023 --- Day {DAY} --- Part {PART}')

    lines = data.splitlines()
    result = solve(lines)

    print(f'{str(result)}')


if __name__ == '__main__':
    start = timer()
    main()
    print(f"Completed in {timer() - start} sec")
