from __future__ import annotations
from timeit import default_timer as timer


class Parser:
    hand_strings = None
    bids = None

    def __init__(self, day: int):
        input_file = open(f"input_{day}.txt", 'r')
        input_lines = input_file.readlines()
        self.hand_strings = [line.strip().split(' ')[0] for line in input_lines]
        self.bids = [int(line.split(' ')[1]) for line in input_lines]

    def get_hand_bid_pairings(self, game_flavor: int) -> list:
        return [(Hand(self.hand_strings[i], game_flavor), self.bids[i]) for i in range(len(self.bids))]


class Hand:
    cards = None
    game_flavor = None

    def __init__(self, card_string: str, game_flavor: int) -> None:
        self.cards = []
        if len(card_string) != 5:
            raise Exception("Invalid number of cards in hand")
        if game_flavor != 0 and game_flavor != 1:
            raise Exception(f"Game flavor must be 0 or 1 but is {game_flavor} instead.")
        self.game_flavor = game_flavor
        for c in card_string:
            self.cards.append(Card(c, game_flavor))

    def __eq__(self, other: Hand) -> bool:
        for i in range(5):
            if self.cards[i] != other.cards[i]:
                return False
        return True

    def __lt__(self, other: Hand) -> bool:
        self_signature = self._get_score_signature()
        other_signature = other._get_score_signature()
        for i in range(min(len(self_signature), len(other_signature))):
            if self_signature[i] != other_signature[i]:
                return self_signature[i] < other_signature[i]

        for i in range(5):
            if self.cards[i] != other.cards[i]:
                return self.cards[i] < other.cards[i]

        return False

    def _get_score_signature(self) -> list:
        counts = {}
        jacks_count = 0
        for card in self.cards:
            if 'J' == card.value and self.game_flavor == 1:
                jacks_count += 1
            elif card.value in counts.keys():
                counts[card.value] += 1
            else:
                counts[card.value] = 1
        score_signature = list(counts.values())
        score_signature.sort(reverse=True)
        if self.game_flavor == 1:
            if (len(score_signature)) > 0:
                score_signature[0] += jacks_count
            else:
                score_signature.append(jacks_count)
        return score_signature


class Card:
    value = None
    game_flavor = None
    orders = [[str(i) for i in range(2, 10)] + ['T', 'J', 'Q', 'K', 'A'],
              ['J'] + [str(i) for i in range(2, 10)] + ['T', 'Q', 'K', 'A']]

    def __init__(self, value: str, game_flavor: int) -> None:
        if game_flavor != 0 and game_flavor != 1:
            raise Exception(f'Game flavor must be 0 or 1 but is {game_flavor} instead')
        self.game_flavor = game_flavor
        if value not in self.orders[self.game_flavor]:
            raise Exception(f'Value {value} not allowed')
        self.value = value

    def __eq__(self, other: Card) -> bool:
        return self.value == other.value

    def __lt__(self, other: Card) -> bool:
        return self._get_rank() < other._get_rank()

    def _get_rank(self) -> int:
        return self.orders[self.game_flavor].index(self.value)


def compute_score(hand_bid_pairings: list) -> int:
    hand_bid_pairings.sort(key=lambda pair: pair[0])

    bids = [pair[1] for pair in hand_bid_pairings]
    results = []

    for i, bid in enumerate(bids):
        results.append(bid * (i+1))

    return sum(results)


if __name__ == '__main__':
    parser = Parser(day=7)

    start1 = timer()
    print(f'Part 1: {compute_score(parser.get_hand_bid_pairings(0))} (in {(timer() - start1) * 1000} ms)')
    start2 = timer()
    print(f'Part 2: {compute_score(parser.get_hand_bid_pairings(1))} (in {(timer() - start2) * 1000} ms)')
