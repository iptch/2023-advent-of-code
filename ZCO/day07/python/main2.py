import sys
from typing import Counter, Iterable


def get_joker_combinations(hand: str) -> Iterable[str]:
    if "J" not in hand:
        yield hand
        return
    if hand == "JJJJJ":
        yield "AAAAA"
        return
    # if I'm not mistaken, it will always be most valuable to map all the jokers in the hand to one same existing value from that hand
    # with 1 joker trivial
    # with 2 jokers
    #  - and 3 different cards: best solution is three of a kind
    #  - and 2 distinct cards: best solution is three of a kind
    # with 3 jokers you always want the same, as you'll get either 4 of a kind
    # with 4 jokers you always want the same to get five of a kind
    non_jokers = set(filter(lambda c: c != "J", hand))
    for c in non_jokers:
        yield hand.replace("J", c)


def get_card_value(c: str) -> int:
    if c.isdigit():
        return int(c)
    return {
        "A": 14,
        "K": 13,
        "Q": 12,
        "J": 1,
        "T": 10,
    }[c]


def get_hand_value(cards: str) -> int:
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
    return rank


def get_rank(hand: str):
    return max(map(get_hand_value, get_joker_combinations(hand))), list(
        map(get_card_value, hand)
    )


def main():
    cards_with_bids = list(map(str.split, sys.stdin))
    cards_with_bids.sort(key=lambda x: get_rank(x[0]))
    s = 0
    for i, (_, bid) in enumerate(cards_with_bids):
        s += (i + 1) * int(bid)
    print(s)


if __name__ == "__main__":
    main()
