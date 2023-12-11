# test_aoc_template.py

import pathlib
import pytest
import aoc_template as aoc

PUZZLE_DIR = pathlib.Path(__file__).parent

@pytest.fixture
def example1():
    puzzle_input = (PUZZLE_DIR / "example1.txt").read_text().strip()
    return aoc.parse(puzzle_input)

@pytest.fixture
def example2():
    puzzle_input = (PUZZLE_DIR / "example2.txt").read_text().strip()
    return aoc.parse(puzzle_input)

def test_get_y_expansion_pts(example1):
    """Test that input is parsed properly."""
    assert aoc.get_y_expansion_pts(example1) == [3, 7]

def test_get_x_expansion_pts(example1):
    """Test that input is parsed properly."""
    assert aoc.get_x_expansion_pts(example1) == [2, 5, 8]

def test_get_shortest_dist():
    """Test that input is parsed properly."""
    assert aoc.get_shortest_dist((5, 1), (9, 4), [3, 7], [2, 5, 8], 2) ==  9
    assert aoc.get_shortest_dist((0, 3), (8, 7), [3, 7], [2, 5, 8], 2) == 15
    assert aoc.get_shortest_dist((2, 0), (6, 9), [3, 7], [2, 5, 8], 2) == 17
    assert aoc.get_shortest_dist((9, 0), (9, 4), [3, 7], [2, 5, 8], 2) ==  5

@pytest.mark.skip(reason="Not implemented")
def test_parse_example1(example1):
    """Test that input is parsed properly."""
    assert example1 == ...

def test_part1_example1(example1):
    """Test part 1 on example input."""
    assert aoc.part1(example1) == 374

@pytest.mark.skip(reason="Not implemented")
def test_part2_example1(example1):
    """Test part 2 on example input."""
    assert aoc.part2(example1) == ...

@pytest.mark.skip(reason="Not implemented")
def test_part2_example2(example2):
    """Test part 2 on example input."""
    assert aoc.part2(example2) == ...