from collections import Counter


def get_lines_from_file(filename="input.txt"):
    lines = []
    with open(filename, 'r') as file:
        line = file.readline()
        while line:
            lines.append(line.strip())
            line = file.readline()
    return lines


def parse(lines):
    r = []
    for line in lines:
        hand = line.split(" ")[0]
        bid = int(line.split(" ")[1])
        r.append((hand, bid))
    return r


def has_joker(hand):
    return "J" in hand


def count_joker(hand):
    if has_joker(hand):
        counter = Counter(hand)
        return counter["J"]
    else:
        return 0


def strength(hand: str, joker=False):
    if joker:
        mapping = "J23456789TQKA"
        return map_hand_to_key_with_joker(hand, mapping)
    else:
        mapping = "23456789TJQKA"
        return map_hand_to_key(hand, mapping)


def map_hand_to_key(hand: str, mapping: str):
    index = [mapping.find(x) for x in hand]

    counter = Counter(hand)
    s = sorted(counter.values())

    if s == [5]:
        index.insert(0, 10)
        return index
    elif s == [1, 4]:
        index.insert(0, 9)
        return index
    elif s == [2, 3]:
        index.insert(0, 8)
        return index
    elif s == [1, 1, 3]:
        index.insert(0, 7)
        return index
    elif s == [1, 2, 2]:
        index.insert(0, 6)
        return index
    elif s == [1, 1, 1, 2]:
        index.insert(0, 5)
        return index
    else:
        index.insert(0, 4)
        return index


def joker_shift(s, js):
    # the ugly way
    if js == 4:
        return [5]
    if js == 3 and s == [1, 1, 3]:
        return [1, 4]
    if js == 3 and s == [2, 3]:
        return [5]
    if js == 2 and s == [1, 1, 1, 2]:
        return [1, 1, 3]
    if js == 2 and s == [1, 2, 2]:
        return [1, 4]
    if js == 2 and s == [1, 1, 1, 2]:
        return [1, 1, 1, 3]
    if js == 2 and s == [1, 2, 2]:
        return [1, 4]
    if js == 2 and s == [2, 3]:
        return [5]
    if js == 1:
        s[-1] = s[-1] + 1
        del s[0]
        return s
    return s


def map_hand_to_key_with_joker(hand: str, mapping: str):
    index = [mapping.find(x) for x in hand]

    counter = Counter(hand)
    js = count_joker(hand)

    s = joker_shift(sorted(counter.values()), js)

    if s == [5]:
        index.insert(0, 10)
        return index
    elif s == [1, 4]:
        index.insert(0, 9)
        return index
    elif s == [2, 3]:
        index.insert(0, 8)
        return index
    elif s == [1, 1, 3]:
        index.insert(0, 7)
        return index
    elif s == [1, 2, 2]:
        index.insert(0, 6)
        return index
    elif s == [1, 1, 1, 2]:
        index.insert(0, 5)
        return index
    else:
        index.insert(0, 4)
        return index


def sum_up(data, joker=False):
    winnings = []
    for i, h in enumerate(sorted(data, key=lambda x: strength(x[0], joker))):
        winnings.append((i + 1) * h[1])
        # print(i + 1, h[0], h[1], strength(h[0], joker), count_joker(h[0]))
    return sum(winnings)


def test_joker(hand, expected):
    s = strength(hand, joker=True)
    assert s == expected, f"s:{s}, h: {hand}"


if __name__ == '__main__':
    data = parse(get_lines_from_file('input.txt'))

    # first index:
    #   Five of a kind -> 10
    #   Four of a kind -> 9
    #   full house -> 8
    #   Three of a kind -> 7
    #   Two pair -> 6
    #   One pair -> 5
    #   High card -> 4

    # k[0] = bucket (five of kind, etc.), k[1:5] = card value

    print("PART 1", sum_up(data, joker=False))

    test_joker("23456", [4, 1, 2, 3, 4, 5])
    test_joker("JJJJJ", [10, 0, 0, 0, 0, 0])
    test_joker("JJJJ2", [10, 0, 0, 0, 0, 1])
    test_joker("JJJ23", [9, 0, 0, 0, 1, 2])
    test_joker("JJJ22", [10, 0, 0, 0, 1, 1])
    test_joker("JJ234", [7, 0, 0, 1, 2, 3])
    test_joker("JJ223", [9, 0, 0, 1, 1, 2])
    test_joker("JJ222", [10, 0, 0, 1, 1, 1])
    test_joker("J2345", [5, 0, 1, 2, 3, 4])
    test_joker("J2234", [7, 0, 1, 1, 2, 3])
    test_joker("J2224", [9, 0, 1, 1, 1, 3])
    test_joker("J2244", [8, 0, 1, 1, 3, 3])

    print("PART 2", sum_up(data, joker=True))
