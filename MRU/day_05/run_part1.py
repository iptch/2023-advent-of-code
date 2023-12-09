class Function:
    def __init__(self, name, sources, destinations, ranges):
        self.name = name
        self.destinations = []
        self.min_sources = []
        self.max_sources = []
        self.ranges = []
        self.next_function: Function | None = None

        for destination, source, r in zip(sources, destinations, ranges):
            i = (r - 1)
            self.min_sources.append(source)
            self.max_sources.append(source + i)
            self.destinations.append(destination)
            self.ranges.append(r)

    def __find_index_between(self, value):
        for i in range(len(self.min_sources)):
            if self.min_sources[i] <= value <= self.max_sources[i]:
                return i
        return -1

    def get_value(self, value):
        index = self.__find_index_between(value)
        if index == -1:
            if self.next_function is None:
                return value
            else:
                return self.next_function.get_value(value)
        else:
            value = self.destinations[index] + (value - self.min_sources[index])

            if self.next_function is None:
                return value
            else:
                return self.next_function.get_value(value)

    def __str__(self):
        return f"{self.name}: \n\tsources: {self.min_sources}\n\tdestinations: {self.destinations}\n\tranges: {self.ranges}"


def get_lines_from_file(filename="input.txt"):
    lines = []
    with open(filename, 'r') as file:
        line = file.readline()
        while line:
            lines.append(line.strip())
            line = file.readline()
    return lines


def parse(lines):
    seeds = []
    order = ['seed-to-soil',
             'soil-to-fertilizer',
             'fertilizer-to-water',
             'water-to-light',
             'light-to-temperature',
             'temperature-to-humidity',
             'humidity-to-location']
    data = {}

    for o in order:
        data[o] = []

    current_part = ""
    for line in lines:
        if len(line) == 0:
            # skip
            continue

        if 'seeds:' in line:
            seeds = [int(x) for x in line.split(" ")[1:]]

        if line[0].isalpha():
            current_part = line.split(" ")[0]

        if line[0].isdigit():
            x, y, r = (line.split(" "))
            # print(current_part, x, y, r)
            data[current_part].append((int(x), int(y), int(r)))

    return seeds, order, data


if __name__ == '__main__':
    lines = get_lines_from_file(filename='input.txt')

    seeds, order, data = parse(lines)
    functions = []
    for k, v in data.items():
        f = Function(name=k, sources=[x[0] for x in v], destinations=[x[1] for x in v], ranges=[x[2] for x in v])
        functions.append(f)
        # print(f)
    for i, o in enumerate(order):
        if i+1 < len(functions):
            # print(o)
            functions[i].next_function = functions[i+1]

    part1 = []
    for s in seeds:
        part1.append(functions[0].get_value(s))

    print("part 1", min(part1))
