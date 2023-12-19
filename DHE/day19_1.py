from __future__ import annotations
from timeit import default_timer as timer


class Solver:
    workflows = None
    accepted = None
    parts = None

    def __init__(self, day: int):
        input_lines = open(f"input_{day}.txt", 'r').readlines()
        i_empty_line = [len(line) for line in input_lines].index(1)

        self.parts = [Part(line.strip()) for line in input_lines[i_empty_line + 1:]]
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
    eval = None
    next_wf_name = None
    result_state = None

    def __init__(self, instr_str):
        if ':' in instr_str:
            condition, result_str = instr_str.split(':')
            if instr_str[1] == '<':
                self.eval = lambda x: getattr(x, condition[0]) < int(condition[2:])
            elif instr_str[1] == '>':
                self.eval = lambda x: getattr(x, condition[0]) > int(condition[2:])
            else:
                raise Exception("Invalid condition")

            if result_str in ['A', 'R']:
                self.result_state = result_str
            else:
                self.next_wf_name = result_str
        else:
            self.eval = lambda x: True
            if instr_str in ['A', 'R']:
                self.result_state = instr_str
            else:
                self.next_wf_name = instr_str


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
        accepted = []
        for part in self.queue:
            for instr in self.instructions:
                if instr.eval(part):
                    if instr.next_wf_name is not None:
                        next_assignments.append((instr.next_wf_name, part))
                    elif instr.result_state == 'A':
                        accepted.append(part)
                    break
        self.queue = []
        return next_assignments, accepted

    def __repr__(self):
        return f"{self.name}: {self.queue}"


class Part:
    x = None
    m = None
    a = None
    s = None

    def __init__(self, xmas):
        property_string = xmas[1:-1].split(',')
        [self.x, self.m, self.a, self.s] = [int(p[2:]) for p in property_string]

    def __repr__(self):
        return f"(x={self.x},m={self.m},a={self.a},s={self.s})"

    def get_rating(self):
        return self.x + self.m + self.a + self.s


if __name__ == '__main__':
    start = timer()

    solver = Solver(day=19)

    for p in solver.parts:
        solver.workflows['in'].queue.append(p)

    while sum([len(wf.queue) for wf in solver.workflows.values()]) > 0:
        solver.step()

    print(f'Part 1: {sum([a.get_rating() for a in solver.accepted])} (in {(timer() - start) * 1000} ms)')
