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

def test_parse_number():
    """Test that number is parsed properly."""
    assert aoc.parse_number("blue", "Game 1: 3 blue, 4 red") == 3

def test_parse_set():
    """Test that set is parsed properly."""
    assert aoc.parse_set("Game 1: 3 blue, 4 red") == [4, 0, 3]

def test_parse_example1(example1):
    """Test that input is parsed properly."""
    assert example1 == [
        [[4, 0, 3], [1, 2, 6], [0, 2, 0]],
        [[0, 2, 1], [1, 3, 4], [0, 1, 1]],
        [[20, 8, 6], [4, 13, 5], [1, 5, 0]], 
        [[3, 1, 6], [6, 3, 0], [14, 3, 15]], 
        [[6, 3, 1], [1, 2, 2]]
    ]

def test_part1_example1(example1):
    """Test part 1 on example input."""
    assert aoc.part1(example1) == 8

def test_part2_example1(example1):
    """Test part 2 on example input."""
    assert aoc.part2(example1) == 2286

@pytest.mark.skip(reason="Not implemented")
def test_part2_example2(example2):
    """Test part 2 on example input."""
    assert aoc.part2(example2) == ...