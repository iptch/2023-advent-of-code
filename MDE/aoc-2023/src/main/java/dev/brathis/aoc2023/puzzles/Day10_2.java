package dev.brathis.aoc2023.puzzles;

import dev.brathis.aoc2023.common.PuzzleInputLoader;
import lombok.extern.slf4j.Slf4j;

import java.io.BufferedReader;
import java.io.IOException;
import java.util.*;

@Slf4j
public class Day10_2 extends Puzzle {
    public Day10_2(PuzzleInputLoader puzzleInputLoader) {
        super(Day10_2.class, puzzleInputLoader);
    }

    private record Coordinate(int rowIdx, int colIdx) {
        @Override
        public String toString() {
            return "[%d, %d]".formatted(rowIdx, colIdx);
        }
    }

    private enum Direction {
        NORTH,
        WEST,
        SOUTH,
        EAST
    }

    private static final Set<Direction> ALL_DIRECTIONS = Set.of(Direction.NORTH, Direction.WEST, Direction.SOUTH, Direction.EAST);

    private final Map<Coordinate, Character> pipeMap = new HashMap<>();
    private int mapWidth;
    private int mapHeight;
    private Coordinate startCoordinate;
    private char startTile;
    private final Set<Coordinate> loop = new HashSet<>();
    private final Set<Coordinate> enclosedTiles = new HashSet<>();
    private final Queue<Coordinate> frontier = new LinkedList<>();

    @Override
    void puzzle(BufferedReader puzzleInput) throws IOException {
        loadMap(puzzleInput);
        printMap();

        findLoop();
        countEnclosedTiles();
    }

