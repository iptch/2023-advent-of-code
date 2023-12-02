import sys

s = 0
for line in sys.stdin:
    nums = ''.join(c for c in line.strip() if c.isdigit())
    num_str = f"{nums[0]}{nums[-1]}"
    s += int(num_str)

print(s)
