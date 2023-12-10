import re
from timeit import default_timer as timer

from aocd import data

DAY = '09'
PART = 'b'


def solve(lines):
    differences = [[[int(number) for number in re.findall(r'[-\d]+', line)]] for line in lines]
    for idx in range(len(differences)):
        depth = 0
        while not all(number == 0 for number in differences[idx][depth]):
            differences[idx].append([])
            for i in range(len(differences[idx][depth]) - 1):
                differences[idx][depth + 1].append(differences[idx][depth][i + 1] - differences[idx][depth][i])
            depth = depth + 1

    extrapolations = []
    for sequence in differences:
        sequence[-1].insert(0, 0)
        for depth in range(len(sequence) - 2, -1, -1):
            sequence[depth].insert(0, sequence[depth][0] - sequence[depth + 1][0])
        extrapolations.append(sequence[0][0])

    return sum(extrapolations)


def main():
    print(f'Advent of Code 2023 --- Day {DAY} --- Part {PART}')

    lines = data.splitlines()
    result = solve(lines)

    print(f'{str(result)}')


if __name__ == '__main__':
    start = timer()
    main()
    print(f"Completed in {timer() - start} sec")