    private void findLoop() {
        frontier.add(startCoordinate);

        while (!frontier.isEmpty()) {
            Coordinate currentTileCoordinate = frontier.poll();

            if (loop.contains(currentTileCoordinate)) {
                log.info("Loop completed! size: {}", loop.size());
                printMap(loop);
                return;
            }

            Set<Direction> neighborDirections = new HashSet<>();
            for (var direction : getDirectionsForTile(pipeMap.get(currentTileCoordinate))) {
                Coordinate neighborTileCoordinate = getNeighboringTileCoordinate(currentTileCoordinate, direction);
                Set<Character> compatibleTiles = getCompatibleTilesForDirection(direction);
                if (!pipeMap.containsKey(neighborTileCoordinate)) {
                    continue;
                }
                if (loop.contains(neighborTileCoordinate)) {
                    continue;
                }
                if (compatibleTiles.contains(pipeMap.get(neighborTileCoordinate))) {
                    frontier.add(neighborTileCoordinate);
                    neighborDirections.add(direction);
                }
            }

            loop.add(currentTileCoordinate);

            if (currentTileCoordinate == startCoordinate) {
                startTile = inferStartTile(neighborDirections);
            }
        }
        throw new RuntimeException("Did not find loop");
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
                    if (tile == 'S') {
                        startCoordinate = new Coordinate(rowIdx, colIdx);
                    }
                    pipeMap.put(new Coordinate(rowIdx, colIdx), tile);
                }
            }
            line = puzzleInput.readLine();
            ++rowIdx;
        }
        mapHeight = rowIdx;
        log.info("Loaded map, {}x{}, start: {}", mapWidth, mapHeight, startCoordinate);
    }

    private void countEnclosedTiles() {
        int numberOfEnclosedTiles = 0;
        for (int rowIdx = 0; rowIdx < mapHeight; ++rowIdx) {
            for (int colIdx = 0; colIdx < mapWidth; ++colIdx) {
                Coordinate coordinate = new Coordinate(rowIdx, colIdx);
                if (loop.contains(coordinate)) {
                    continue;
                }
                if (isEnclosed(coordinate)) {
                    enclosedTiles.add(coordinate);
                    ++numberOfEnclosedTiles;
                }
            }
        }
        log.info("There are {} enclosed tiles", numberOfEnclosedTiles);
        printMap(loop, enclosedTiles);
    }

    private boolean isEnclosed(Coordinate coordinate) {
        double crossings = 0.0;
        final int rowIdx = coordinate.rowIdx;
        for (int colIdx = 0; colIdx < coordinate.colIdx; ++colIdx) {
            Coordinate rayCoordinate = new Coordinate(rowIdx, colIdx);
            // only main loop tiles are relevant
            if (!loop.contains(rayCoordinate)) {
                continue;
            }
            crossings += getScore(pipeMap.get(rayCoordinate));
        }
        return ((int) crossings) % 2 != 0;
    }

    private Set<Character> getCompatibleTilesForDirection(Direction direction) {
        return switch (direction) {
            case NORTH -> Set.of('|', '7', 'F');
            case EAST -> Set.of('-', 'J', '7');
            case SOUTH -> Set.of('|', 'L', 'J');
            case WEST -> Set.of('-', 'L', 'F');
        };
    }

    private Coordinate getNeighboringTileCoordinate(Coordinate tile, Direction direction) {
        return switch (direction) {
            case NORTH -> new Coordinate(tile.rowIdx - 1, tile.colIdx);
            case EAST -> new Coordinate(tile.rowIdx, tile.colIdx + 1);
            case SOUTH -> new Coordinate(tile.rowIdx + 1, tile.colIdx);
            case WEST -> new Coordinate(tile.rowIdx, tile.colIdx - 1);
        };
    }

    private Set<Direction> getDirectionsForTile(char tile) {
        return switch (tile) {
            case '|' -> Set.of(Direction.NORTH, Direction.SOUTH);
            case '-' -> Set.of(Direction.EAST, Direction.WEST);
            case 'L' -> Set.of(Direction.NORTH, Direction.EAST);
            case 'J' -> Set.of(Direction.NORTH, Direction.WEST);
            case '7' -> Set.of(Direction.SOUTH, Direction.WEST);
            case 'F' -> Set.of(Direction.EAST, Direction.SOUTH);
            case 'S' -> ALL_DIRECTIONS;
            default -> throw new IllegalArgumentException("Invalid tile '%s'".formatted(tile));
        };
    }

    private double getScore(char tile) {
        return switch (tile) {
            case '|' -> 1.0;
            case 'F', 'J' -> 0.5;
            case '7', 'L' -> -0.5;
            case 'S' -> getScore(startTile);
            default -> 0.0;
        };
    }

    private void printMap() {
        StringBuilder stringBuilder = new StringBuilder();
        stringBuilder.append("\n");
        for (int rowIdx = 0; rowIdx < mapHeight; ++rowIdx) {
            stringBuilder.append("%03d: ".formatted(rowIdx));
            for (int colIdx = 0; colIdx < mapWidth; ++colIdx) {
                stringBuilder.append(replace(pipeMap.get(new Coordinate(rowIdx, colIdx))));
            }
            stringBuilder.append("\n");
        }
        log.info(stringBuilder.toString());
    }

    private void printMap(Set<Coordinate> loop) {
        StringBuilder stringBuilder = new StringBuilder();
        stringBuilder.append("\n");
        for (int rowIdx = 0; rowIdx < mapHeight; ++rowIdx) {
            stringBuilder.append("%03d: ".formatted(rowIdx));
            for (int colIdx = 0; colIdx < mapWidth; ++colIdx) {
                Coordinate coordinate = new Coordinate(rowIdx, colIdx);
                if (loop.contains(coordinate)) {
                    stringBuilder.append(replace(pipeMap.get(coordinate)));
                } else {
                    stringBuilder.append('.');
                }
            }
            stringBuilder.append("\n");
        }
        log.info(stringBuilder.toString());
    }

    private void printMap(Set<Coordinate> loop, Set<Coordinate> enclosedTiles) {
        StringBuilder stringBuilder = new StringBuilder();
        stringBuilder.append("\n");
        for (int rowIdx = 0; rowIdx < mapHeight; ++rowIdx) {
            stringBuilder.append("%03d: ".formatted(rowIdx));
            for (int colIdx = 0; colIdx < mapWidth; ++colIdx) {
                Coordinate coordinate = new Coordinate(rowIdx, colIdx);
                if (loop.contains(coordinate)) {
                    stringBuilder.append(replace(pipeMap.get(coordinate)));
                } else if (enclosedTiles.contains(coordinate)) {
                    stringBuilder.append('\u2588');
                } else {
                    stringBuilder.append('.');
                }
            }
            stringBuilder.append("\n");
        }
        log.info(stringBuilder.toString());
    }

    private char inferStartTile(Set<Direction> neighborDirections) {
        if (neighborDirections.size() != 2) {
            throw new RuntimeException("Expected start tile to have 2 neighbors");
        }
        if (neighborDirections.equals(Set.of(Direction.NORTH, Direction.SOUTH))) {
            return '|';
        }
        if (neighborDirections.equals(Set.of(Direction.EAST, Direction.WEST))) {
            return '-';
        }
        if (neighborDirections.equals(Set.of(Direction.NORTH, Direction.EAST))) {
            return 'L';
        }
        if (neighborDirections.equals(Set.of(Direction.NORTH, Direction.WEST))) {
            return 'J';
        }
        if (neighborDirections.equals(Set.of(Direction.SOUTH, Direction.WEST))) {
            return '7';
        }
        if (neighborDirections.equals(Set.of(Direction.SOUTH, Direction.EAST))) {
            return 'F';
        }
        throw new RuntimeException("Invalid combination of directions: %s".formatted(neighborDirections));
    }

    private char replace(char tile) {
        return switch(tile) {
            case 'L' -> '\u2514';
            case 'J' -> '\u2518';
            case '7' -> '\u2510';
            case 'F' -> '\u250c';
            default -> tile;
        };
    }
}
