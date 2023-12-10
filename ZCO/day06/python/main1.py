import math
import sys

line = sys.stdin.readline()
ts = list(map(int, line.removeprefix("Time:").split()))

line = sys.stdin.readline()
ds = list(map(int, line.removeprefix("Distance:").split()))

p = 1
for T, record_travel in zip(ts, ds):
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
    root1 = (T - discriminant) / 2
    root2 = (T + discriminant) / 2

    start = math.floor(root1) + 1
    end = math.ceil(root2) - 1

    r = range(start, min(end, T) + 1)
    p *= len(r)

print(p)
