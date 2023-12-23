import copy
import functools
from heapq import heappush, heappop
from timeit import default_timer as timer

from aocd import data

DAY = '23'
PART = 'b'


@functools.cache
def get_neighbors(row_idx, col_idx, island_map):
    all_neighbors = [(row_idx + 1, col_idx), (row_idx, col_idx + 1), (row_idx - 1, col_idx), (row_idx, col_idx - 1)]
    valid_neighbors = [n for n in all_neighbors if 0 <= n[0] <= len(island_map) - 1 and 0 <= n[1] <= len(island_map[0]) - 1 and island_map[n[0]][n[1]]]
    return valid_neighbors


@functools.cache
def fast_forward_until_crossing(l_row, l_col, row, col, distance, island_map):
    neighbors = [n for n in get_neighbors(row, col, island_map) if n != (l_row, l_col)]
    while len(neighbors) == 1:
        l_row, l_col = row, col
        row, col = neighbors[0][0], neighbors[0][1]
        distance += 1
        neighbors = [n for n in get_neighbors(row, col, island_map) if n != (l_row, l_col)]
    return row, col, distance


def find_longest_hike(island_graph, island_map):
    path = set()
    path.add((0, 1))
    unvisited_nodes = [(0, 0, 1, path)]
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
                print(f'found currently longest path: {longest_path_length}')
            continue

        for new_row_idx, new_col_idx, distance in island_graph[(current_row_idx, current_col_idx)]:
            if (new_row_idx, new_col_idx) not in current_path:
                new_path_length = current_path_length + distance
                new_path = copy.deepcopy(current_path)
                new_path.add((new_row_idx, new_col_idx))
                heappush(unvisited_nodes, (-new_path_length, new_row_idx, new_col_idx, new_path))

    return longest_path_length, longest_path


def construct_graph(row, col, island_graph, island_map):
    neighbors = get_neighbors(row, col, island_map)
    for n in neighbors:
        n_row, n_col, distance = fast_forward_until_crossing(row, col, n[0], n[1], 1, island_map)
        if (row, col) not in island_graph:
            island_graph[(row, col)] = [(n_row, n_col, distance)]
        else:
            island_graph[(row, col)].append((n_row, n_col, distance))
        if (n_row, n_col) not in island_graph:
            construct_graph(n_row, n_col, island_graph, island_map)


def solve(lines):
    island_map = tuple([tuple([tile != '#' for tile in row]) for row in lines])
    island_graph = {}  # key: (row, col),  value: [ (neighbor_row, neighbor_col, distance_to_neighbor) ]
    construct_graph(0, 1, island_graph, island_map)
    path_length, path = find_longest_hike(island_graph, island_map)
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
