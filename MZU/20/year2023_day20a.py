import queue
from timeit import default_timer as timer

from aocd import data

DAY = '20'
PART = 'a'


def initialize_con_nodes(nodes):
    con_nodes = {key: value for (key, value) in nodes.items() if value[0] == '&'}
    for key, value in nodes.items():
        for output_node in value[-1]:
            if output_node in con_nodes.keys():
                con_nodes[output_node][1][key] = False


def update_con_nodes(pulse, source_node, nodes):
    con_nodes = {key: value for (key, value) in nodes.items() if value[0] == '&'}
    for value in con_nodes.values():
        if source_node in value[1].keys():
            value[1][source_node] = pulse


def solve(lines):
    nodes = {}
    for line in lines:
        input_node, output_nodes = line.split(' -> ')
        out_nodes = output_nodes.split(', ')
        if input_node[0] == '%':
            nodes[input_node[1:]] = ['%', False, out_nodes]  # type, on/off state, output nodes
        elif input_node[0] == '&':
            nodes[input_node[1:]] = ['&', {}, out_nodes]  # type, last pulse for each input, output nodes
        else:
            nodes[input_node] = out_nodes  # broadcast

    initialize_con_nodes(nodes)

    low, high = 0, 0
    for _ in range(1000):
        low += 1
        out_nodes = nodes['broadcaster']
        nodes_to_process = queue.Queue()
        for n in out_nodes:
            nodes_to_process.put((False, n))
            low += 1
        while not nodes_to_process.empty():
            pulse, node = nodes_to_process.get()
            if node in ['output', 'rx']:
                continue
            if nodes[node][0] == '%':
                if not pulse:  # only reacts on low pulses
                    nodes[node][1] = not nodes[node][1]  # switch state
                    for output_node in nodes[node][-1]:
                        if nodes[node][1]:  # register pulse it sends out
                            high += 1
                        else:
                            low += 1
                        nodes_to_process.put((nodes[node][1], output_node))
                    update_con_nodes(nodes[node][1], node, nodes)
            elif nodes[node][0] == '&':
                pulse = not all(n == True for n in nodes[node][1].values())
                for output_node in nodes[node][-1]:
                    if not pulse:
                        low += 1
                    else:
                        high += 1
                    nodes_to_process.put((pulse, output_node))
                update_con_nodes(pulse, node, nodes)
    return low * high


def main():
    print(f'Advent of Code 2023 --- Day {DAY} --- Part {PART}')

    lines = data.splitlines()
    result = solve(lines)

    print(f'{str(result)}')


if __name__ == '__main__':
    start = timer()
    main()
    print(f"Completed in {timer() - start} sec")
