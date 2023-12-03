package dev.brathis.aoc2023.puzzles;

import dev.brathis.aoc2023.common.PuzzleInputLoader;
import lombok.extern.slf4j.Slf4j;

import java.io.BufferedReader;
import java.io.IOException;
import java.util.*;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

@Slf4j
public class Day03_1 extends Puzzle {
    public Day03_1(PuzzleInputLoader puzzleInputLoader) {
        super(Day03_1.class, puzzleInputLoader);
    }

    private static final Pattern NUMBER_PATTERN = Pattern.compile("(?<number>\\d+)");
    private static final Pattern SYMBOL_PATTERN = Pattern.compile("[\\S&&[^\\d\\.]]");

    private record Number(int number, int rowIndex, int charIndex, int size) {
    }

    ;

    private record Coordinate(int rowIndex, int charIndex) {
    }

    ;

    private record MapSearchDto(List<Number> numbers, Set<Coordinate> symbolCoordinates) {
    }

    ;

    @Override
    void puzzle(BufferedReader puzzleInput) throws IOException {
        List<String> lines = linesAsList(puzzleInput);
        MapSearchDto mapSearchResult = searchMap(lines);
        int result = findSumOfNumbersAdjacentToSymbol(mapSearchResult.numbers(), mapSearchResult.symbolCoordinates());
        log.info("The result is {}", result);
    }

    private MapSearchDto searchMap(List<String> lines) {
        List<Number> numbers = new ArrayList<>();
        Set<Coordinate> symbols = new HashSet<>();
        int rowIndex = 0;
        for (String line : lines) {
            Matcher numberMatcher = NUMBER_PATTERN.matcher(line);
            while (numberMatcher.find()) {
                Number number = new Number(Integer.parseInt(numberMatcher.group("number")), rowIndex, numberMatcher.start(), numberMatcher.group("number").length());
                log.info("Found number {}", number);
                numbers.add(number);
            }
            Matcher symbolMatcher = SYMBOL_PATTERN.matcher(line);
            while (symbolMatcher.find()) {
                Coordinate symbolCoordinate = new Coordinate(rowIndex, symbolMatcher.start());
                log.info("Found symbol at {}", symbolCoordinate);
                symbols.add(symbolCoordinate);
            }
            ++rowIndex;
        }
        return new MapSearchDto(numbers, symbols);
    }

    private int findSumOfNumbersAdjacentToSymbol(List<Number> numbers, Set<Coordinate> symbolCoordinates) {
        int sum = 0;
        for (Number number : numbers) {
            List<Coordinate> adjacentCoordinates = findAdjacentCoordinates(number);
            log.info("Number {} has {} adjacent coordinates: {}", number.number(), adjacentCoordinates.size(), adjacentCoordinates);
            if (adjacentCoordinates.stream().anyMatch(symbolCoordinates::contains)) {
                log.info("Number {} has at least one adjacent symbol", number.number());
                sum += number.number();
            } else {
                log.info("Number {} has NO adjacent symbol", number.number());
            }
        }
        return sum;
    }

    private List<Coordinate> findAdjacentCoordinates(Number number) {
        List<Coordinate> adjacentCoordinates = new LinkedList<>();
        adjacentCoordinates.add(new Coordinate(number.rowIndex - 1, number.charIndex - 1)); // top-left
        adjacentCoordinates.add(new Coordinate(number.rowIndex, number.charIndex - 1)); // left
        adjacentCoordinates.add(new Coordinate(number.rowIndex + 1, number.charIndex - 1)); // bottom-left
        adjacentCoordinates.add(new Coordinate(number.rowIndex - 1, number.charIndex + number.size)); // top-right
        adjacentCoordinates.add(new Coordinate(number.rowIndex, number.charIndex + number.size)); // right
        adjacentCoordinates.add(new Coordinate(number.rowIndex + 1, number.charIndex + number.size)); // bottom-right
        for (int charIndex = number.charIndex; charIndex < number.charIndex + number.size; ++charIndex) {
            adjacentCoordinates.add(new Coordinate(number.rowIndex - 1, charIndex)); // top
            adjacentCoordinates.add(new Coordinate(number.rowIndex + 1, charIndex)); // bottom
        }
        return adjacentCoordinates;
    }
}
