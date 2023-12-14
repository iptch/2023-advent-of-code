# aoc_template.py

import pathlib
import sys

def transpose(pattern):
    return [[row[i] for row in pattern] for i in range(len(pattern[0]))]

def is_diff_by_one(str1, str2):
    count = 0

    for i, char1 in enumerate(str1):
        if char1 != str2[i]:
            count += 1
            if count > 1:
                return False

    if count == 1:
        return True
    
    return False

def is_reflection(i, pattern, has_smudge = False):
    count = 0

    for j in range(1, min(i, len(pattern) - i)):
        if has_smudge and is_diff_by_one(pattern[i - 1 - j], pattern[i + j]):
            count += 1
            if count > 1:
                return False
        elif pattern[i - 1 - j] != pattern[i + j]:
            return False
        
    return True

def get_reflections(pattern, has_smudge = False):
    result = []

    for i in range(1, len(pattern)):
        if pattern[i - 1] == pattern[i]:
            if is_reflection(i, pattern, has_smudge):
                result.append(i)
        elif has_smudge and is_diff_by_one(pattern[i - 1], pattern[i]):
            if is_reflection(i, pattern):
                result.append(i)

    return result

def parse(puzzle_input):
    """Parse input."""

    patterns = []
    pattern = []

    for line in puzzle_input.splitlines():
        if line == "":
            patterns.append(pattern)
            pattern = []
        else:
            pattern.append(line)

    patterns.append(pattern)

    return patterns

def part1(data):
    """Solve part 1."""

    result = 0

    for pattern in data:
        h_reflections = get_reflections(pattern)
        v_reflections = get_reflections(transpose(pattern))

        result += sum(v_reflections) + 100 * sum(h_reflections)

    return result

def part2(data):
    """Solve part 2."""

    result = 0

    for pattern in data:
        transposed = transpose(pattern)
        h_reflections_with_smudge = [item for item in get_reflections(pattern, True) if item not in get_reflections(pattern)]
        v_reflections_with_smudge = [item for item in get_reflections(transposed, True) if item not in get_reflections(transposed)]

        result += sum(v_reflections_with_smudge) + 100 * sum(h_reflections_with_smudge)

    return result

def solve(puzzle_input):
    """Solve the puzzle for the given input."""
    data = parse(puzzle_input)
    solution1 = part1(data)
    solution2 = part2(data)

    return solution1, solution2

if __name__ == "__main__":
    for path in sys.argv[1:]:
        print(f"{path}:")
        puzzle_input = pathlib.Path(path).read_text().strip()
        solutions = solve(puzzle_input)
        print("\n".join(str(solution) for solution in solutions))