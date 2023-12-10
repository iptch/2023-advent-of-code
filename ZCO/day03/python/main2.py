from collections import defaultdict
import pprint
import sys


def iter_gear_ratios(lines: list[str]):
    def get_char(i: int, j: int):
        if 0 <= i < len(lines) and 0 <= j < len(lines[i]):
            return lines[i][j]
        return "."

    gears = defaultdict(list)

    for i, line in enumerate(lines):
        current_digits = []
        current_area = set()
        for j, c in enumerate(line):
            if c.isdigit():
                current_digits.append(c)
                current_area.update(
                    [
                        (i - 1, j - 1),
                        (i - 1, j),
                        (i - 1, j + 1),
                        (i, j - 1),
                        (i, j - 1),
                        (i, j + 1),
                        (i + 1, j - 1),
                        (i + 1, j),
                        (i + 1, j + 1),
                    ]
                )
            else:
                if current_digits:
                    for k in current_area:
                        if get_char(k[0], k[1]) == "*":
                            gears[k].append(int("".join(current_digits)))
                current_digits.clear()
                current_area.clear()
        if current_digits:
            for k in current_area:
                if get_char(k[0], k[1]) == "*":
                    gears[k].append(int("".join(current_digits)))

    for gear in gears.values():
        if len(gear) == 2:
            yield gear[0] * gear[1]


def main():
    lines = sys.stdin.read().splitlines()
    print(sum(iter_gear_ratios(lines)))


if __name__ == "__main__":
    main()
