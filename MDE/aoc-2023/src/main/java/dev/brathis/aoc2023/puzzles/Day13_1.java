package dev.brathis.aoc2023.puzzles;

import dev.brathis.aoc2023.common.PuzzleInputLoader;
import lombok.extern.slf4j.Slf4j;

import java.io.BufferedReader;
import java.io.IOException;
import java.util.ArrayList;
import java.util.List;
import java.util.stream.Collectors;

@Slf4j
public class Day13_1 extends Puzzle {
    public Day13_1(PuzzleInputLoader puzzleInputLoader) {
        super(Day13_1.class, puzzleInputLoader);
    }

    private record Pattern(List<String> rows) {
        int getWidth() {
            return rows.get(0).length();
        }

        int getHeight() {
            return rows.size();
        }

        String getRow(int idx) {
            return rows.get(idx);
        }

        String getColumn(int idx) {
            return rows.stream()
                    .map(row -> String.valueOf(row.charAt(idx)))
                    .collect(Collectors.joining());
        }
    }

    private final List<Pattern> patterns = new ArrayList<>();
    private Pattern currentPattern = null;

    @Override
    void puzzle(BufferedReader puzzleInput) throws IOException {
        String line = puzzleInput.readLine();
        while (line != null) {
            if (!line.isEmpty()) {
                processLine(line);
            } else {
                completePattern();
            }
            line = puzzleInput.readLine();
        }
        completePattern();

        log.info("Found {} patterns", patterns.size());

        int score = 0;
        for (var pattern : patterns) {
            Integer horizontalMirrorIdx = findHorizontalMirror(pattern);
            if (horizontalMirrorIdx != null) {
                score += 100 * horizontalMirrorIdx;
                continue;
            }
            Integer verticalMirrorIdx = findVerticalMirror(pattern);
            if (verticalMirrorIdx != null) {
                score += verticalMirrorIdx;
            }
        }
        log.info("The answer is {}", score);
    }

    void processLine(String line) {
        if (currentPattern == null) {
            currentPattern = new Pattern(new ArrayList<>());
        }
        currentPattern.rows.add(line);
    }

    void completePattern() {
        patterns.add(currentPattern);
        currentPattern = null;
    }

    Integer findHorizontalMirror(Pattern pattern) {
        int mirrorTop = 0;
        int mirrorBottom = 1;
        while (mirrorBottom < pattern.getHeight()) {
            if (patternHasHorizontalMirrorAt(pattern, mirrorTop, mirrorBottom)) {
                log.info("Found horizontal mirror at ({}, {})", mirrorTop, mirrorBottom);
                return mirrorBottom;
            }
            ++mirrorTop;
            ++mirrorBottom;
        }
        return null;
    }

    boolean patternHasHorizontalMirrorAt(Pattern pattern, int mirrorTop, int mirrorBottom) {
        int cursorTop = mirrorTop;
        int cursorBottom = mirrorBottom;
        while (cursorTop >= 0 && cursorBottom < pattern.getHeight()) {
            if (!pattern.getRow(cursorTop).equals(pattern.getRow(cursorBottom))) {
                return false;
            }
            --cursorTop;
            ++cursorBottom;
        }
        return true;
    }

    Integer findVerticalMirror(Pattern pattern) {
        int mirrorLeft = 0;
        int mirrorRight = 1;
        while (mirrorRight < pattern.getWidth()) {
            if (patternHasVerticalMirrorAt(pattern, mirrorLeft, mirrorRight)) {
                log.info("Found vertical mirror at ({}, {})", mirrorLeft, mirrorRight);
                return mirrorRight;
            }
            ++mirrorLeft;
            ++mirrorRight;
        }
        return null;
    }

    boolean patternHasVerticalMirrorAt(Pattern pattern, int mirrorLeft, int mirrorRight) {
        int cursorLeft = mirrorLeft;
        int cursorRight = mirrorRight;
        while (cursorLeft >= 0 && cursorRight < pattern.getWidth()) {
            if (!pattern.getColumn(cursorLeft).equals(pattern.getColumn(cursorRight))) {
                return false;
            }
            --cursorLeft;
            ++cursorRight;
        }
        return true;
    }
}
