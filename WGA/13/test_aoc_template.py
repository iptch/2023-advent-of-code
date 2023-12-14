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

def test_get_reflections(example1):
    assert aoc.get_reflections(example1[0]) == []
    assert aoc.get_reflections(example1[1]) == [4]
    assert aoc.get_reflections(aoc.transpose(example1[0])) == [5]
    assert aoc.get_reflections(aoc.transpose(example1[1])) == []

def test_get_reflections_with_smudge(example1):
    assert aoc.get_reflections(example1[0], True) == [3]
    assert aoc.get_reflections(example1[1], True) == [1, 4]
    assert aoc.get_reflections(aoc.transpose(example1[0]), True) == [5]
    assert aoc.get_reflections(aoc.transpose(example1[1]), True) == []

def test_is_diff_by_one():
    assert aoc.is_diff_by_one("#.##..##.", "..##..##.") == True
    assert aoc.is_diff_by_one("..##..##.", "..##..##.") == False

@pytest.mark.skip(reason="Not implemented")
def test_parse_example1(example1):
    """Test that input is parsed properly."""
    assert example1 == ...

def test_part1_example1(example1):
    """Test part 1 on example input."""
    assert aoc.part1(example1) == 405

def test_part2_example1(example1):
    """Test part 2 on example input."""
    assert aoc.part2(example1) == 400

@pytest.mark.skip(reason="Not implemented")
def test_part2_example2(example2):
    """Test part 2 on example input."""
    assert aoc.part2(example2) == ...