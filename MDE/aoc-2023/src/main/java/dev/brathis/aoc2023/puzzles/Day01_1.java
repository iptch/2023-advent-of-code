package dev.brathis.aoc2023.puzzles;

import dev.brathis.aoc2023.common.PuzzleInputLoader;
import lombok.extern.slf4j.Slf4j;

import java.io.BufferedReader;
import java.io.IOException;

@Slf4j
public class Day01_1 extends Puzzle {
    public Day01_1(PuzzleInputLoader puzzleInputLoader) {
        super(Day01_1.class, puzzleInputLoader);
    }

    @Override
    void puzzle(BufferedReader puzzleInput) throws IOException {
        String line = puzzleInput.readLine();
        int sum = 0;
        while (line != null) {
            Integer lineValue = processLine(line);
            if (lineValue != null) {
                sum += lineValue;
            } else {
                return;
            }
            line = puzzleInput.readLine();
        }
        log.info("The answer is {}", sum);
    }

    private Integer processLine(String line) {
        Character firstDigit = findFirstDigit(line);
        Character lastDigit = findLastDigit(line);
        if (firstDigit != null && lastDigit != null) {
            return 10 * Integer.parseInt(firstDigit.toString()) + Integer.parseInt(lastDigit.toString());
        }
        log.error("Encountered invalid line: {}", line);
        return null;
    }

    private Character findFirstDigit(String line) {
        for (int i = 0; i < line.length(); ++i) {
            if (Character.isDigit(line.charAt(i))) {
                return line.charAt(i);
            }
        }
        return null;
    }

    private Character findLastDigit(String line) {
        for (int i = line.length() - 1; i >= 0; --i) {
            if (Character.isDigit(line.charAt(i))) {
                return line.charAt(i);
            }
        }
        return null;
    }
}
