from __future__ import annotations

import copy
from timeit import default_timer as timer


class Solver:
    workflows = None
    accepted = None

    def __init__(self, day: int):
        input_lines = open(f"input_{day}.txt", 'r').readlines()
        i_empty_line = [len(line) for line in input_lines].index(1)

        self.workflows = {}
        for line in input_lines[:i_empty_line]:
            wf = Workflow(line.strip())
            self.workflows[wf.name] = wf

        self.accepted = []

    def step(self):
        assignments = []
        for wf in self.workflows.keys():
            assignments_tmp, accepted = self.workflows[wf].do_work()
            self.accepted.extend(accepted)
            assignments.extend(assignments_tmp)

        for part_assignment in assignments:
            self.workflows[part_assignment[0]].queue.append(part_assignment[1])


class Instruction:
    is_default = True
    limit = None
    operator = None
    attr = None

    next_wf_name = None
    result_state = None

    def __init__(self, instr_str):
        if ':' in instr_str:
            self.is_default = False
            condition, result_str = instr_str.split(':')
            self.limit = int(condition[2:])
            self.operator = instr_str[1]
            self.attr = instr_str[0]

            if result_str in ['A', 'R']:
                self.result_state = result_str
            else:
                self.next_wf_name = result_str
        else:
            self.is_default = True

            if instr_str in ['A', 'R']:
                self.result_state = instr_str
            else:
                self.next_wf_name = instr_str

    def is_applicable(self, part_range):
        if '>' == self.operator:
            return getattr(part_range, self.attr)[1] > self.limit
        elif '<' == self.operator:
            return getattr(part_range, self.attr)[0] < self.limit
        elif self.is_default:
            return True
        else:
            raise Exception('cannot check for applicability of instruction.')

    def apply(self, part_range):
        if '>' == self.operator:
            prev_range = getattr(part_range, self.attr)
            if prev_range[0] > self.limit:
                return (self.next_wf_name, self.result_state, part_range), None
            else:
                applied_range = copy.deepcopy(part_range)
                setattr(applied_range, self.attr, (self.limit + 1, prev_range[1]))
                setattr(part_range, self.attr, (prev_range[0], self.limit + 1))
                return (self.next_wf_name, self.result_state, applied_range), part_range

        elif '<' == self.operator:
            prev_range = getattr(part_range, self.attr)
            if prev_range[1] < self.limit:
                return (self.next_wf_name, self.result_state, part_range), None
            else:
                applied_range = copy.deepcopy(part_range)
                setattr(applied_range, self.attr, (prev_range[0], self.limit))
                setattr(part_range, self.attr, (self.limit, prev_range[1]))
                return (self.next_wf_name, self.result_state, applied_range), part_range

        elif self.is_default:
            return (self.next_wf_name, self.result_state, part_range), None


class Workflow:
    name = None
    instructions = None
    queue = None

    def __init__(self, w_string):
        self.name, instr_strs = w_string[:-1].split('{')
        self.instructions = []
        for instr_str in instr_strs.split(','):
            self.instructions.append(Instruction(instr_str))
        self.queue = []

    def do_work(self):
        next_assignments = []
        applied_ranges = []
        accepted = []
        for part_range in self.queue:
            for instr in self.instructions:
                if part_range is not None and instr.is_applicable(part_range):
                    applied_range, rest = instr.apply(part_range)
                    part_range = rest
                    applied_ranges.append(applied_range)
            if part_range is not None:
                raise Exception(f"Range {part_range} was not mapped")

        self.queue = []

        for applied_range in applied_ranges:
            if applied_range[0] is not None:
                next_assignments.append((applied_range[0], applied_range[2]))
            elif 'A' == applied_range[1]:
                accepted.append(applied_range[2])

        return next_assignments, accepted

    def __repr__(self):
        return f"{self.name}: {self.queue}"


class PartRange:
    x = None
    m = None
    a = None
    s = None

    def __init__(self, x=(1, 4001), m=(1, 4001), a=(1, 4001), s=(1, 4001)):
        self.x = x
        self.m = m
        self.a = a
        self.s = s

    def __repr__(self):
        return f"(x={self.x},m={self.m},a={self.a},s={self.s})"

    def get_rating(self):
        return (self.x[1] - self.x[0]) * (self.m[1] - self.m[0]) * (self.a[1] - self.a[0]) * (self.s[1] - self.s[0])


if __name__ == '__main__':
    start = timer()

    solver = Solver(day=19)
    part_range = PartRange()

    solver.workflows['in'].queue.append(part_range)

    while sum([len(wf.queue) for wf in solver.workflows.values()]) > 0:
        solver.step()

    print(f'Part 2: {sum([a.get_rating() for a in solver.accepted])} (in {(timer() - start) * 1000} ms)')
