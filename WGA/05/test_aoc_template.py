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

def test_get_destination(example1):
    """Test that destination is mapped properly."""
    assert aoc.get_dest(99, example1["maps"][0]) == 51

def test_get_location(example1):
    """Test that location is mapped properly."""
    assert aoc.get_location(79, example1["maps"]) == 82

def test_get_dest_ranges(example1):
    """Test that location ranges are mapped properly."""
    assert aoc.get_dest_ranges([(79, 93)], example1["maps"][0]) == [(81, 95)]

def test_get_location_ranges(example1):
    """Test that location ranges are mapped properly."""
    assert aoc.get_location_ranges((79, 93), example1["maps"]) == [(82, 85), (46, 56), (60, 61)]

def test_parse_example1(example1):
    """Test that input is parsed properly."""
    assert example1 == {
        "seeds": [79, 14, 55, 13],
        "maps": [
            [
                (52,  50,  98),
                (50,  98, 100)
            ],
            [
                (39,   0,  15),
                ( 0,  15,  52),
                (37,  52,  54)
            ],
            [
                (42,   0,   7),
                (57,   7,  11),
                ( 0,  11,  53),
                (49,  53,  61)                
            ],
            [
                (88,  18,  25),
                (18,  25,  95)
            ],
            [
                (81,  45,  64),
                (68,  64,  77),
                (45,  77, 100)
            ],
            [
                ( 1,   0,  69),
                ( 0,  69,  70)
            ],
            [
                (60,  56,  93),
                (56,  93,  97)
            ]
        ]
    }

def test_part1_example1(example1):
    """Test part 1 on example input."""
    assert aoc.part1(example1) == 35

def test_part2_example1(example1):
    """Test part 2 on example input."""
    assert aoc.part2(example1) == 46

@pytest.mark.skip(reason="Not implemented")
def test_part2_example2(example2):
    """Test part 2 on example input."""
    assert aoc.part2(example2) == ...