package dev.brathis.aoc2023.puzzles;

import dev.brathis.aoc2023.common.PuzzleInputLoader;
import lombok.Data;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;

import java.io.BufferedReader;
import java.io.IOException;
import java.util.*;
import java.util.stream.Collectors;

@Slf4j
public class Day17_2 extends Puzzle {
    public Day17_2(PuzzleInputLoader puzzleInputLoader) {
        super(Day17_2.class, puzzleInputLoader);
    }

    private record Coordinate(int rowIdx, int colIdx) {
        @Override
        public String toString() {
            return "(%d,%d)".formatted(rowIdx, colIdx);
        }
    }

    private enum Direction {
        UP,
        DOWN,
        LEFT,
        RIGHT;

        Direction opposite() {
            return switch (this) {
                case LEFT -> RIGHT;
                case UP -> DOWN;
                case RIGHT -> LEFT;
                case DOWN -> UP;
            };
        }
    }


    @Data
    @RequiredArgsConstructor
    private static class Node {

        private final Coordinate coordinate;
        private final int straightLength;
        private final Direction straightDirection;
        @Override
        public String toString() {
            return "Node[coordinate=%s, dir=%s, len=%d]".formatted(
                    coordinate,
                    straightDirection,
                    straightLength
            );
        }
    }

    @Data
    private static class FrontierNode {
        private final int cost;
        private final Coordinate coordinate;
        private final int straightLength;
        private final Direction straightDirection;
    }

    private final Map<Coordinate, Integer> weights = new HashMap<>();
    private final PriorityQueue<FrontierNode> frontier = new PriorityQueue<>(Comparator.comparingInt(FrontierNode::getCost));
    private final Map<Node, Integer> visited = new HashMap<>();
    private int mapWidth;
    private int mapHeight;
    private Coordinate endCoordinate;


    @Override
    void puzzle(BufferedReader puzzleInput) throws IOException {
        // This is a modified A* algorithm,
        // with the added restriction that there cannot be more than 3 straight
        // segments on each path.
        loadWeights(puzzleInput);
        endCoordinate = new Coordinate(mapHeight - 1, mapWidth - 1);
        log.info("Loaded weights: {} x {}, end coordinate: {}", mapHeight, mapWidth, endCoordinate);

        final FrontierNode startNode = new FrontierNode(0, new Coordinate(0, 0), 0, null);
        frontier.add(startNode);

        while (!frontier.isEmpty()) {
            // pop the node with the smallest f
            FrontierNode fn = frontier.remove();
            log.debug("Visiting node {}", fn);
            final int currentNodeCost = fn.cost;

            // each node is only visited once
            Node node = new Node(fn.coordinate, fn.straightLength, fn.straightDirection);
            if (visited.containsKey(node)) {
                continue;
            }
            visited.put(node, currentNodeCost);

            // try out all the current node's neighbors
            for (Direction direction : List.of(Direction.UP, Direction.DOWN, Direction.LEFT, Direction.RIGHT)) {
                // cannot turn without going straight for less than 4 steps
                if (fn.straightDirection != null && (!direction.equals(fn.straightDirection) && fn.straightLength < 4)) {
                    continue;
                }

                // cannot go straight for more than 10 steps
                if (direction.equals(fn.straightDirection) && fn.straightLength == 10) {
                    continue;
                }

                // cannot reverse direction
                if (fn.straightDirection != null && direction.equals(fn.straightDirection.opposite())) {
                    continue;
                }

                Coordinate neighborCoordinate = getCoordinate(fn.coordinate, direction);

                // skip off-grid coordinates
                if (!weights.containsKey(neighborCoordinate)) {
                    continue;
                }

                // calculate the cost from the start node to the neighbor (g)
                final int neighborCost = currentNodeCost + weights.get(neighborCoordinate);
                FrontierNode neighbor = new FrontierNode(
                        neighborCost,
                        neighborCoordinate,
                        direction.equals(fn.straightDirection) ? fn.straightLength + 1 : 1,
                        direction
                );

                // enqueue the neighbor
                frontier.add(neighbor);
            }
        }

        // out of all the ways that the end node can be reached, pick the one with the lowest cost
        Set<Map.Entry<Node, Integer>> endNodes = visited.entrySet().stream()
                .filter(n -> endCoordinate.equals(n.getKey().coordinate))
                .collect(Collectors.toSet());
        log.info("Found {} end nodes: {}", endNodes.size(), endNodes);
        if (endNodes.isEmpty()) {
            log.error("Did not visit end nodes");
            return;
        }
        List<Integer> endNodeCosts = endNodes.stream()
                .map(Map.Entry::getValue)
                .toList();
        int distance = Collections.min(endNodeCosts);
        log.info("The answer is {}", distance);
    }

    private void loadWeights(BufferedReader puzzleInput) throws IOException {
        int rowIdx = 0;
        String line = puzzleInput.readLine();
        while (line != null) {
            if (rowIdx == 0) {
                mapWidth = line.length();
            }
            for (int colIdx = 0; colIdx < line.length(); ++colIdx) {
                weights.put(new Coordinate(rowIdx, colIdx), Integer.parseInt(String.valueOf(line.charAt(colIdx))));
            }
            ++rowIdx;
            line = puzzleInput.readLine();
        }
        mapHeight = rowIdx;
    }

    private Coordinate getCoordinate(Coordinate start, Direction direction) {
        return switch (direction) {
            case LEFT -> new Coordinate(start.rowIdx, start.colIdx - 1);
            case UP -> new Coordinate(start.rowIdx - 1, start.colIdx);
            case RIGHT -> new Coordinate(start.rowIdx, start.colIdx + 1);
            case DOWN -> new Coordinate(start.rowIdx + 1, start.colIdx);
        };
    }
}
