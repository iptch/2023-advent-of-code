package dev.brathis.aoc2023.puzzles;

import dev.brathis.aoc2023.common.PuzzleInputLoader;
import lombok.Data;
import lombok.extern.slf4j.Slf4j;

import java.io.BufferedReader;
import java.io.IOException;
import java.util.*;

@Slf4j
public class Day23_1 extends Puzzle {
    public Day23_1(PuzzleInputLoader puzzleInputLoader) {
        super(Day23_1.class, puzzleInputLoader);
    }

    record Coordinate(int rowIdx, int colIdx) {

        static Coordinate of(int rowIdx, int colIdx) {
            return new Coordinate(rowIdx, colIdx);
        }

        @Override
        public String toString() {
            return "(%d,%d)".formatted(rowIdx, colIdx);
        }
    }

    @Data
    private static class Path {
        private final Coordinate head;
        private final int length;
        private final Set<Coordinate> visited;

        Path(Coordinate head, int length, Set<Coordinate> visited) {
            this.head = head;
            this.length = length;
            this.visited = new HashSet<>();
            this.visited.addAll(visited);
        }
    }

    private final Map<Coordinate, Character> tileMap = new HashMap<>();
    private int mapWidth;
    private int mapHeight;


    @Override
    void puzzle(BufferedReader puzzleInput) throws IOException {
        String line = puzzleInput.readLine();
        int rowIdx = 0;
        while (line != null) {
            if (rowIdx == 0) {
                mapWidth = line.length();
            }
            for (int colIdx = 0; colIdx < line.length(); ++colIdx) {
                tileMap.put(Coordinate.of(rowIdx, colIdx), line.charAt(colIdx));
            }
            line = puzzleInput.readLine();
            ++rowIdx;
        }
        mapHeight = rowIdx;

        Coordinate startCoordinate = Coordinate.of(0, 1);
        Coordinate endCoordinate = Coordinate.of(mapHeight - 1, mapWidth - 2);
        log.info("Searching path from {} to {}", startCoordinate, endCoordinate);
        Queue<Path> paths = new LinkedList<>();
        paths.add(new Path(startCoordinate, 0, new HashSet<>()));

        List<Integer> pathLengths = new LinkedList<>();
        while (!paths.isEmpty()) {
            Path p = paths.remove();
            Coordinate c = p.head;
            log.debug("{}", c);
            if (c.equals(endCoordinate)) {
                log.info("found path of length {}", p.length);
                pathLengths.add(p.length);
                continue;
            }
            p.visited.add(c);
            char tile = tileMap.get(c);
            var neighbors = tile == '.' ? getNeighbors(c) : getNeighbor(c, tile);
            for (var n : neighbors) {
                if (!tileMap.containsKey(n) || tileMap.get(n).equals('#') || p.visited.contains(n)) {
                    continue;
                }
                paths.add(new Path(n, p.length + 1, p.visited));
            }
        }
        log.info("The answer is {}", Collections.max(pathLengths));
    }

    List<Coordinate> getNeighbors(Coordinate coordinate) {
        return List.of(
                Coordinate.of(coordinate.rowIdx - 1, coordinate.colIdx),
                Coordinate.of(coordinate.rowIdx + 1, coordinate.colIdx),
                Coordinate.of(coordinate.rowIdx, coordinate.colIdx - 1),
                Coordinate.of(coordinate.rowIdx, coordinate.colIdx + 1)
        );
    }

    List<Coordinate> getNeighbor(Coordinate coordinate, char tile) {
        return switch (tile) {
            case '<' -> List.of(Coordinate.of(coordinate.rowIdx, coordinate.colIdx - 1));
            case '>' -> List.of(Coordinate.of(coordinate.rowIdx, coordinate.colIdx + 1));
            case '^' -> List.of(Coordinate.of(coordinate.rowIdx - 1, coordinate.colIdx));
            case 'v' -> List.of(Coordinate.of(coordinate.rowIdx + 1, coordinate.colIdx));
            default -> throw new IllegalArgumentException("Invalid tile '%s'".formatted(tile));
        };
    }
}
