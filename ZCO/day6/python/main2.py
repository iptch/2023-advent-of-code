import sys
import math

line = sys.stdin.readline()
T = int(line.removeprefix("Time:").strip().replace(" ", ""))

line = sys.stdin.readline()
record_travel = int(line.removeprefix("Distance:").strip().replace(" ", ""))

# This is the function of travel based on startup time:
#   travel(startup_time) = (T - startup_time) * startup_time
# This is an upside down U function. If we solve this equation for travel = record_travel, we get
#   record_travel = (T - startup_time) * startup_time
#   0 = startup_time ^ 2 - T * startup_time + record_travel
# The roots of a quadratic equation are (-b +- (b^2 - 4ac)) / 2a, which is
#   discriminant = T ** 2 - 4 * record_travel
#   root1 = (T + discriminant) / 2
#   root2 = (T - discriminant) / 2
discriminant = math.sqrt(T**2 - 4 * record_travel)
root1 = (T + discriminant) / 2
root2 = (T - discriminant) / 2
root1, root2 = sorted([root1, root2])

# We can then take the amount of distinct values strictly between these two roots
if int(root1) == root1:
    start = int(root1) + 1
else:
    start = math.ceil(root1)
if int(root2) == root2:
    end = int(root2) - 1
else:
    end = math.floor(root2)

print(len(range(start, min(end, T) + 1)))
