"""Could not solve day 1 part 2 with my preferred solution because Go Regex does not support
positive lookahead. Python to the rescue."""

import re
from pathlib import PosixPath


def main():
    sum = 0
    regex = "1|2|3|4|5|6|7|8|9|one|two|three|four|five|six|seven|eight|nine"

    parent_path = PosixPath().parent.absolute()
    file_path = parent_path / "SKA" / "inputs" / "aoc01.txt"
    with open(file_path.as_posix(), "r") as file:
        for line in file:
            x = [
                *map(
                    {n: str(i % 9 + 1) for i, n in enumerate(regex.split("|"))}.get,
                    re.findall(rf"(?=({regex}))", line),
                )
            ]

            if len(x) == 0:
                print("no digits found")
            elif len(x) == 1:
                number = x[0] + x[0]
                sum += int(number)
            else:
                number = x[0] + x[-1]
                sum += int(number)

    print(sum)


if __name__ == "__main__":
    main()
