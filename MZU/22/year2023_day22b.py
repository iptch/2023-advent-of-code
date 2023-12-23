import copy
import re
from timeit import default_timer as timer

from aocd import data

DAY = '22'
PART = 'b'


def solve(lines):
    bricks = []
    for line in lines:
        x1, y1, z1, x2, y2, z2 = [int(n) for n in re.findall(r'\d+', line)]
        bricks.append([(x1, y1, z1), (x2, y2, z2), '1'])

    bricks = sorted(bricks, key=lambda n: min(n[0][2], n[1][2]))
    pile_max_height = 350
    pile = [[['.' for x in range(10)] for y in range(10)] for z in range(pile_max_height)]
    letters = list('ABCDEFGHIJKLMNOPQRSTUVWXYZ')
    for idx, enriched_brick in enumerate(bricks):
        s, e, _ = enriched_brick
        x1, y1, z1 = s
        x2, y2, z2 = e
        x_values = range(x1, x2 + 1, 1)
        y_values = range(y1, y2 + 1, 1)
        z_values = range(z1, z2 + 1, 1)

        first_free_z = 1
        for x in x_values:
            for y in y_values:
                last_occupied_brick = 0
                for z in range(1, pile_max_height, 1):
                    if pile[z][y][x] != '.':
                        last_occupied_brick = z
                first_free_z = max(first_free_z, last_occupied_brick + 1)

        l = letters[0]
        del letters[0]
        letters.append(l)
        bricks[idx][2] = l

        bricks[idx][0] = (x1, y1, first_free_z)
        bricks[idx][1] = (x2, y2, first_free_z + (z2 - z1))
        for x in x_values:
            for y in y_values:
                for z in z_values:
                    pile[first_free_z + (z - min(z_values))][y][x] = l

    enriched_bricks = copy.deepcopy(bricks)
    for idx, brick in enumerate(bricks):
        s, e, _ = brick
        x1, y1, z1 = s
        x2, y2, z2 = e
        supporting = set()
        supported_by = set()
        for o_idx, o_b in enumerate(bricks):
            o_s, o_e, _ = o_b
            o_x1, o_y1, o_z1 = o_s
            o_x2, o_y2, o_z2 = o_e
            for x in range(x1, x2 + 1, 1):
                for y in range(y1, y2 + 1, 1):
                    # for each brick, find out by which bricks it is supported by:
                    # for each x and y, check if there is another brick at the min z value - 1
                    if o_x1 <= x <= o_x2 and o_y1 <= y <= o_y2 and z1 - 1 == o_z2:
                        supported_by.add(o_idx)
                    # for each brick, find out which bricks it supports:
                    # for each x and y, check if there is another brick at the max z value + 1
                    if o_x1 <= x <= o_x2 and o_y1 <= y <= o_y2 and z2 + 1 == o_z1:
                        supporting.add(o_idx)
        enriched_bricks[idx].append(supporting)
        enriched_bricks[idx].append(supported_by)

    total_fallen_bricks = 0
    for idx, brick in enumerate(enriched_bricks):
        brick.append(idx)
    max_brick_height = max(b[1][2] - b[0][2] for b in enriched_bricks)

    for idx, brick in enumerate(enriched_bricks):
        fallen_indices = set()
        fallen_indices.add(idx)
        start_height = brick[1][2] + 1
        nothing_happened_since = start_height
        for z in range(start_height, pile_max_height, 1):
            bricks_starting_here = [b for b in enriched_bricks if b[0][2] == z]
            something_happened = False
            for o_brick in bricks_starting_here:
                if all(s_idx in fallen_indices for s_idx in o_brick[4]):
                    fallen_indices.add(o_brick[5])
                    something_happened = True
            if something_happened:
                nothing_happened_since = z
            if z - nothing_happened_since > max_brick_height:
                break
        total_fallen_bricks += len(fallen_indices) - 1

    return total_fallen_bricks


def main():
    print(f'Advent of Code 2023 --- Day {DAY} --- Part {PART}')

    lines = data.splitlines()
    result = solve(lines)

    print(f'{str(result)}')


if __name__ == '__main__':
    start = timer()
    main()
    print(f"Completed in {timer() - start} sec")
