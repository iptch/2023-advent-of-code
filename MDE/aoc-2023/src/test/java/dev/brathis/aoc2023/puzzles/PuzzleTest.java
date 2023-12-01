package dev.brathis.aoc2023.puzzles;

import dev.brathis.aoc2023.common.ClasspathPuzzleInputLoader;
import dev.brathis.aoc2023.common.PuzzleInputLoader;
import org.junit.jupiter.api.Nested;
import org.junit.jupiter.api.Test;

import java.io.BufferedReader;

import static org.assertj.core.api.Assertions.assertThat;

class PuzzleTest {

    static class Day42_1 extends Puzzle {

        Day42_1(PuzzleInputLoader puzzleInputLoader) {
            super(Day42_1.class, puzzleInputLoader);
        }

        @Override
        void puzzle(BufferedReader puzzleInput) {

        }
    }

    @Nested
    class ClassName_Day42 {
        @Test
        void test_getDay() {
            PuzzleInputLoader puzzleInputLoader = new ClasspathPuzzleInputLoader("testPuzzleInputs");
            var day = new Day42_1(puzzleInputLoader);
            assertThat(day.getDay()).isEqualTo(42);
        }
    }
}
