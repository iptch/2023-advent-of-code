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

def test_get_destination():
    """Test that destination is mapped properly."""
    assert aoc.get_destination(99, [
        [50, 98,  2],
        [52, 50, 48]
    ]) == 51

def test_get_location(example1):
    """Test that location is mapped properly."""
    assert aoc.get_location(79, example1) == 82

def test_parse_example1(example1):
    """Test that input is parsed properly."""
    assert example1 == {
        "seeds": [79, 14, 55, 13],
        "seed_to_soil": [
            [50, 98,  2],
            [52, 50, 48]
        ],
        "soil_to_fertilizer": [
            [ 0, 15, 37],
            [37, 52,  2],
            [39,  0, 15]
        ],
        "fertilizer_to_water": [
            [49, 53,  8],
            [ 0, 11, 42],
            [42,  0,  7],
            [57,  7,  4]
        ],
        "water_to_light": [
            [88, 18,  7],
            [18, 25, 70]
        ],
        "light_to_temperature": [
            [45, 77, 23],
            [81, 45, 19],
            [68, 64, 13]
        ],
        "temperature_to_humidity": [
            [ 0, 69,  1],
            [ 1,  0, 69]
        ],
        "humidity_to_location": [
            [60, 56, 37],
            [56, 93,  4]
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