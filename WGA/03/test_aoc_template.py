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

def test_extract_numbers():
    """Test that numbers are extracted properly."""
    assert aoc.extract(aoc.REGEX_NUMBERS, "467..114..") == [("467", 0, 3), ("114", 5, 8)]

def test_extract_gears():
    """Test that gears are extracted properly."""
    assert aoc.extract(aoc.REGEX_GEARS, "...*......") == [("*", 3, 4)]

def test_is_adjacent_to_symbol(example1):
    """Test that adjacent to symbol is checked properly."""
    assert aoc.is_adjacent_to_symbol(example1, 0, 2) == True

def test_get_adjacent_numbers(example1):
    """Test that adjacent numbers are retrieved properly."""
    assert aoc.get_adjacent_numbers([
        [("467", 0, 3), ("114", 5, 8)],
        [],
        [("35", 2, 4), ("633", 6, 9)]
    ], 1, 3) == [467, 35]

def test_parse_example1(example1):
    """Test that input is parsed properly."""
    assert example1 == [
        "467..114..",
        "...*......",
        "..35..633.",
        "......#...",
        "617*......",
        ".....+.58.",
        "..592.....",
        "......755.",
        "...$.*....",
        ".664.598.."
    ]

def test_part1_example1(example1):
    """Test part 1 on example input."""
    assert aoc.part1(example1) == 4361

def test_part2_example1(example1):
    """Test part 2 on example input."""
    assert aoc.part2(example1) == 467835

@pytest.mark.skip(reason="Not implemented")
def test_part2_example2(example2):
    """Test part 2 on example input."""
    assert aoc.part2(example2) == ...