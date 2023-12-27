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
public class Day11_1 extends Puzzle {
    public Day11_1(PuzzleInputLoader puzzleInputLoader) {
        super(Day11_1.class, puzzleInputLoader);
    }

    private record Coordinate(int rowIdx, int colIdx) {
        @Override
        public String toString() {
            return "[%d, %d]".formatted(rowIdx, colIdx);
        }
    }

    private Map<Coordinate, Character> galaxyMap = new HashMap<>();
    private final List<Coordinate> galaxies = new ArrayList<>();
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
        Map<Coordinate, Character> newGalaxyMap = new HashMap<>();
        int targetRowIdx = 0;
        for (int rowIdx = 0; rowIdx < mapHeight; ++rowIdx) {
            boolean isEmpty = true;
            for (int colIdx = 0; colIdx < mapWidth; ++colIdx) {
                char tile = galaxyMap.get(new Coordinate(rowIdx, colIdx));
                if (tile != '.') {
                    isEmpty = false;
                    break;
                }
            }
            if (isEmpty) {
                for (int colIdx = 0; colIdx < mapWidth; ++colIdx) {
                    newGalaxyMap.put(new Coordinate(targetRowIdx, colIdx), galaxyMap.get(new Coordinate(rowIdx, colIdx)));
                }
                ++targetRowIdx;
            }
            for (int colIdx = 0; colIdx < mapWidth; ++colIdx) {
                newGalaxyMap.put(new Coordinate(targetRowIdx, colIdx), galaxyMap.get(new Coordinate(rowIdx, colIdx)));
            }
            ++targetRowIdx;
        }
        galaxyMap = newGalaxyMap;
        mapHeight = targetRowIdx;
    }

    private void expandColumns() {
        Map<Coordinate, Character> newGalaxyMap = new HashMap<>();
        int targetColumnIdx = 0;
        for (int colIdx = 0; colIdx < mapWidth; ++colIdx) {
            boolean isEmpty = true;
            for (int rowIdx = 0; rowIdx < mapHeight; ++rowIdx) {
                char tile = galaxyMap.get(new Coordinate(rowIdx, colIdx));
                if (tile != '.') {
                    isEmpty = false;
                    break;
                }
            }
            if (isEmpty) {
                for (int rowIdx = 0; rowIdx < mapHeight; ++rowIdx) {
                    newGalaxyMap.put(new Coordinate(rowIdx, targetColumnIdx), galaxyMap.get(new Coordinate(rowIdx, colIdx)));
                }
                ++targetColumnIdx;
            }
            for (int rowIdx = 0; rowIdx < mapHeight; ++rowIdx) {
                newGalaxyMap.put(new Coordinate(rowIdx, targetColumnIdx), galaxyMap.get(new Coordinate(rowIdx, colIdx)));
            }
            ++targetColumnIdx;
        }
        galaxyMap = newGalaxyMap;
        mapWidth = targetColumnIdx;
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
        int sum = 0;
        for (int galaxyAIdx = 0; galaxyAIdx < galaxies.size(); ++galaxyAIdx) {
            for (int galaxyBIdx = galaxyAIdx + 1; galaxyBIdx < galaxies.size(); ++galaxyBIdx) {
                Coordinate galaxyA = galaxies.get(galaxyAIdx);
                Coordinate galaxyB = galaxies.get(galaxyBIdx);
                sum += manhattan(galaxyA, galaxyB);
            }
        }
        log.info("The answer is {}", sum);
    }

    private int manhattan(Coordinate a, Coordinate b) {
        return Math.abs(a.rowIdx - b.rowIdx) + Math.abs(a.colIdx - b.colIdx);
    }
}
