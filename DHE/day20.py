from __future__ import annotations

from timeit import default_timer as timer
import graphviz
import math

FF = '%'
CO = '&'
BR = 'br'


class FilterNetwork:
    modules = None
    low_count = None
    high_count = None
    itr = None
    cycle_lengths = None

    def __init__(self, day: int):
        input_file = open(f"input_{day}.txt", 'r')
        modules_list = [Module(module_str.strip()) for module_str in input_file.readlines()]
        self.modules = dict([(m.name, m) for m in modules_list])
        self._init_co_modules()
        self.low_count = 0
        self.high_count = 0
        self.itr = 0
        self.cycle_lengths = {}

    def __repr__(self):
        repr_str = ''
        for m_name in self.modules:
            repr_str += str(int(self.modules[m_name].on))
        return repr_str

    def _init_co_modules(self):
        co_modules = [m_name for m_name in self.modules.keys() if self.modules[m_name].type == CO]
        for c_name in co_modules:
            for m_name in self.modules.keys():
                if self.modules[c_name].name in self.modules[m_name].outputs:
                    self.modules[c_name].prev_modules[m_name] = False

    def _apply_pulses(self, pulses):
        next_pulses = []
        # pulses is a list of tuples: (prev_name, m_name, pulse)
        for prev_module, m_name, pulse in pulses:
            if pulse:
                self.high_count += 1
            else:
                self.low_count += 1

            if m_name in ['pl', 'zm', 'lz', 'mz'] and not pulse and self.cycle_lengths.get(m_name) is None:
                self.cycle_lengths[m_name] = self.itr

            if m_name not in self.modules.keys():
                continue
            module = self.modules[m_name]
            output_pulse = module.pass_pulse(pulse, prev_module)
            if output_pulse is not None:
                for next_module in self.modules[m_name].outputs:
                    next_pulses.append((m_name, next_module, output_pulse))

        return next_pulses

    def push_button(self):
        self.itr += 1
        pulses = [(None, 'oadcaster', False)]
        while len(pulses) > 0:
            pulses = self._apply_pulses(pulses)

    def visualize(self):
        dot = graphviz.Digraph()
        for m_name in self.modules.keys():
            dot.node(m_name, f'{self.modules[m_name].type}{m_name}')
        for m_name in self.modules.keys():
            for o_name in self.modules[m_name].outputs:
                dot.edge(m_name, o_name)
        dot.render('day20', view=True)

    def compute_pushes_to_turn_on(self):
        return math.lcm(self.cycle_lengths['pl'], self.cycle_lengths['zm'], self.cycle_lengths['lz'],
                        self.cycle_lengths['mz'])


class Module:
    outputs = None
    name = None
    on = None
    type = None
    prev_modules = None

    def __init__(self, filter_str):
        self.on = False
        self.name, output_strs = filter_str.split(' -> ')
        if self.name[0] == FF:
            self.type = FF
            self.name = self.name[1:]
        elif self.name[0] == CO:
            self.type = CO
            self.name = self.name[1:]
        elif self.name == 'broadcaster':
            self.type = BR
            # only for stylistic reasons
            self.name = self.name[2:]
        else:
            raise Exception('unknown filter type')

        self.prev_modules = {}
        self.outputs = output_strs.split(', ')

    def __repr__(self):
        return f"{self.type}{self.name} -> {', '.join(self.outputs)}"

    def __eq__(self, other: Module):
        return self.name == other.name

    def pass_pulse(self, pulse, prev_module):
        if self.type == FF:
            if pulse:
                return None
            self.on = not self.on
            return self.on
        elif self.type == CO:
            self.prev_modules[prev_module] = pulse
            return not all(self.prev_modules.values())
        elif self.type == BR:
            return pulse


if __name__ == '__main__':
    start = timer()

    network = FilterNetwork(day=20)
    for i in range(10000):
        network.push_button()

    # network.visualize()

    print(f'Part 1: {network.low_count * network.high_count}')
    print(f'Part 1: {network.compute_pushes_to_turn_on()}')
    print(f'Total time: {(timer() - start) * 1000} ms')
