package dev.brathis.aoc2023.puzzles;

import dev.brathis.aoc2023.common.PuzzleInputLoader;
import lombok.extern.slf4j.Slf4j;

import java.io.BufferedReader;
import java.io.IOException;
import java.util.*;
import java.util.function.Predicate;
import java.util.stream.Collectors;
import java.util.stream.Stream;

@Slf4j
public class Day21_1 extends Puzzle {
    public Day21_1(PuzzleInputLoader puzzleInputLoader) {
        super(Day21_1.class, puzzleInputLoader);
    }

    private record Coordinate(int rowIdx, int colIdx) {
        static Coordinate of(int rowIdx, int colIdx) {
            return new Coordinate(rowIdx, colIdx);
        }
    }

    private final Map<Coordinate, String> tiles = new HashMap<>();
    private Set<Coordinate> reachableSet = new HashSet<>();
    private Coordinate startCoordinate = null;

    @Override
    void puzzle(BufferedReader puzzleInput) throws IOException {
        String line = puzzleInput.readLine();
        int rowIdx = 0;
        while (line != null) {
            processLine(line, rowIdx);
            ++rowIdx;
            line = puzzleInput.readLine();
        }

        reachableSet.add(startCoordinate);
        for (int i = 0; i < 64; ++i) {
            Set<Coordinate> nextReachableSet = new HashSet<>();
            for (Coordinate c : reachableSet) {
                nextReachableSet.addAll(nextSteps(c));
            }
            reachableSet = nextReachableSet;
        }

        log.info("The answer is {}", reachableSet.size());
    }

    private void processLine(String line, int rowIdx) {
        for (int colIdx = 0; colIdx < line.length(); ++colIdx) {
            Coordinate coordinate = Coordinate.of(rowIdx, colIdx);
            String tile = String.valueOf(line.charAt(colIdx));
            if (startCoordinate == null && tile.equals("S")) {
                startCoordinate = coordinate;
            }
            tiles.put(coordinate, tile);
        }
    }

    private Set<Coordinate> nextSteps(Coordinate coordinate) {
        return Stream.of(
                        Coordinate.of(coordinate.rowIdx - 1, coordinate.colIdx),
                        Coordinate.of(coordinate.rowIdx, coordinate.colIdx - 1),
                        Coordinate.of(coordinate.rowIdx + 1, coordinate.colIdx),
                        Coordinate.of(coordinate.rowIdx, coordinate.colIdx + 1)
                )
                .filter(tiles::containsKey)
                .filter(Predicate.not(c -> tiles.get(c).equals("#")))
                .collect(Collectors.toSet());
    }
}
