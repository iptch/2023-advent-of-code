package dev.brathis.aoc2023.common;

import dev.brathis.aoc2023.puzzles.Puzzle;

import java.lang.reflect.InvocationTargetException;

public class PuzzleLoader {
    private static final String PUZZLE_PACKAGE_NAME = "dev.brathis.aoc2023.puzzles";

    private final PuzzleInputLoader puzzleInputLoader;
    public PuzzleLoader(PuzzleInputLoader puzzleInputLoader) {
        this.puzzleInputLoader = puzzleInputLoader;
    }

    public Puzzle loadPuzzle(Integer day, Integer part) {
        String className = "%s.Day%02d_%d".formatted(PUZZLE_PACKAGE_NAME, day, part);
        ClassLoader classLoader = PuzzleLoader.class.getClassLoader();
        try {
            Class<Puzzle> puzzleClass = (Class<Puzzle>) classLoader.loadClass(className);
            return puzzleClass.getConstructor(PuzzleInputLoader.class).newInstance(puzzleInputLoader);
        } catch (ClassNotFoundException | InstantiationException | IllegalAccessException | NoSuchMethodException |
                 InvocationTargetException e) {
            return null;
        }
    }
}
