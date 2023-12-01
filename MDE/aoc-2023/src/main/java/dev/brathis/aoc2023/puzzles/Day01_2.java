package dev.brathis.aoc2023.puzzles;

import dev.brathis.aoc2023.common.PuzzleInputLoader;
import lombok.extern.slf4j.Slf4j;

import java.io.BufferedReader;
import java.io.IOException;
import java.util.Map;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

@Slf4j
public class Day01_2 extends Puzzle {

    private static final Map<String, Integer> INTEGER_MAP = Map.of(
            "one", 1,
            "two", 2,
            "three", 3,
            "four", 4,
            "five", 5,
            "six", 6,
            "seven", 7,
            "eight", 8,
            "nine", 9
    );
    private static final Pattern FIRST_DIGIT_PATTERN = Pattern.compile("^(.*?)(?<digit>\\d|one|two|three|four|five|six|seven|eight|nine)");
    private static final Pattern LAST_DIGIT_PATTERN = Pattern.compile("(.*)(?<digit>\\d|one|two|three|four|five|six|seven|eight|nine)");
    public Day01_2(PuzzleInputLoader puzzleInputLoader) {
        super(Day01_2.class, puzzleInputLoader);
    }

    @Override
    void puzzle(BufferedReader puzzleInput) throws IOException {
        String line = puzzleInput.readLine();
        int sum = 0;
        while (line != null) {
            Integer lineValue = processLine(line);
            if (lineValue == null) {
                return;
            }
            sum += lineValue;
            line = puzzleInput.readLine();
        }
        log.info("The answer is {}", sum);
    }

    private Integer processLine(String line) {
        Integer firstDigit = findFirstDigit(line);
        Integer lastDigit = findLastDigit(line);
        if (firstDigit != null && lastDigit != null) {
            return 10 * firstDigit + lastDigit;
        }
        log.error("Encountered invalid line: '{}'", line);
        return null;
    }

    private Integer findFirstDigit(String line) {
        Matcher matcher = FIRST_DIGIT_PATTERN.matcher(line);
        if (matcher.find()) {
            return toInteger(matcher.group("digit"));
        }
        log.error("Failed to find first digit on line '{}'", line);
        return null;
    }

    private Integer findLastDigit(String line) {
        Matcher matcher = LAST_DIGIT_PATTERN.matcher(line);
        if (matcher.find()) {
            return toInteger(matcher.group("digit"));
        }
        log.error("Failed to find last digit on line '{}'", line);
        return null;
    }

    private Integer toInteger(String match) {
        try {
            return Integer.parseInt(match);
        } catch (NumberFormatException e) {
            return INTEGER_MAP.get(match);
        }
    }
}
