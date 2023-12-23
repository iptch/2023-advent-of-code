import copy
import math
from timeit import default_timer as timer

from aocd import data

DAY = '19'
PART = 'b'


def parse(lines):
    workflows = {}
    workflows_done = False

    for line in lines:
        if not line:
            workflows_done = True
        elif not workflows_done:
            workflow_name, rules = line[0:-1].split('{')
            rules = [rule.split(':') for rule in rules.split(',')]
            workflows[workflow_name] = rules

    return workflows


def get_possibilities(workflow, ranges, workflows):
    sum_of_possibilities = 0
    if workflow not in 'AR':
        for rule in workflows[workflow]:
            if len(rule) == 2:
                l = rule[0][0]
                operator = rule[0][1]
                value = int(rule[0][2:])
                if operator == '<':  # e.g. x < 25
                    # going to other workflow, rule evaluates to true
                    o_ranges = copy.deepcopy(ranges)
                    o_ranges[l][1] = min(ranges[l][1], value - 1)
                    o_workflow = rule[1]
                    sum_of_possibilities += get_possibilities(o_workflow, o_ranges, workflows)
                    # staying in this workflow, rule evaluates to false
                    ranges[l][0] = max(ranges[l][0], value)
                else:  # e.g. x > 25
                    # going to other workflow, rule evaluates to true
                    o_ranges = copy.deepcopy(ranges)
                    o_ranges[l][0] = max(ranges[l][0], value + 1)
                    o_workflow = rule[1]
                    sum_of_possibilities += get_possibilities(o_workflow, o_ranges, workflows)
                    # staying in this workflow, rule evaluates to false
                    ranges[l][1] = min(ranges[l][1], value)
            else:
                workflow = rule[0]

    if workflow == 'A':
        return sum_of_possibilities + math.prod([l[1] - l[0] + 1 for l in ranges.values()])
    elif workflow == 'R':
        return sum_of_possibilities
    else:
        return sum_of_possibilities + get_possibilities(workflow, ranges, workflows)


def solve(lines):
    workflows = parse(lines)
    ranges = {'x': [1, 4000], 'm': [1, 4000], 'a': [1, 4000], 's': [1, 4000]}
    workflow = 'in'
    return get_possibilities(workflow, ranges, workflows)


def main():
    print(f'Advent of Code 2023 --- Day {DAY} --- Part {PART}')

    lines = data.splitlines()
    result = solve(lines)

    print(f'{str(result)}')


if __name__ == '__main__':
    start = timer()
    main()
    print(f"Completed in {timer() - start} sec")
