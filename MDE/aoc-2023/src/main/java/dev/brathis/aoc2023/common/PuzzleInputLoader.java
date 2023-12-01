package dev.brathis.aoc2023.common;

import java.io.BufferedReader;

public interface PuzzleInputLoader {
    BufferedReader getTestPuzzleInput(Integer day);
    BufferedReader getPuzzleInput(Integer day);
}
