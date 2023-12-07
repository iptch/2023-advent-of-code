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

def test_get_type_rank_withour_joker():
    """Test that type rank is returned properly."""
    assert aoc.get_type_rank("23456") == 0
    assert aoc.get_type_rank("A23A4") == 1
    assert aoc.get_type_rank("23432") == 2
    assert aoc.get_type_rank("TTT98") == 3
    assert aoc.get_type_rank("23332") == 4
    assert aoc.get_type_rank("AA8AA") == 5
    assert aoc.get_type_rank("AAAAA") == 6

def test_parse_example1(example1):
    """Test that input is parsed properly."""
    assert example1 == [["32T3K", 765], ["T55J5", 684], ["KK677", 28], ["KTJJT", 220], ["QQQJA", 483]] 

def test_part1_example1(example1):
    """Test part 1 on example input."""
    assert aoc.part1(example1) == 6440

def test_part2_example1(example1):
    """Test part 2 on example input."""
    assert aoc.part2(example1) == 5905

@pytest.mark.skip(reason="Not implemented")
def test_part2_example2(example2):
    """Test part 2 on example input."""
    assert aoc.part2(example2) == ...