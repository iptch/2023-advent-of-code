package dev.brathis.aoc2023.puzzles;

import dev.brathis.aoc2023.common.PuzzleInputLoader;
import lombok.extern.slf4j.Slf4j;

import java.io.BufferedReader;
import java.io.IOException;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

@Slf4j
public class Day11_2 extends Puzzle {
    public Day11_2(PuzzleInputLoader puzzleInputLoader) {
        super(Day11_2.class, puzzleInputLoader);
    }

    private record Coordinate(int rowIdx, int colIdx) {
        @Override
        public String toString() {
            return "[%d, %d]".formatted(rowIdx, colIdx);
        }
    }

    private static final int SCALE_FACTOR = 1_000_000;

    private final Map<Coordinate, Character> galaxyMap = new HashMap<>();
    private final List<Coordinate> galaxies = new ArrayList<>();
    private final List<Integer> rowFactors = new ArrayList<>();
    private final List<Integer> colFactors = new ArrayList<>();
    private int mapWidth;
    private int mapHeight;

    @Override
    void puzzle(BufferedReader puzzleInput) throws IOException {
        loadMap(puzzleInput);
        printMap();
        expandRows();
        expandColumns();
        printMap();
        findGalaxies();
        sumDistances();
    }

    private void loadMap(BufferedReader puzzleInput) throws IOException {
        String line = puzzleInput.readLine();
        int rowIdx = 0;
        while (line != null) {
            if (!line.isEmpty()) {
                if (rowIdx == 0) {
                    mapWidth = line.length();
                }
                for (int colIdx = 0; colIdx < line.length(); ++colIdx) {
                    char tile = line.charAt(colIdx);
                    galaxyMap.put(new Coordinate(rowIdx, colIdx), tile);
                }
            }
            line = puzzleInput.readLine();
            ++rowIdx;
        }
        mapHeight = rowIdx;
        log.info("Loaded map, {}x{}", mapWidth, mapHeight);
    }


    private void printMap() {
        StringBuilder stringBuilder = new StringBuilder();
        stringBuilder.append("\n");
        for (int rowIdx = 0; rowIdx < mapHeight; ++rowIdx) {
            for (int colIdx = 0; colIdx < mapWidth; ++colIdx) {
                stringBuilder.append(galaxyMap.get(new Coordinate(rowIdx, colIdx)));
            }
            stringBuilder.append("\n");
        }
        log.info(stringBuilder.toString());
    }

    private void expandRows() {
        for (int rowIdx = 0; rowIdx < mapHeight; ++rowIdx) {
            boolean isEmpty = true;
            for (int colIdx = 0; colIdx < mapWidth; ++colIdx) {
                char tile = galaxyMap.get(new Coordinate(rowIdx, colIdx));
                if (tile != '.') {
                    isEmpty = false;
                    break;
                }
            }
            rowFactors.add(isEmpty ? SCALE_FACTOR : 1);
        }
    }

    private void expandColumns() {
        for (int colIdx = 0; colIdx < mapWidth; ++colIdx) {
            boolean isEmpty = true;
            for (int rowIdx = 0; rowIdx < mapHeight; ++rowIdx) {
                char tile = galaxyMap.get(new Coordinate(rowIdx, colIdx));
                if (tile != '.') {
                    isEmpty = false;
                    break;
                }
            }
            colFactors.add(isEmpty ? SCALE_FACTOR : 1);
        }
    }

    private void findGalaxies() {
        for (int rowIdx = 0; rowIdx < mapHeight; ++rowIdx) {
            for (int colIdx = 0; colIdx < mapWidth; ++colIdx) {
                Coordinate coordinate = new Coordinate(rowIdx, colIdx);
                if (galaxyMap.get(coordinate) == '#') {
                    galaxies.add(coordinate);
                }
            }
        }
        log.info("Found galaxies: {}", galaxies);
    }

    private void sumDistances() {
        long sum = 0;
        for (int galaxyAIdx = 0; galaxyAIdx < galaxies.size(); ++galaxyAIdx) {
            for (int galaxyBIdx = galaxyAIdx + 1; galaxyBIdx < galaxies.size(); ++galaxyBIdx) {
                Coordinate galaxyA = galaxies.get(galaxyAIdx);
                Coordinate galaxyB = galaxies.get(galaxyBIdx);
                sum += manhattan(galaxyA, galaxyB);
            }
        }
        log.info("The answer is {}", sum);
    }

    private long manhattan(Coordinate a, Coordinate b) {
        return rowDistance(a.rowIdx, b.rowIdx) + colDistance(a.colIdx, b.colIdx);
    }

    private long rowDistance(int rowIdxA, int rowIdxB) {
        if (rowIdxA == rowIdxB) {
            return 0;
        }
        int startIdx = Math.min(rowIdxA, rowIdxB);
        int stopIdx = Math.max(rowIdxA, rowIdxB);
        long distance = 0;
        for (int rowIdx = startIdx; rowIdx < stopIdx; ++rowIdx) {
            distance += rowFactors.get(rowIdx);
        }
        return distance;
    }

    private long colDistance(int colIdxA, int colIdxB) {
        if (colIdxA == colIdxB) {
            return 0;
        }
        int startIdx = Math.min(colIdxA, colIdxB);
        int stopIdx = Math.max(colIdxA, colIdxB);
        long distance = 0;
        for (int colIdx = startIdx; colIdx < stopIdx; ++colIdx) {
            distance += colFactors.get(colIdx);
        }
        return distance;
    }
}
