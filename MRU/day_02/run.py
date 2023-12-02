import sys


def process(function, filename="input.txt"):
    total = 0
    with open(filename, 'r') as file:
        line = file.readline()
        while line:
            line = line.strip()
            n = function(line)
            total = total + n
            line = file.readline()
    return total


def total_cubes(game_set):
    current_counts = {'blue': 0, 'green': 0, 'red': 0}
    for subset in game_set:
        for s in subset:
            current_counts[s[0]] += s[1]
    return current_counts


def min_cubes(game_set):
    current_counts = {'red': -1, 'green': -1, 'blue': -1}
    for subset in game_set:
        for s in subset:
            if current_counts[s[0]] < s[1]:
                current_counts[s[0]] = s[1]
    return current_counts


def is_possible(game_set, target_counts):
    for subset in game_set:
        current_counts = {color: 0 for color in target_counts}
        for s in subset:
            current_counts[s[0]] += s[1]
        possible_set = all(current_counts[color] <= target_counts[color] for color in target_counts)
        if not possible_set:
            return False

    return True


def to_game_sets(line):
    subset = line.split(':')
    id = int(subset[0].split(' ')[1])
    sets = [subset_to_tuple(e) for e in [b.strip().split(',') for b in subset[1].split(';')]]
    # [[('green', 1), ('red', 3), ('blue', 6)], [('green', 3), ('red', 6)], [('green', 3), ('blue', 15), ('red', 14)]]
    return id, sets


def subset_to_tuple(value):
    # ['6 red', ' 1 blue', ' 3 green']
    return [(x.strip().split(' ')[1], int(x.strip().split(' ')[0])) for x in value]


def part1(line):
    target_counts = {'red': 12, 'green': 13, 'blue': 14}

    total = 0

    # Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
    id, game_sets = to_game_sets(line)

    # print(is_possible(game_sets, target_counts), id, game_sets)
    if is_possible(game_sets, target_counts):
        total += id
    return total


def part2(line):
    id, game_sets = to_game_sets(line)
    total = 1
    for k, v in min_cubes(game_sets).items():
        total *= v

    return total


if __name__ == '__main__':
    t1 = process(part1, 'input.txt')
    print(f"total 1: {t1}")

    t2 = process(part2, 'input.txt')
    print(f"total 1: {t2}")
