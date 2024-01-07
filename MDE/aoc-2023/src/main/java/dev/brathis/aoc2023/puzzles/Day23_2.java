package dev.brathis.aoc2023.puzzles;

import dev.brathis.aoc2023.common.PuzzleInputLoader;
import lombok.Data;
import lombok.extern.slf4j.Slf4j;

import java.io.BufferedReader;
import java.io.IOException;
import java.util.*;
import java.util.function.Predicate;

@Slf4j
public class Day23_2 extends Puzzle {
    public Day23_2(PuzzleInputLoader puzzleInputLoader) {
        super(Day23_2.class, puzzleInputLoader);
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
    private static class TilePath {
        private final Coordinate head;
        private final int length;
        private final Node node;
    }

    @Data
    private static class GraphPath {
        private final Node head;
        private final int length;
        private final Set<Coordinate> visited;

        GraphPath(Node head, int length, Set<Coordinate> visited) {
            this.head = head;
            this.length = length;
            this.visited = new HashSet<>();
            this.visited.addAll(visited);
        }
    }

    @Data
    private static class Node {
        private final Coordinate coordinate;
        private final Map<Coordinate, Integer> neighbors = new HashMap<>();

        @Override
        public String toString() {
            return "Node(coordinate=%s, neighbors=%s".formatted(coordinate, neighbors.entrySet());
        }
    }

    private final Map<Coordinate, Character> tileMap = new HashMap<>();
    private final Map<Coordinate, Node> nodes = new HashMap<>();
    private int mapWidth;
    private int mapHeight;


    @Override
    void puzzle(BufferedReader puzzleInput) throws IOException {
        parseTileMap(puzzleInput);
        buildGraph();
        for (var n : nodes.values()) {
            log.info("{}", n);
        }
        var numNodes = nodes.size();
        var numEdges = nodes.values().stream()
                .map(Node::getNeighbors)
                .mapToInt(Map::size)
                .sum() / 2;
        log.info("{} nodes {} edges", numNodes, numEdges);

        Coordinate startCoordinate = Coordinate.of(0, 1);
        Coordinate endCoordinate = Coordinate.of(mapHeight - 1, mapWidth - 2);
        var longestPath = findLongestPathLength(startCoordinate, endCoordinate);
        log.info("The answer is {}", longestPath);
    }

    private int findLongestPathLength(Coordinate startCoordinate, Coordinate endCoordinate) {
        Node startNode = nodes.get(startCoordinate);
        Node endNode = nodes.get(endCoordinate);
        List<Integer> pathLengths = findPathLengths(new GraphPath(startNode, 0, new HashSet<>()), endNode);
        return Collections.max(pathLengths);
    }

    List<Integer> findPathLengths(GraphPath p, Node endNode) {
        if (p.head.coordinate.equals(endNode.coordinate)) {
            log.debug("Found path of length {}", p.length);
            return List.of(p.length);
        }
        List<Integer> pathLengths = new LinkedList<>();
        p.visited.add(p.head.coordinate);
        for (var n : p.head.neighbors.entrySet()) {
            var nc = n.getKey();
            var nl = n.getValue();
            if (p.visited.contains(nc)) {
                log.debug("already visited node {}", nc);
                continue;
            }
            var gp = new GraphPath(nodes.get(nc), p.length + nl, p.visited);
            pathLengths.addAll(findPathLengths(gp, endNode));
        }
        return pathLengths;
    }

    private void buildGraph() {
        Set<Coordinate> visited = new HashSet<>();
        Coordinate startCoordinate = Coordinate.of(0, 1);
        Node startNode = getOrCreateNode(startCoordinate);
        Coordinate endCoordinate = Coordinate.of(mapHeight - 1, mapWidth - 2);
        Deque<TilePath> s = new LinkedList<>();
        s.addFirst(new TilePath(startCoordinate, 0, startNode));
        while (!s.isEmpty()) {
            var p = s.removeFirst();
            visited.add(p.head);

            if (p.head.equals(endCoordinate)) {
                var node = getOrCreateNode(p.head);
                var prevNode = p.node;
                prevNode.neighbors.put(p.head, p.length);
                node.neighbors.put(prevNode.coordinate, p.length);
                continue;
            }

            var neighbors = getValidUnvisitedNeighbors(p.head, visited);
            if (neighbors.isEmpty()) {
                var nodeNeighbors = getExistingNodeNeighbors(p.head);
                if (!nodeNeighbors.isEmpty()) {
                    log.debug("{} has existing node neighbors {}", p.head, nodeNeighbors);
                    if (nodeNeighbors.size() == 1) {
                        Node neighbor = nodes.get(nodeNeighbors.get(0));
                        // a node is never its own neighbor
                        if (neighbor.coordinate.equals(p.node.coordinate)) {
                            continue;
                        }
                        neighbor.neighbors.put(p.node.coordinate, p.length + 1);
                        p.node.neighbors.put(neighbor.coordinate, p.length + 1);
                        continue;
                    } else {
                        throw new IllegalStateException("%s has multiple neighbors which are existing nodes: %s".formatted(p.head, nodeNeighbors));
                    }
                } else {
                    throw new IllegalStateException("%s has no valid unvisited neighbors".formatted(p.head));
                }
            }

            if (neighbors.size() == 1) {
                s.addFirst(new TilePath(neighbors.get(0), p.length + 1, p.node));
            } else {
                var node = getOrCreateNode(p.head);
                var prevNode = p.node;
                prevNode.neighbors.put(p.head, p.length);
                node.neighbors.put(prevNode.coordinate, p.length);

                for (var n : neighbors) {
                    s.addFirst(new TilePath(n, 1, node));
                }
            }
        }
    }

    private Node getOrCreateNode(Coordinate coordinate) {
        if (nodes.containsKey(coordinate)) {
            return nodes.get(coordinate);
        }
        Node node = new Node(coordinate);
        nodes.put(coordinate, node);
        return node;
    }

    private List<Coordinate> getValidUnvisitedNeighbors(Coordinate c, Set<Coordinate> visited) {
        var unvisitedNeighbors = getNeighbors(c).stream()
                .filter(Predicate.not(visited::contains))
                .toList();
        List<Coordinate> validUnvisitedNeighbors = new LinkedList<>();
        for (var n : unvisitedNeighbors) {
            if (tileMap.containsKey(n) && tileMap.get(n) != '#') {
                validUnvisitedNeighbors.add(n);
            }
        }
        return validUnvisitedNeighbors;
    }

    private List<Coordinate> getExistingNodeNeighbors(Coordinate c) {
        return getNeighbors(c).stream()
                .filter(nodes::containsKey)
                .toList();
    }

    private void parseTileMap(BufferedReader puzzleInput) throws IOException {
        String line = puzzleInput.readLine();
        int rowIdx = 0;
        while (line != null) {
            if (rowIdx == 0) {
                mapWidth = line.length();
            }
            for (int colIdx = 0; colIdx < line.length(); ++colIdx) {
                char tile = line.charAt(colIdx);
                tileMap.put(Coordinate.of(rowIdx, colIdx), tile);
            }
            line = puzzleInput.readLine();
            ++rowIdx;
        }
        mapHeight = rowIdx;
    }

    List<Coordinate> getNeighbors(Coordinate coordinate) {
        return List.of(
                Coordinate.of(coordinate.rowIdx - 1, coordinate.colIdx),
                Coordinate.of(coordinate.rowIdx + 1, coordinate.colIdx),
                Coordinate.of(coordinate.rowIdx, coordinate.colIdx - 1),
                Coordinate.of(coordinate.rowIdx, coordinate.colIdx + 1)
        );
    }
}
