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
public class Day21_2 extends Puzzle {
    public Day21_2(PuzzleInputLoader puzzleInputLoader) {
        super(Day21_2.class, puzzleInputLoader);
    }

    private record Coordinate(int rowIdx, int colIdx) {
        static Coordinate of(int rowIdx, int colIdx) {
            return new Coordinate(rowIdx, colIdx);
        }
    }

    private record ActiveGardenResultDto(long quantity, int offset) {
        static ActiveGardenResultDto empty() {
            return new ActiveGardenResultDto(0, 0);
        }
    }

    private enum FrontierGardenType {
        CENTER,
        NORTH,
        NORTHEAST,
        EAST,
        SOUTHEAST,
        SOUTH,
        SOUTHWEST,
        WEST,
        NORTHWEST,
    }

    private enum Parity {
        EVEN,
        ODD
    }

    private final Map<Coordinate, String> tiles = new HashMap<>();
    private final Map<FrontierGardenType, List<Integer>> frontierGardenSequences = new HashMap<>();
    private Coordinate startCoordinate = null;
    private int mapHeight;
    private int mapWidth;
    private int gardenSize;
    private int floodedEven;
    private int floodedOdd;

    @Override
    void puzzle(BufferedReader puzzleInput) throws IOException {
        parseMap(puzzleInput);
        log.info("Map: H={} W={}", mapHeight, mapWidth);
        assert mapWidth == mapHeight;
        gardenSize = mapHeight;
        assert mapWidth % 2 == 1;
        assert startCoordinate.rowIdx == (mapHeight - 1) / 2;
        assert startCoordinate.colIdx == (mapWidth - 1) / 2;
        assert false;

        var startingPositions = Map.of(
                FrontierGardenType.CENTER, Coordinate.of((mapHeight - 1) / 2, (mapWidth - 1) / 2),
                FrontierGardenType.NORTH, Coordinate.of(mapHeight - 1, (mapWidth - 1) / 2),
                FrontierGardenType.NORTHEAST, Coordinate.of(mapHeight - 1, 0),
                FrontierGardenType.EAST, Coordinate.of(((mapHeight - 1) / 2), 0),
                FrontierGardenType.SOUTHEAST, Coordinate.of(0, 0),
                FrontierGardenType.SOUTH, Coordinate.of(0, (mapWidth - 1) / 2),
                FrontierGardenType.SOUTHWEST, Coordinate.of(0, mapWidth - 1),
                FrontierGardenType.WEST, Coordinate.of((mapHeight - 1) / 2, mapWidth - 1),
                FrontierGardenType.NORTHWEST, Coordinate.of(mapHeight - 1, mapWidth - 1)
        );
        for (var entry : startingPositions.entrySet()) {
            List<Integer> sequence = getReachableTilesFromStartingPosition(entry.getValue());
            frontierGardenSequences.put(entry.getKey(), sequence);
            log.info("{}: {}", entry.getKey(), sequence);
        }
        log.info("even: {}, odd: {}", floodedEven, floodedOdd);

        if (!testAgainstBruteForce()) {
            int tmp = floodedEven;
            floodedEven = floodedOdd;
            floodedOdd = tmp;
        }
        if (!testAgainstBruteForce()) {
            log.warn(":(");
            return;
        }

//
//        final int steps = 130;
//        long reachableTiles = getReachableTiles(steps);
//        long reachableTilesBruteForce = getReachableTilesBruteForce(steps);
//        log.info("steps={} reachableTiles={} reachableTilesBruteForce={} err={}", steps, reachableTiles, reachableTilesBruteForce, reachableTiles - reachableTilesBruteForce);

        long reachableTiles = getReachableTiles(26_501_365);
        log.info("The answer is {}", reachableTiles);
    }

    private boolean testAgainstBruteForce() {
        Set<Coordinate> reachableBruteForce = Set.of(startCoordinate);
        for (int steps = 0; steps < 2 * gardenSize + 1; ++steps) {
            long reachableTiles = getReachableTiles(steps);
            long reachableTilesBruteForce = reachableBruteForce.size();
            log.info("steps={} reachableTiles={} reachableTilesBruteForce={} err={}", steps, reachableTiles, reachableTilesBruteForce, reachableTiles - reachableTilesBruteForce);
            reachableBruteForce = nextBruteForce(reachableBruteForce);
            if (reachableTilesBruteForce != reachableTiles) {
                return false;
            }
        }
        return true;
    }

    private long getReachableTilesBruteForce(int steps) {
        Set<Coordinate> reachable = Set.of(startCoordinate);
        for (int i = 0; i < steps; ++i) {
            reachable = nextBruteForce(reachable);
            log.trace("after {} steps: {}", i + 1, reachable.size());
        }
        return reachable.size();
    }

    private Set<Coordinate> nextBruteForce(Set<Coordinate> reachable) {
        Set<Coordinate> nextReachable = new HashSet<>();
        for (var c : reachable) {
            nextReachable.addAll(getAllNeighbors(c));
        }
        return nextReachable;
    }

