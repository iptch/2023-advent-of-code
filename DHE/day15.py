from __future__ import annotations

from timeit import default_timer as timer


def compute_hash(sequence):
    hash_value = 0
    for c in sequence:
        hash_value += ord(c)
        hash_value *= 17
        hash_value %= 256
    return hash_value


class Parser:
    labeled_lenses = None

    def __init__(self, day: int):
        input_file = open(f"input_{day}.txt", 'r')
        self.labeled_lenses = [line.split(',') for line in input_file.readlines()][0]

    def get_lens_parts(self):
        lenses = []
        for lens in self.labeled_lenses:
            if '=' in lens:
                parts = lens.split('=')
                lenses.append(('=', parts[0], int(parts[1])))
            elif '-' in lens:
                lenses.append(('-', lens.split('-')[0], 0))


class Lens:
    operation = None
    label = None
    focal_length = None

    def __init__(self, label_repr):
        if '=' in label_repr:
            self.operation = '='
            parts = label_repr.split('=')
            self.label = parts[0]
            self.focal_length = int(parts[1])
        elif '-' in label_repr:
            self.operation = '-'
            self.label = label_repr.split('-')[0]
        else:
            raise Exception("unknown operation")

    def __eq__(self, other: Lens):
        return self.label == other.label

    def __repr__(self):
        return f"{self.label}: {self.focal_length}"

    def get_box(self):
        return compute_hash(self.label)


class Solver:
    lenses = None
    boxes = None

    def __init__(self, labeled_lenses):
        self.lenses = [Lens(lens_repr) for lens_repr in labeled_lenses]
        self.boxes = {}

    def _fill_boxes(self, lenses):
        for lens in lenses:
            if "=" == lens.operation:
                if self.boxes.get(lens.get_box()) is None:
                    self.boxes[lens.get_box()] = []
                if lens in self.boxes[lens.get_box()]:
                    lens_index = self.boxes[lens.get_box()].index(lens)
                    self.boxes[lens.get_box()][lens_index] = lens
                else:
                    self.boxes[lens.get_box()].append(lens)
            elif '-' == lens.operation and self.boxes.get(lens.get_box()) is not None and lens in self.boxes[lens.get_box()]:
                self.boxes[lens.get_box()].remove(lens)

        return self.boxes

    def solve(self):
        boxes = self._fill_boxes(self.lenses)
        results = 0
        for k in boxes.keys():
            if len(boxes[k]) > 0:
                result = 0
                for i, lens in enumerate(boxes[k]):
                    result += (k + 1) * (i + 1) * lens.focal_length
                results += result
        return results


if __name__ == '__main__':
    start = timer()
    parser = Parser(day=15)
    solver = Solver(parser.labeled_lenses)

    print(f"Puzzle 1: {sum([compute_hash(l) for l in parser.labeled_lenses])}")
    print(f"Puzzle 2: {solver.solve()}")

    print(f'Total time: {(timer() - start) * 1000} ms')
