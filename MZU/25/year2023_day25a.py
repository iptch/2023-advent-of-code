import re
from timeit import default_timer as timer

import networkx as nx
from aocd import data
from pyvis.network import Network

DAY = '25'
PART = 'a'


def get_connected_components(component, group, components):
    if component in components:
        for c in components[component]:
            group.add(c)
            group.update(get_connected_components(c, group, components))
    return group


def get_groups(components):
    groups = []
    for c in components:
        is_already_covered = False
        for g in groups:
            if c in g:
                is_already_covered = True
        if not is_already_covered:
            current_group = set()
            current_group.add(c)
            new_group = get_connected_components(c, current_group, components)
            could_be_merged = False
            for g in groups:
                if any(comp in g for comp in new_group):
                    g.update(new_group)
                    could_be_merged = True

                for g1 in groups:
                    if g1 != g and any(comp in g for comp in g1):
                        g.update(g1)
                        groups.remove(g1)

            if not could_be_merged:
                groups.append(new_group)

    return groups


def visualize(components):
    G = nx.DiGraph(components)
    for n in G.nodes(data=True):
        n[1]['name'] = n[0]  # add label to graph
    net = Network(directed=True)
    net.from_nx(G)
    net.show('aoc-day25.html', notebook=False)


def solve(lines):
    components = {}
    for line in lines:
        line_components = [c for c in re.findall(r'[a-z]+', line)]
        components[line_components[0]] = line_components[1:]

    visualize(components)

    # From visualization, I saw that the three wires are the following and remove these :)
    components['bvc'].remove('rsm')
    components['zmq'].remove('pgh')
    components['bkm'].remove('ldk')

    # then I calculate the group sizes
    groups = get_groups(components)
    return len(groups[0]) * len(groups[1])


def main():
    print(f'Advent of Code 2023 --- Day {DAY} --- Part {PART}')

    lines = data.splitlines()
    result = solve(lines)

    print(f'{str(result)}')


if __name__ == '__main__':
    start = timer()
    main()
    print(f"Completed in {timer() - start} sec")
