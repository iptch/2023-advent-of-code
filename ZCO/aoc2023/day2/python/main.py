import math
import re
import sys

PREFIX = re.compile(r"^Game \d+:")

# A game is a list of reveals, a reveal is a mapping of colors to quantity
games: list[list[dict[str, int]]] = []

for line in sys.stdin:
    line = PREFIX.sub("", line)

    reveals = []
    for reveal_string in line.split(";"):
        reveals.append({})
        for color in reveal_string.split(","):
            num, color = color.split()
            reveals[-1][color] = int(num)
    games.append(reveals)

s = 0
for game in games:
    max_colors = {
        "red": 0,
        "green": 0,
        "blue": 0,
    }
    for showing in game:
        for color, num in showing.items():
            max_colors[color] = max(max_colors[color], num)

    s += math.prod(max_colors.values())

print(s)
