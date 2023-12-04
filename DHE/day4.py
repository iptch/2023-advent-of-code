import numpy as np

INPUT = """Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53
Card 2: 13 32 20 16 61 | 61 30 68 82 17 32 24 19
Card 3:  1 21 53 59 44 | 69 82 63 72 16 21 14  1
Card 4: 41 92 73 84 69 | 59 84 76 51 58  5 54 83
Card 5: 87 83 26 28 32 | 88 30 70 12 93 22 82 36
Card 6: 31 18 13 56 72 | 74 77 10 23 35 67 36 11"""


def parse_input():
    games = []

    for line in INPUT.split("\n"):
        content = line.split(": ")[1]
        winner_string, numbers_string = content.split(" | ")
        numbers = [int(c) for c in numbers_string.split(" ") if c != '']
        winners = [int(w) for w in winner_string.split(" ") if w != '']
        games.append((winners, numbers))

    return games


def compute_wins(game):
    wins = 0
    for number in game[1]:
        wins += number in game[0]
    return wins


def compute_game_score(matches):
    if matches == 0:
        return 0
    else:
        return 2 ** (matches - 1)


def compute_card_amounts(matches_per_game):
    card_amounts = np.array([1 for _ in matches_per_game])

    for i, matches in enumerate(matches_per_game):
        card_amounts[i+1:i+matches+1] += np.ones((card_amounts[i+1:i+matches+1]).shape, dtype=int) * card_amounts[i]

    return card_amounts


if __name__ == '__main__':
    games = parse_input()
    matches_per_game = [compute_wins(game) for game in games]

    # --- part 1 ---
    print(sum([compute_game_score(matches) for matches in matches_per_game]))

    # --- part 2 ---
    print(sum(compute_card_amounts(matches_per_game)))
