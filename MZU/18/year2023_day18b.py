from timeit import default_timer as timer

from aocd import data

DAY = '18'
PART = 'b'


def solve(lines):
    coordinates = [(10000000, 10000000)]  # start and end point
    loop_area = 0
    for line in lines:
        real_instructions = line.split('#')[1][:-1]
        distance = int(real_instructions[:-1], 16)
        loop_area += distance
        direction = int(real_instructions[-1])
        last_x, last_y = coordinates[-1]
        new_x, new_y = last_x, last_y
        if direction == 0:  # right
            new_x += distance
        elif direction == 1:  # down
            new_y -= distance
        elif direction == 2:  # left
            new_x -= distance
        elif direction == 3:  # up
            new_y += distance
        if (new_x, new_y) not in coordinates:
            coordinates.append((new_x, new_y))

    for r, c in coordinates:
        print(f'{r}\t{c}')  # just to easily copy and paste to a google sheets for quick plotting

    coordinates.reverse()  # it is mandatory to traverse the coordinates in counter clockwise direction for shoelace algorithm

    # Shoelace Algorithm
    first_sum, second_sum = 0, 0
    for i in range(len(coordinates) - 1):
        first_sum += coordinates[i][0] * coordinates[i + 1][1]
        second_sum += coordinates[i][1] * coordinates[i + 1][0]
    # wrap around
    first_sum += coordinates[-1][0] * coordinates[0][1]
    second_sum += coordinates[-1][1] * coordinates[0][0]

    inside_area = abs(first_sum - second_sum) / 2
    # this inside area contains a part of the digging loop, because the area ends in the middle of the loop (which is 1m wide).
    # we can use picks theorem to calculate the area of the loop that lies within the calculated area
    inside_area_of_loop = (loop_area / 2) - 1
    # we can then calculate the total area as follows:
    return int(inside_area - inside_area_of_loop + loop_area)


def main():
    print(f'Advent of Code 2023 --- Day {DAY} --- Part {PART}')

    lines = data.splitlines()
    result = solve(lines)

    print(f'{str(result)}')


if __name__ == '__main__':
    start = timer()
    main()
    print(f"Completed in {timer() - start} sec")
