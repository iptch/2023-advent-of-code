package dev.brathis.aoc2023.puzzles;

import dev.brathis.aoc2023.common.PuzzleInputLoader;
import lombok.extern.slf4j.Slf4j;

import java.io.BufferedReader;
import java.io.IOException;
import java.util.Arrays;
import java.util.LinkedList;
import java.util.List;

@Slf4j
public class Day15_1 extends Puzzle {
    public Day15_1(PuzzleInputLoader puzzleInputLoader) {
        super(Day15_1.class, puzzleInputLoader);
    }

    @Override
    void puzzle(BufferedReader puzzleInput) throws IOException {
        String line = puzzleInput.readLine();
        int answer = processInput(line).stream()
                .mapToInt(this::doHash)
                .sum();
        log.info("The answer is {}", answer);
    }

    List<String> processInput(String input) {
        return Arrays.asList(input.split(","));
    }

    private int doHash(String input) {
        int currentValue = 0;
        for (char c : input.toCharArray()) {
            currentValue += (int) c;
            currentValue *= 17;
            currentValue %= 256;
        }
        log.info("HASH of {} is {}", input, currentValue);
        return currentValue;
    }
}
