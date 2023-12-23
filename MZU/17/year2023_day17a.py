import copy
from heapq import heappop, heappush
from timeit import default_timer as timer

from aocd import data

DAY = '17'
PART = 'a'


def get_new_indexes(row_idx, col_idx, direction):
    if direction == 0:  # d
        return row_idx + 1, col_idx
    elif direction == 1:  # r
        return row_idx, col_idx + 1
    elif direction == 2:  # u
        return row_idx - 1, col_idx
    elif direction == 3:  # l
        return row_idx, col_idx - 1


def find_optimal_heat_loss(heat_loss_map):
    unvisited_nodes = [(0, 0, 0, 0, 0, [(0, 0)])]
    visited_nodes = set()
    max_row = len(heat_loss_map) - 1
    max_col = len(heat_loss_map[0]) - 1

    while unvisited_nodes:
        # find next node in priority queue (the one with the lowest heat loss)
        current_heat_loss, current_row_idx, current_col_idx, current_direction, current_steps, current_path = heappop(unvisited_nodes)

        if (current_row_idx, current_col_idx, current_direction, current_steps) in visited_nodes:
            continue

        visited_nodes.add((current_row_idx, current_col_idx, current_direction, current_steps))

        if current_row_idx == max_row and current_col_idx == max_col:
            return current_heat_loss, current_path  # we are at the end

        for new_direction in range(4):
            if current_direction != new_direction:
                if (new_direction in [0, 2] and current_direction in [0, 2]) or (new_direction in [1, 3] and current_direction in [1, 3]):
                    continue
                new_steps = 1
            else:
                if current_steps < 3:
                    new_steps = current_steps + 1
                else:
                    continue

            new_row_idx, new_col_idx = get_new_indexes(current_row_idx, current_col_idx, new_direction)
            if (new_row_idx, new_col_idx, new_direction) not in visited_nodes:
                if 0 <= new_row_idx <= max_row and 0 <= new_col_idx <= max_col:
                    new_heat_loss = current_heat_loss + heat_loss_map[new_row_idx][new_col_idx]
                    new_path = copy.deepcopy(current_path)
                    new_path.append((new_row_idx, new_col_idx))
                    heappush(unvisited_nodes, (new_heat_loss, new_row_idx, new_col_idx, new_direction, new_steps, new_path))


def solve(lines):
    heat_loss_map = [[int(heat_loss) for heat_loss in row] for row in lines]
    heat_loss, path = find_optimal_heat_loss(heat_loss_map)
    for r, c in path:
        heat_loss_map[r][c] = 0
    for row in heat_loss_map:
        print(''.join(str(row)))
    return heat_loss


def main():
    print(f'Advent of Code 2023 --- Day {DAY} --- Part {PART}')

    lines = data.splitlines()
    result = solve(lines)

    print(f'{str(result)}')


if __name__ == '__main__':
    start = timer()
    main()
    print(f"Completed in {timer() - start} sec")
