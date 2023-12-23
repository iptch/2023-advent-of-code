import re
from timeit import default_timer as timer

from aocd import data

DAY = '19'
PART = 'a'


def parse(lines):
    workflows = {}
    parts = []
    workflows_done = False

    for line in lines:
        if not line:
            workflows_done = True
        else:
            if not workflows_done:
                workflow_name, rules = line[0:-1].split('{')
                rules = [rule.split(':') for rule in rules.split(',')]
                workflows[workflow_name] = rules
            else:
                part_numbers = [int(nr) for nr in re.findall(r'\d+', line)]
                parts.append({
                    'x': part_numbers[0],
                    'm': part_numbers[1],
                    'a': part_numbers[2],
                    's': part_numbers[3]
                })

    return workflows, parts


def solve(lines):
    workflows, parts = parse(lines)
    sum_of_accepted_parts = 0
    for part in parts:
        x, m, a, s = part['x'], part['m'], part['a'], part['s']
        current_workflow = 'in'
        while current_workflow not in 'AR':
            for rule in workflows[current_workflow]:
                if len(rule) == 2:
                    rule_result = eval(rule[0])
                    if rule_result:
                        current_workflow = rule[1]
                        break
                else:
                    current_workflow = rule[0]

        if current_workflow == 'A':
            sum_of_accepted_parts += x + m + a + s

    return sum_of_accepted_parts


def main():
    print(f'Advent of Code 2023 --- Day {DAY} --- Part {PART}')

    lines = data.splitlines()
    result = solve(lines)

    print(f'{str(result)}')


if __name__ == '__main__':
    start = timer()
    main()
    print(f"Completed in {timer() - start} sec")