    private long getReachableTiles(int steps) {
        log.debug("Calculating reachable tiles after {} steps", steps);
        long reachableTiles = 0L;
        for (var gardenType : FrontierGardenType.values()) {
            for (var parity : Parity.values()) {
                ActiveGardenResultDto activeGardens = getActiveGardensPerType(gardenType, parity, steps);
                if (activeGardens.quantity < 0) {
                    throw new RuntimeException("computed %d active gardens for %s %s %d".formatted(activeGardens.quantity, gardenType, parity, steps));
                }
                log.trace("gardenType={} parity={} steps={} activeGardens={}", gardenType, parity, steps, activeGardens);
                if (activeGardens.offset > frontierGardenSequences.get(gardenType).size() - 1) {
                    throw new IndexOutOfBoundsException("Offset %d does not exist for sequence %s %s".formatted(activeGardens.offset, gardenType, parity));
                }
                long reachableTilesPerType = frontierGardenSequences.get(gardenType).get(activeGardens.offset);
                if (activeGardens.quantity > 0) {
                    log.debug("{} {} {} active, offset={} -> {}", activeGardens.quantity, gardenType, parity, activeGardens.offset, reachableTilesPerType);
                }
                reachableTiles += activeGardens.quantity * reachableTilesPerType;
            }
            // An "even" garden is a garden whose top-left tile is reachable in an even number of steps.
            long floodedGardensEven = getFloodedGardensPerType(gardenType, Parity.EVEN, steps);
            if (floodedGardensEven < 0) {
                throw new RuntimeException("computed %d flooded gardens for %s %s %d".formatted(floodedGardensEven, gardenType, Parity.EVEN, steps));
            }
            long floodedGardensEvenTiles = steps % 2 == 0 ? floodedEven * floodedGardensEven : floodedOdd * floodedGardensEven;
            if (floodedGardensEven > 0) {
                log.debug("{} {} {} flooded -> {}", floodedGardensEven, gardenType, Parity.EVEN, floodedGardensEvenTiles);
            }
            long floodedGardensOdd = getFloodedGardensPerType(gardenType, Parity.ODD, steps);
            if (floodedGardensOdd < 0) {
                throw new RuntimeException("computed %d flooded gardens for %s %s %d".formatted(floodedGardensOdd, gardenType, Parity.ODD, steps));
            }
            long floodedGardensOddTiles = steps % 2 == 0 ? floodedOdd * floodedGardensOdd : floodedEven * floodedGardensOdd;
            if (floodedGardensOdd > 0) {
                log.debug("{} {} {} flooded -> {}", floodedGardensOdd, gardenType, Parity.ODD, floodedGardensOddTiles);
            }
            reachableTiles += floodedGardensEvenTiles;
            reachableTiles += floodedGardensOddTiles;
        }
        return reachableTiles;
    }

    private ActiveGardenResultDto getActiveGardensPerType(FrontierGardenType gardenType, Parity parity, int steps) {
        return switch (gardenType) {
            case CENTER -> {
                if (parity.equals(Parity.ODD)) {
                    // the center tile is even
                    yield ActiveGardenResultDto.empty();
                }
                yield steps <= gardenSize - 1 ? new ActiveGardenResultDto(1, steps) : ActiveGardenResultDto.empty();
            }
            case SOUTHEAST, SOUTHWEST, NORTHWEST, NORTHEAST -> {
                int it = Math.max(0, (steps - 1) / gardenSize);
                int start = it * gardenSize + 1;
                int offset = steps - start;
                if (it < 1) {
                    yield ActiveGardenResultDto.empty();
                }
                if (it % 2 == 1) {
                    // odd period
                    if (parity.equals(Parity.EVEN)) {
                        yield new ActiveGardenResultDto(it, offset);
                    } else if (it > 1) {
                        yield new ActiveGardenResultDto(it - 1, offset + gardenSize);
                    }
                } else {
                    // even period
                    if (parity.equals(Parity.ODD)) {
                        yield new ActiveGardenResultDto(it, offset);
                    } else if (it > 1) {
                        yield new ActiveGardenResultDto(it - 1, offset + gardenSize);
                    }
                }
                yield ActiveGardenResultDto.empty();
            }
            case EAST, SOUTH, WEST, NORTH -> {
                if (steps < (gardenSize + 1) / 2) {
                    yield ActiveGardenResultDto.empty();
                }
                int it = (steps - (gardenSize + 1) / 2) / gardenSize;
                int start = (gardenSize + 1) / 2 + it * gardenSize;
                if (it % 2 == 0) {
                    if (parity.equals(Parity.ODD)) {
                        // new odd garden starts
                        yield new ActiveGardenResultDto(1L, steps - start);
                    } else if (it >= 1) {
                        // previous even garden is still in progress
                        yield new ActiveGardenResultDto(1L, steps - start + gardenSize);
                    } else {
                        yield ActiveGardenResultDto.empty();
                    }
                } else if (it % 2 == 1) {
                    if (parity.equals(Parity.EVEN)) {
                        // new even garden starts
                        yield new ActiveGardenResultDto(1L, steps - start);
                    } else if (it >= 1) {
                        // previous odd garden is still in progress
                        yield new ActiveGardenResultDto(1L, steps - start + gardenSize);
                    } else {
                        yield ActiveGardenResultDto.empty();
                    }
                } else {
                    yield ActiveGardenResultDto.empty();
                }
            }
        };
    }

