import sys
import re

PREFIX = re.compile(r"Card +\d+:")

lines = sys.stdin.read().splitlines()

copies = [1 for _ in range(len(lines))]

for i, line in enumerate(lines):
    line = PREFIX.sub("", line)

    winning, got = line.split("|")
    winning = {int(n) for n in winning.split()}
    got = {int(n) for n in got.split()}
    winning_got = winning.intersection(got)

    points = len(winning_got)

    for di in range(i + 1, min(len(lines), i + points + 1)):
        copies[di] += copies[i]

print(sum(copies))
