package dev.brathis.aoc2023.common;

import java.io.BufferedReader;
import java.io.InputStream;
import java.io.InputStreamReader;

public class ClasspathPuzzleInputLoader implements PuzzleInputLoader {

    private final String puzzleDirectory;

    public ClasspathPuzzleInputLoader(String puzzleDirectory) {
        this.puzzleDirectory = puzzleDirectory;
    }

    private String getResourcePath(Integer day, Boolean isTest) {
        if (isTest) {
            return "%s/%02d.test.txt".formatted(puzzleDirectory, day);
        }
        return "%s/%02d.txt".formatted(puzzleDirectory, day);
    }

    @Override
    public BufferedReader getTestPuzzleInput(Integer day) {
        return getResource(getResourcePath(day, true));
    }

    @Override
    public BufferedReader getPuzzleInput(Integer day) {
        return getResource(getResourcePath(day, false));
    }

    private static BufferedReader getResource(String path) {
        ClassLoader classLoader = ClasspathPuzzleInputLoader.class.getClassLoader();
        InputStream inputStream = classLoader.getResourceAsStream(path);
        if (inputStream == null) {
            return null;
        }
        InputStreamReader inputStreamReader = new InputStreamReader(inputStream);
        return new BufferedReader(inputStreamReader);
    }
}
