import sys


def iter_numbers(lines: list[str]):
    def get_char(i: int, j: int):
        if 0 <= i < len(lines) and 0 <= j < len(lines[i]):
            return lines[i][j]
        return "."

    for i, line in enumerate(lines):
        current_digits = []
        current_is_adjacent = False
        for j, c in enumerate(line):
            if c.isdigit():
                current_digits.append(c)
                surrounding_chars = [
                    get_char(i - 1, j - 1),
                    get_char(i - 1, j),
                    get_char(i - 1, j + 1),
                    get_char(i + 1, j - 1),
                    get_char(i + 1, j),
                    get_char(i + 1, j + 1),
                    get_char(i, j - 1),
                    get_char(i, j + 1),
                ]
                if not all(
                    sc == "." or sc.isdigit() for sc in surrounding_chars
                ):
                    current_is_adjacent = True
            else:
                if current_digits and current_is_adjacent:
                    yield int("".join(current_digits))
                current_digits = []
                current_is_adjacent = False
        if current_digits and current_is_adjacent:
            yield int("".join(current_digits))


def main():
    lines = sys.stdin.read().splitlines()
    print(sum(iter_numbers(lines)))


if __name__ == "__main__":
    main()
