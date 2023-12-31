package dev.brathis.aoc2023.puzzles;

import dev.brathis.aoc2023.common.PuzzleInputLoader;
import lombok.extern.slf4j.Slf4j;

import java.io.BufferedReader;
import java.io.IOException;
import java.util.LinkedList;
import java.util.List;
import java.util.regex.Pattern;

@Slf4j
public class Day18_2 extends Puzzle {
    public Day18_2(PuzzleInputLoader puzzleInputLoader) {
        super(Day18_2.class, puzzleInputLoader);
    }

    private static final Pattern LINE_PATTERN = Pattern.compile("^[UDRL] \\d+ \\(#(?<steps>[a-z0-9]{5})(?<direction>[0123])\\)$");
    private static final List<Coordinate> nodes = new LinkedList<>();
    private static final List<Integer> edgeLengths = new LinkedList<>();

    private record Coordinate(int rowIdx, int colIdx) {
        @Override
        public String toString() {
            return "(%d,%d)".formatted(rowIdx, colIdx);
        }
    }

    @Override
    void puzzle(BufferedReader puzzleInput) throws IOException {
        String line = puzzleInput.readLine();
        while (line != null) {
            processLine(line);
            line = puzzleInput.readLine();
        }

        log.info("Collected {} nodes", nodes.size());
        long innerArea = calculateInnerArea();
        log.info("Inner area is {}", innerArea);
        long aroundEdgeArea = calculateAroundEdgeArea();
        log.info("Around edge area is {}", aroundEdgeArea);
        long totalArea = innerArea + aroundEdgeArea;
        log.info("The answer is {}", totalArea);
    }

    private void processLine(String line) {
        var matcher = LINE_PATTERN.matcher(line);
        if (!matcher.matches()) {
            throw new IllegalArgumentException("'%s' does not match pattern".formatted(line));
        }
        int steps = Integer.parseInt(matcher.group("steps"), 16);
        String direction = matcher.group("direction");
        Coordinate lastNode = nodes.isEmpty() ? new Coordinate(0, 0) : nodes.get(nodes.size() - 1);
        Coordinate newNode = switch (direction) {
            case "0" -> new Coordinate(lastNode.rowIdx, lastNode.colIdx + steps);
            case "1" -> new Coordinate(lastNode.rowIdx + steps, lastNode.colIdx);
            case "2" -> new Coordinate(lastNode.rowIdx, lastNode.colIdx - steps);
            case "3" -> new Coordinate(lastNode.rowIdx - steps, lastNode.colIdx);
            default ->
                    throw new IllegalArgumentException("Direction '%s' is not valid".formatted(direction));
        };
        nodes.add(newNode);
        edgeLengths.add(steps);
    }

    private long calculateInnerArea() {
        // shoelace formula
        long area = 0;
        for (int nodeIdx = 0; nodeIdx < nodes.size(); ++nodeIdx) {
            int prevNodeIdx = nodeIdx == 0 ? nodes.size() - 1 : nodeIdx - 1;
            int nextNodeIdx = nodeIdx == nodes.size() - 1 ? 0 : nodeIdx + 1;
            Coordinate node = nodes.get(nodeIdx);
            Coordinate prevNode = nodes.get(prevNodeIdx);
            Coordinate nextNode = nodes.get(nextNodeIdx);
            area += (long) node.rowIdx * (nextNode.colIdx - prevNode.colIdx);
        }
        return Math.abs(area / 2);
    }

    private long calculateAroundEdgeArea() {
        long totalLength = edgeLengths.stream()
                .mapToLong(l -> l)
                .sum();
        return 1 + Math.round((double) totalLength / 2);
    }
}
