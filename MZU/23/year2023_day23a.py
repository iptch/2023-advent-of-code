import copy
from heapq import heappop, heappush
from timeit import default_timer as timer

from aocd import data

DAY = '23'
PART = 'a'


def get_neighbors(row_idx, col_idx, island_map):
    if island_map[row_idx][col_idx] == '^':
        return [(row_idx - 1, col_idx)]
    elif island_map[row_idx][col_idx] == '>':
        return [(row_idx, col_idx + 1)]
    elif island_map[row_idx][col_idx] == 'v':
        return [(row_idx + 1, col_idx)]
    elif island_map[row_idx][col_idx] == '<':
        return [(row_idx, col_idx - 1)]
    else:
        all_neighbors = [(row_idx + 1, col_idx), (row_idx, col_idx + 1), (row_idx - 1, col_idx), (row_idx, col_idx - 1)]
        valid_neighbors = [n for n in all_neighbors if island_map[n[0]][n[1]] != '#']
        return valid_neighbors


def find_longest_hike(island_map):
    unvisited_nodes = [(0, 0, 1, [(0, 1)])]
    # visited_nodes = set()
    max_row = len(island_map) - 1
    max_col = len(island_map[0]) - 1
    longest_path_length = 0
    longest_path = None

    while unvisited_nodes:
        # find next node in priority queue (the one with the lowest heat loss)
        current_path_length, current_row_idx, current_col_idx, current_path = heappop(unvisited_nodes)
        # because the priority queue impl. always optimizes for the smallest element,
        # we simply make our target value negative
        current_path_length = abs(current_path_length)

        if current_row_idx == max_row and current_col_idx == max_col - 1:
            if current_path_length > longest_path_length:
                longest_path_length = current_path_length
                longest_path = current_path
            continue

        for new_row_idx, new_col_idx in get_neighbors(current_row_idx, current_col_idx, island_map):
            if (new_row_idx, new_col_idx) not in current_path:
                new_path_length = current_path_length + 1
                new_path = copy.deepcopy(current_path)
                new_path.append((new_row_idx, new_col_idx))
                heappush(unvisited_nodes, (-new_path_length, new_row_idx, new_col_idx, new_path))

    return longest_path_length, longest_path


def solve(lines):
    island_map = [[tile for tile in row] for row in lines]
    path_length, path = find_longest_hike(island_map)
    for r, c in path:
        island_map[r][c] = '0'
    for row in island_map:
        print(''.join(str(row)))
    return path_length


def main():
    print(f'Advent of Code 2023 --- Day {DAY} --- Part {PART}')

    lines = data.splitlines()
    result = solve(lines)

    print(f'{str(result)}')


if __name__ == '__main__':
    start = timer()
    main()
    print(f"Completed in {timer() - start} sec")
