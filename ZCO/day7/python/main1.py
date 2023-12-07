import sys
from typing import Counter, Tuple


def get_value(c: str):
    if c.isdigit():
        return int(c)
    return {
        "A": 14,
        "K": 13,
        "Q": 12,
        "J": 11,
        "T": 10,
    }[c]


def bla(cards: str) -> Tuple[int, str]:
    counter = Counter(cards)
    if len(counter) == 1:
        # five of a kind
        rank = 5
    elif max(counter.values()) == 4:
        # four of a kind
        rank = 4
    elif len(counter) == 2:
        # full house (it was not [4, 1] so it must be [2, 3])
        rank = 3
    elif max(counter.values()) == 3:
        # three of a kind
        rank = 2
    elif len(counter) == 3:
        # two pairs (was not {3, 1, 1} so must be {2, 2, 1})
        rank = 1
    elif max(counter.values()) == 2:
        # one pair
        rank = 0
    else:
        assert (len(counter)) == 5
        rank = -1
    return rank, list(map(get_value, cards))


def main():
    cards_with_bids = list(map(str.split, sys.stdin))
    cards_with_bids.sort(key=lambda x: bla(x[0]))
    s = 0
    for i, (_, bid) in enumerate(cards_with_bids):
        s += (i + 1) * int(bid)
    print(s)


if __name__ == "__main__":
    main()
