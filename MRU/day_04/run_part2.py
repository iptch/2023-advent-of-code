import re


def get_lines_from_file(filename="input.txt"):
    lines = []
    with open(filename, 'r') as file:
        line = file.readline()
        while line:
            lines.append(line.strip())
            line = file.readline()
    return lines


def prepare_tree(lines):
    result = {1: []}
    card_n = 1
    for line in lines:
        result[card_n] = get_next_cards(line, card_n)
        card_n += 1
    return result


def get_numbers(text):
    return re.findall(r"\d+", text)


def traverse_tree_count(tree, current_card, counter):
    result = counter
    for card in tree[current_card]:
        result += traverse_tree_count(tree, card, 1)
    return result


def get_next_cards(line, card_n):
    parts = line.split(":")
    w, n = parts[1].split("|")
    n_copies = len(set(get_numbers(w)).intersection(set(get_numbers(n))))
    next_cards = []
    for i in range(0, n_copies):
        next_cards.append(card_n + i + 1)
    return next_cards


if __name__ == '__main__':
    lines = get_lines_from_file(filename='input.txt')
    tree = prepare_tree(lines)

    total = 0
    for card in tree.keys():
        total += traverse_tree_count(tree, card, 1)

    print(total)
