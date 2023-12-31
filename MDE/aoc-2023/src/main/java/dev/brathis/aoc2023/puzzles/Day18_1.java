package dev.brathis.aoc2023.puzzles;

import dev.brathis.aoc2023.common.PuzzleInputLoader;
import lombok.Data;
import lombok.extern.slf4j.Slf4j;

import java.io.BufferedReader;
import java.io.IOException;
import java.util.HashMap;
import java.util.HashSet;
import java.util.Map;
import java.util.Set;
import java.util.regex.Pattern;

@Slf4j
public class Day18_1 extends Puzzle {
    public Day18_1(PuzzleInputLoader puzzleInputLoader) {
        super(Day18_1.class, puzzleInputLoader);
    }

    private static final Pattern LINE_PATTERN = Pattern.compile("^(?<direction>[UDRL]) (?<steps>\\d+) \\(#[a-z0-9]{6}\\)$");
    private static final String EDGE_HORIZONTAL = "-";
    private static final String EDGE_VERTICAL = "|";
    private static final String EDGE_NORTHWEST = "┌";
    private static final String EDGE_NORTHEAST = "┐";
    private static final String EDGE_SOUTHWEST = "└";
    private static final String EDGE_SOUTHEAST = "┘";

    private record Coordinate(int rowIdx, int colIdx) {
        @Override
        public String toString() {
            return "(%d,%d)".formatted(rowIdx, colIdx);
        }
    }

    @Data
    private static class EdgeNode {
        private final Coordinate coordinate;
        private String direction;
        private EdgeNode prev;
        private EdgeNode next;

        String getEdge() {
            return switch (direction) {
                case "R" -> switch (next.direction) {
                    case "R" -> EDGE_HORIZONTAL;
                    case "U" -> EDGE_SOUTHEAST;
                    case "D" -> EDGE_NORTHEAST;
                    default -> throw new IllegalArgumentException("invalid edge");
                };
                case "L" -> switch (next.direction) {
                    case "L" -> EDGE_HORIZONTAL;
                    case "U" -> EDGE_SOUTHWEST;
                    case "D" -> EDGE_NORTHWEST;
                    default -> throw new IllegalArgumentException("invalid edge");
                };
                case "U" -> switch (next.direction) {
                    case "U" -> EDGE_VERTICAL;
                    case "L" -> EDGE_NORTHEAST;
                    case "R" -> EDGE_NORTHWEST;
                    default -> throw new IllegalArgumentException("invalid edge");
                };
                case "D" -> switch (next.direction) {
                    case "D" -> EDGE_VERTICAL;
                    case "L" -> EDGE_SOUTHEAST;
                    case "R" -> EDGE_SOUTHWEST;
                    default -> throw new IllegalArgumentException("invalid edge");
                };
                default -> throw new IllegalArgumentException("invalid edge");
            };
        }

        double getScore() {
            return switch (getEdge()) {
                case EDGE_HORIZONTAL -> 0.0;
                case EDGE_VERTICAL -> 1.0;
                case EDGE_NORTHWEST, EDGE_SOUTHEAST -> 0.5;
                case EDGE_NORTHEAST, EDGE_SOUTHWEST -> -0.5;
                default -> throw new IllegalStateException("Unexpected value: " + getEdge());
            };
        }
    }

    private final Map<Coordinate, EdgeNode> edge = new HashMap<>();
    private final Set<Coordinate> fill = new HashSet<>();
    private int minCol = 0;
    private int maxCol = 0;
    private int minRow = 0;
    private int maxRow = 0;
    private EdgeNode head;