    private long getFloodedGardensPerType(FrontierGardenType gardenType, Parity parity, int steps) {
        return switch (gardenType) {
            case CENTER -> parity.equals(Parity.EVEN) && steps >= gardenSize ? 1 : 0;
            case SOUTHEAST, SOUTHWEST, NORTHWEST, NORTHEAST -> {
                long it = Math.max(0, (steps - 1) / gardenSize);
                yield parity.equals(Parity.EVEN) ? ((it - 1) / 2) * ((it - 1) / 2) : (it / 2 - 1) * (it / 2 - 1) + it / 2 - 1;
            }
            case EAST, SOUTH, WEST, NORTH -> {
                long it = Math.max(0, (steps - (gardenSize + 1) / 2) / gardenSize);
                if (it < 2) {
                    yield 0;
                }
                if (parity.equals(Parity.ODD)) {
                    yield it / 2;
                } else {
                    yield (it - 1) / 2;
                }
            }
        };
    }

    private void parseMap(BufferedReader puzzleInput) throws IOException {
        String line = puzzleInput.readLine();
        int rowIdx = 0;
        while (line != null) {
            processLine(line, rowIdx);
            ++rowIdx;
            line = puzzleInput.readLine();
        }
        mapHeight = rowIdx;
    }

    List<Integer> getReachableTilesFromStartingPosition(Coordinate start) {
        List<Integer> sequence = new ArrayList<>();
        Set<Coordinate> reachable = new HashSet<>(Set.of(start));
        int steps = 3 * gardenSize;
        for (int i = 0; i < steps; ++i) {
            sequence.add(reachable.size());
            reachable = reachable.stream()
                    .map(this::getNeighborsInSameGarden)
                    .flatMap(Collection::stream)
                    .collect(Collectors.toSet());
        }
        if (steps % 2 == 0) {
            floodedOdd = sequence.get(sequence.size() - 1);
            floodedEven = sequence.get(sequence.size() - 2);
        } else {
            floodedEven = sequence.get(sequence.size() - 1);
            floodedOdd = sequence.get(sequence.size() - 2);
        }
        return sequence;
    }

    private void processLine(String line, int rowIdx) {
        if (rowIdx == 0) {
            mapWidth = line.length();
        }
        for (int colIdx = 0; colIdx < line.length(); ++colIdx) {
            Coordinate coordinate = Coordinate.of(rowIdx, colIdx);
            String tile = String.valueOf(line.charAt(colIdx));
            if (startCoordinate == null && tile.equals("S")) {
                startCoordinate = coordinate;
            }
            tiles.put(coordinate, tile);
        }
    }

    private Set<Coordinate> getNeighborsInSameGarden(Coordinate c) {
        return Stream.of(
                        Coordinate.of(c.rowIdx - 1, c.colIdx),
                        Coordinate.of(c.rowIdx, c.colIdx - 1),
                        Coordinate.of(c.rowIdx + 1, c.colIdx),
                        Coordinate.of(c.rowIdx, c.colIdx + 1)
                )
                .filter(cc -> cc.rowIdx >= 0 && cc.rowIdx < mapHeight && cc.colIdx >= 0 && cc.colIdx < mapWidth)
                .filter(Predicate.not(cc -> getTile(cc).equals("#")))
                .collect(Collectors.toSet());
    }

    private Set<Coordinate> getAllNeighbors(Coordinate coordinate) {
        return Stream.of(
                        Coordinate.of(coordinate.rowIdx - 1, coordinate.colIdx),
                        Coordinate.of(coordinate.rowIdx, coordinate.colIdx - 1),
                        Coordinate.of(coordinate.rowIdx + 1, coordinate.colIdx),
                        Coordinate.of(coordinate.rowIdx, coordinate.colIdx + 1)
                )
                .filter(Predicate.not(c -> getTile(c).equals("#")))
                .collect(Collectors.toSet());
    }

    private String getTile(Coordinate c) {
        return tiles.get(wrapAround(c));
    }

    private Coordinate wrapAround(Coordinate c) {
        int rowIdx = c.rowIdx % mapHeight;
        if (rowIdx < 0) {
            rowIdx += mapHeight;
        }
        int colIdx = c.colIdx % mapWidth;
        if (colIdx < 0) {
            colIdx += mapWidth;
        }
        return Coordinate.of(rowIdx, colIdx);
    }
}
