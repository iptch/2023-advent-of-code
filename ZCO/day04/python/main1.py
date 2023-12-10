import sys
import re

PREFIX = re.compile(r"Card +\d+:")

s = 0

for line in sys.stdin:
    line = PREFIX.sub("", line)
    winning, got = line.split("|")
    winning = {int(n) for n in winning.split()}
    got = {int(n) for n in got.split()}
    winning_got = winning.intersection(got)
    if winning_got:
        s += 2 ** (len(winning_got) - 1)

print(s)
