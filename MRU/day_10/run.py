def get_lines_from_file(filename="input.txt"):
    lines = []
    with open(filename, 'r') as file:
        line = file.readline()
        while line:
            lines.append(line.strip())
            line = file.readline()
    return lines


def get_pos(c, values):
    pos = []
    for i, p in enumerate(values):
        if p == c:
            pos.append(i)

    return pos


def parse(lines):
    grid = []
    points = []
    y = 0
    for x, line in enumerate(lines):
        xs = [c for c in line]
        grid.append(xs)
        found_start = get_pos('S', xs)
        if found_start:
            points.extend([(x_found, y) for x_found in found_start])
        y += 1
    return points, grid


def get_mapping(c):
    op_fw = (1, 0)
    op_bw = (-1, 0)
    op_uw = (0, -1)
    op_dw = (0, 1)

    fw = ['-', '7', 'J', 'S']
    bw = ['-', 'F', 'L', 'S']
    dw = ['|', 'L', 'J', 'S']
    uw = ['|', 'F', '7', 'S']

    mapping = {
        '-': {
            op_fw: fw,
            op_bw: bw
        },
        '|': {
            op_uw: uw,
            op_dw: dw
        },
        'F': {
            op_fw: fw,
            op_dw: dw
        },
        '7': {
            op_bw: bw,
            op_dw: dw
        },
        'L': {
            op_fw: fw,
            op_uw: uw
        },
        'J': {
            op_uw: uw,
            op_bw: bw
        },
        'S': {
            op_fw: fw,
            op_bw: bw,
            op_dw: dw,
            op_uw: uw
        }
    }
    return mapping[c]


def get_start_points(start_points):
    for p in start_points:
        yield p[0], p[1]


def get_value(point, grid):
    x = point[0]
    y = point[1]
    return grid[y][x]


def get_maxs(grid):
    return len(grid[0]) - 1, len(grid) - 1


def is_in_grid(point, grid):
    x_max, y_max = get_maxs(grid)
    x = point[0]
    y = point[1]
    return 0 <= x <= x_max and 0 <= y <= y_max


def get_next_points(x, y, grid):
    ps = [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]
    ps = list(filter(lambda p: is_in_grid(p, grid), ps))
    return ps


def shift_point(p1, p2):
    return p1[0] + p2[0], p1[1] + p2[1]


def get_next_moves(point, grid):
    next_moves = []

    x = point[0]
    y = point[1]
    ps = get_next_points(x, y, grid)
    current_value = get_value((x, y), grid)
    rules = get_mapping(current_value)
    # print(f"next moves for x: {x}, y: {y}, next_points: {ps}")

    for r in rules:
        # print("check", r, p, shift_point(p, r))
        n_pos = shift_point((x, y), r)
        if is_in_grid(n_pos, grid):
            allowed_values = rules[r]
            nex_val = get_value(n_pos, grid)
            # print(f"n_pos: {n_pos}, allowed: {allowed_values}, next_val: {nex_val}")
            if nex_val in allowed_values:
                # print(f"n_pos: {n_pos}, allowed: {allowed_values}, next_val: {nex_val}")
                next_moves.append(n_pos)

    return next_moves


def get_crossing(values):
    count = 0
    for i, v in enumerate(values):
        if i + 1 < len(values):
            if values[i + 1] - v != 1:
                count += 1
    return count


if __name__ == '__main__':
    start_points, grid = parse(get_lines_from_file(filename="input.txt"))
    start_point = next(get_start_points(start_points))

    token = None
    current_point = start_point
    next_point = None
    visited = set()
    while True:
        visited.add(current_point)
        next_points = get_next_moves(current_point, grid)

        finished = True
        for p in next_points:
            if p not in visited:
                next_point = p
                token = get_value(next_point, grid)
                current_point = next_point
                finished = False
                break

        if finished:
            break

    print(len(visited))
    print("part 1", len(visited) / 2)

    # ray casting algorithm
    count_inside = 0
    for y, row in enumerate(grid):
        for x, e in enumerate(row):
            if (x, y) not in visited:
                crossing_boundaries = ""
                for i in range(0, len(row)):
                    if (i, y) in visited:
                        crossing_boundaries += get_value((i, y), grid)
                    if (i, y) == (x, y):

                        # ignoring S seems to work
                        crossing_boundaries = crossing_boundaries.replace("-", "")
                        crossing_boundaries = crossing_boundaries.replace("L7", '|')
                        crossing_boundaries = crossing_boundaries.replace("FJ", '|')
                        crossing_boundaries = crossing_boundaries.replace("LJ", '||')
                        crossing_boundaries = crossing_boundaries.replace("F7", '||')
                        n = crossing_boundaries.count("|")

                        if n % 2 != 0:
                            count_inside += 1
                        break

    print("part 2", count_inside)
