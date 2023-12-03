package dev.brathis.aoc2023.puzzles;

import dev.brathis.aoc2023.common.PuzzleInputLoader;

import java.io.BufferedReader;
import java.io.IOException;
import java.util.ArrayList;
import java.util.List;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

public abstract class Puzzle {
    private static final String PUZZLE_CLASS_NAME_REGEX = "Day(?<day>\\d{2})_(?<part>\\d)";
    private static final Pattern PUZZLE_CLASS_NAME_PATTERN = Pattern.compile(PUZZLE_CLASS_NAME_REGEX);
    private static final String PUZZLE_CLASS_NAME_PATTERN_DAY_GROUP_NAME = "day";
    private final Class<?> puzzleClass;
    private final PuzzleInputLoader puzzleInputLoader;

    protected Puzzle(Class<?> puzzleClass, PuzzleInputLoader puzzleInputLoader) {
        this.puzzleClass = puzzleClass;
        this.puzzleInputLoader = puzzleInputLoader;
    }

    private Matcher getMatcher() {
        String puzzleClassName = getPuzzleClassName();
        Matcher matcher = PUZZLE_CLASS_NAME_PATTERN.matcher(puzzleClassName);
        if (!matcher.matches()) {
            throw new RuntimeException("%s does not match pattern %s".formatted(puzzleClassName, PUZZLE_CLASS_NAME_REGEX));
        }
        return matcher;
    }

    public Integer getDay() {
        Matcher matcher = getMatcher();
        return Integer.parseInt(matcher.group(PUZZLE_CLASS_NAME_PATTERN_DAY_GROUP_NAME));
    }

    private String getPuzzleClassName() {
        return puzzleClass.getSimpleName();
    }

    private BufferedReader getPuzzleInput() {
        return puzzleInputLoader.getPuzzleInput(getDay());
    }

    private BufferedReader getTestPuzzleInput() {
        return puzzleInputLoader.getTestPuzzleInput(getDay());
    }

    abstract void puzzle(BufferedReader puzzleInput) throws Exception;

    public void run() throws Exception {
        puzzle(getPuzzleInput());
    }
    public void runTest() throws Exception {
        puzzle(getTestPuzzleInput());
    }

    protected List<String> linesAsList(BufferedReader puzzleInput) throws IOException {
        List<String> lines = new ArrayList<>();
        String line = puzzleInput.readLine();
        while (line != null) {
            lines.add(line);
            line = puzzleInput.readLine();
        }
        return lines;
    }
}
