import functools
from timeit import default_timer as timer

from aocd import data

DAY = '07'
PART = 'a'

CARD_VALUES = {
    'A': 1,
    'K': 2,
    'Q': 3,
    'J': 4,
    'T': 5,
    '9': 6,
    '8': 7,
    '7': 8,
    '6': 9,
    '5': 10,
    '4': 11,
    '3': 12,
    '2': 13
}


def is_five_of_a_kind(hand):
    return hand[0] == hand[1] == hand[2] == hand[3] == hand[4]


def is_four_of_a_kind(hand):
    return any(hand.count(card) == 4 for card in hand)


def is_full_house(hand):
    return len(set(hand)) == 2


def is_three_of_a_kind(hand):
    return any(hand.count(card) == 3 for card in hand)


def is_two_pair(hand):
    return len(set(hand)) == 3


def is_one_pair(hand):
    return len(set(hand)) == 4


def get_type(hand):
    if is_five_of_a_kind(hand):
        return 1
    elif is_four_of_a_kind(hand):
        return 2
    elif is_full_house(hand):
        return 3
    elif is_three_of_a_kind(hand):
        return 4
    elif is_two_pair(hand):
        return 5
    elif is_one_pair(hand):
        return 6
    else:
        return 7


def compare_hands(a, b):
    a, b = a[0], b[0]
    if get_type(a) < get_type(b):
        return -1
    elif get_type(a) > get_type(b):
        return 1
    else:
        for la, lb in zip(a, b):
            if CARD_VALUES[la] < CARD_VALUES[lb]:
                return -1
            elif CARD_VALUES[la] > CARD_VALUES[lb]:
                return 1
    return 0


def solve(lines):
    hands = [line.split(' ') for line in lines]

    sorted_hands = sorted(hands, key=functools.cmp_to_key(compare_hands), reverse=True)
    winnings = []
    for idx, hand in enumerate(sorted_hands):
        rank = idx + 1
        winnings.append(rank * int(hand[1]))

    return sum(winnings)


def main():
    print(f'Advent of Code 2023 --- Day {DAY} --- Part {PART}')

    lines = data.splitlines()
    result = solve(lines)

    print(f'{str(result)}')


if __name__ == '__main__':
    start = timer()
    main()
    print(f"Completed in {timer() - start} sec")
