package dev.brathis.aoc2023.puzzles;

import dev.brathis.aoc2023.common.PuzzleInputLoader;
import lombok.extern.slf4j.Slf4j;

import java.io.BufferedReader;
import java.io.IOException;
import java.util.*;

@Slf4j
public class Day10_1 extends Puzzle {
    public Day10_1(PuzzleInputLoader puzzleInputLoader) {
        super(Day10_1.class, puzzleInputLoader);
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
    private final Set<Coordinate> loop = new HashSet<>();
    private final Queue<Coordinate> frontier = new LinkedList<>();

    @Override
    void puzzle(BufferedReader puzzleInput) throws IOException {
        loadMap(puzzleInput);
        printMap();

        frontier.add(startCoordinate);

        while (!frontier.isEmpty()) {
            Coordinate currentTileCoordinate = frontier.poll();

            if (loop.contains(currentTileCoordinate)) {
                log.info("Loop completed! size: {}", loop.size());
                printMap(loop);
                log.info("The answer is {}", (int) Math.ceil((double) loop.size() / 2));
                return;
            }

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
                }
            }

            loop.add(currentTileCoordinate);
        }
        log.info("Completed without closing loop :(");
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

    private void printMap() {
        StringBuilder stringBuilder = new StringBuilder();
        stringBuilder.append("\n");
        for (int rowIdx = 0; rowIdx < mapHeight; ++rowIdx) {
            for (int colIdx = 0; colIdx < mapWidth; ++colIdx) {
                stringBuilder.append(pipeMap.get(new Coordinate(rowIdx, colIdx)));
            }
            stringBuilder.append("\n");
        }
        log.info(stringBuilder.toString());
    }

    private void printMap(Set<Coordinate> loop) {
        StringBuilder stringBuilder = new StringBuilder();
        stringBuilder.append("\n");
        for (int rowIdx = 0; rowIdx < mapHeight; ++rowIdx) {
            for (int colIdx = 0; colIdx < mapWidth; ++colIdx) {
                Coordinate coordinate = new Coordinate(rowIdx, colIdx);
                if (loop.contains(coordinate)) {
                    stringBuilder.append("*");
                } else {
                    stringBuilder.append(pipeMap.get(coordinate));
                }
            }
            stringBuilder.append("\n");
        }
        log.info(stringBuilder.toString());
    }
}