    @Override
    void puzzle(BufferedReader puzzleInput) throws IOException {
        head = new EdgeNode(new Coordinate(0, 0));
        edge.put(head.coordinate, head);

        String line = puzzleInput.readLine();
        while (line != null) {
            processLine(line);
            line = puzzleInput.readLine();
        }

        assert head.direction != null;
        assert head.coordinate.equals(new Coordinate(0, 0));

        log.info("Dug {} tiles along edge", edge.size());
        log.info("Field limits: ({},{}) x ({},{})", minRow, minCol, maxRow, maxCol);
        fill();
        log.info("Dug {} tiles within edge", fill.size());
        printMap();
        log.info("The answer is {}", edge.size() + fill.size());
    }

    private void processLine(String line) {
        var matcher = LINE_PATTERN.matcher(line);
        if (!matcher.matches()) {
            throw new IllegalArgumentException("'%s' does not match pattern".formatted(line));
        }
        dig(matcher.group("direction"), Integer.parseInt(matcher.group("steps")));
    }

    private void dig(String direction, int steps) {
        for (int i = 0; i < steps; ++i) {
            Coordinate diggerPosition = step(direction);
            updateLimits(diggerPosition);

            if (!edge.containsKey(diggerPosition)) {
                var edgeNode = new EdgeNode(diggerPosition);
                edgeNode.direction = direction;
                edgeNode.prev = head;
                head.next = edgeNode;
                head = edgeNode;
                edge.put(diggerPosition, edgeNode);
            } else {
                var startNode = edge.get(diggerPosition);
                startNode.prev = head;
                startNode.direction = direction;
                head.next = startNode;
                head = startNode;
                log.debug("Edge contour completed at {}", head.coordinate);
            }
        }
    }

    private Coordinate step(String direction) {
        var headCoordinate = head.coordinate;
        return switch (direction) {
            case "U" -> new Coordinate(headCoordinate.rowIdx - 1, headCoordinate.colIdx);
            case "D" -> new Coordinate(headCoordinate.rowIdx + 1, headCoordinate.colIdx);
            case "L" -> new Coordinate(headCoordinate.rowIdx, headCoordinate.colIdx - 1);
            case "R" -> new Coordinate(headCoordinate.rowIdx, headCoordinate.colIdx + 1);
            default -> throw new IllegalArgumentException("'%s' is not a valid direction".formatted(direction));
        };
    }

    private void updateLimits(Coordinate coordinate) {
        minCol = Math.min(minCol, coordinate.colIdx);
        maxCol = Math.max(maxCol, coordinate.colIdx);
        minRow = Math.min(minRow, coordinate.rowIdx);
        maxRow = Math.max(maxRow, coordinate.rowIdx);
    }

    private void fill() {
        for (int rowIdx = minRow; rowIdx <= maxRow; ++rowIdx) {
            for (int colIdx = minCol; colIdx <= maxCol; ++colIdx) {
                Coordinate tile = new Coordinate(rowIdx, colIdx);
                if (edge.containsKey(tile)) {
                    continue;
                }

                double score = 0.0;
                // test ray always moves left to right
                for (int rayColIdx = minCol; rayColIdx <= colIdx; ++rayColIdx) {
                    Coordinate ray = new Coordinate(rowIdx, rayColIdx);
                    if (edge.containsKey(ray)) {
                        score += edge.get(ray).getScore();
                    }
                }
                if (Math.abs(Math.round(score)) % 2 == 1) {
                    log.debug("{} is IN", tile);
                    fill.add(tile);
                } else {
                    log.debug("{} is OUT", tile);
                }
            }
        }
    }

    private void printMap() {
        var sb = new StringBuilder();
        for (int rowIdx = minRow; rowIdx <= maxRow; ++rowIdx) {
            sb.append("%03d: ".formatted(rowIdx));
            for (int colIdx = minCol; colIdx <= maxCol; ++colIdx) {
                var tile = new Coordinate(rowIdx, colIdx);
                if (edge.containsKey(tile)) {
                    sb.append(edge.get(tile).getEdge());
                } else if (fill.contains(tile)) {
                    sb.append("#");
                } else {
                    sb.append(".");
                }
            }
            sb.append("\n");
        }
        log.info("\n{}", sb);
    }
}
