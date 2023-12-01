package dev.brathis.aoc2023.common;

import org.junit.jupiter.api.Test;

import java.io.BufferedReader;

import static org.assertj.core.api.Assertions.assertThat;

class ClasspathPuzzleInputLoaderTest {
    private final ClasspathPuzzleInputLoader loader;

    ClasspathPuzzleInputLoaderTest() {
        loader = new ClasspathPuzzleInputLoader("testPuzzleInputs");
    }

    @Test
    void test_loadExistingTestInput() {
        BufferedReader puzzleInput = loader.getTestPuzzleInput(1);
        assertThat(puzzleInput).isNotNull();
    }

    @Test
    void test_loadExistingInput() {
        BufferedReader puzzleInput = loader.getPuzzleInput(2);
        assertThat(puzzleInput).isNotNull();
    }

    @Test
    void test_loadNonExistingInput() {
        BufferedReader puzzleInput = loader.getPuzzleInput(1);
        assertThat(puzzleInput).isNull();
    }
}
