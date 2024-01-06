package dev.brathis.aoc2023.puzzles;

import dev.brathis.aoc2023.common.PuzzleInputLoader;
import lombok.Data;
import lombok.extern.slf4j.Slf4j;

import java.io.BufferedReader;
import java.io.IOException;
import java.util.*;
import java.util.regex.Pattern;
import java.util.stream.Collectors;

@Slf4j
public class Day22_2 extends Puzzle {
    public Day22_2(PuzzleInputLoader puzzleInputLoader) {
        super(Day22_2.class, puzzleInputLoader);
    }

    private static final Pattern BRICK_PATTERN = Pattern.compile("^(?<x1>\\d+),(?<y1>\\d+),(?<z1>\\d+)~(?<x2>\\d+),(?<y2>\\d+),(?<z2>\\d+)$");

    record PlanarCoordinate(int x, int y) {

        static PlanarCoordinate of(int x, int y) {
            return new PlanarCoordinate(x, y);
        }

        @Override
        public String toString() {
            return "(%d,%d)".formatted(x, y);
        }
    }

    @Data
    private static class Brick {
        private final int id;
        private final int x1;
        private final int y1;
        private final int z1;
        private final int x2;
        private final int y2;
        private final int z2;

        private int minX() {
            return Math.min(x1, x2);
        }

        private int minY() {
            return Math.min(y1, y2);
        }

        private int minZ() {
            return Math.min(z1, z2);
        }

        private int maxX() {
            return Math.max(x1, x2);
        }

        private int maxY() {
            return Math.max(y1, y2);
        }

        private int maxZ() {
            return Math.max(z1, z2);
        }


        Set<PlanarCoordinate> getFootprint() {
            Set<PlanarCoordinate> footprint = new HashSet<>();
            for (int x = minX(); x <= maxX(); ++x) {
                for (int y = minY(); y <= maxY(); ++y) {
                    footprint.add(PlanarCoordinate.of(x, y));
                }
            }
            return footprint;
        }

        int z() {
            return maxZ() - minZ() + 1;
        }
    }

    @Data
    private static class FloorTile {
        private final int floorHeight;
        private final int brickId;
    }

    private final Set<Brick> bricks = new TreeSet<>(Comparator
            .comparingInt(Brick::minZ)
            .thenComparingInt(Brick::maxZ)
            .thenComparingInt(Brick::minY)
            .thenComparingInt(Brick::maxY)
            .thenComparingInt(Brick::minX)
            .thenComparingInt(Brick::maxX));
    private final PriorityQueue<Brick> settledBricks = new PriorityQueue<>(Comparator
            .comparingInt(Brick::minZ)
            .thenComparingInt(Brick::maxZ)
            .thenComparingInt(Brick::minY)
            .thenComparingInt(Brick::maxY)
            .thenComparingInt(Brick::minX)
            .thenComparingInt(Brick::maxX));

    private final Map<PlanarCoordinate, FloorTile> floor = new HashMap<>();
    private final Map<Integer, Set<Integer>> relyingBricks = new HashMap<>();
    private final Map<Integer, Set<Integer>> reliedUponBricks = new HashMap<>();

    @Override
    void puzzle(BufferedReader puzzleInput) throws IOException {
        String line = puzzleInput.readLine();
        while (line != null) {
            processLine(line);
            line = puzzleInput.readLine();
        }
        initFloorHeight();

        for (var brick : bricks) {
            var footprint = brick.getFootprint();
            var highestFloorLevel = footprint.stream()
                    .map(floor::get)
                    .mapToInt(FloorTile::getFloorHeight)
                    .max()
                    .orElseThrow();
            int lowerZ = highestFloorLevel + 1;
            int upperZ = lowerZ + brick.z() - 1;
            log.debug("Placing brick {} at z ({},{}), ", brick, lowerZ, upperZ);

            footprint.stream()
                    .map(floor::get)
                    .filter(floorTile -> floorTile.floorHeight == highestFloorLevel)
                    .forEach(floorTile -> {
                        log.debug("brick {} relies on brick {}, level={}", brick.id, floorTile.brickId, floorTile.floorHeight);
                        if (!relyingBricks.containsKey(floorTile.brickId)) {
                            Set<Integer> relyingBrickIds = new HashSet<>();
                            relyingBrickIds.add(brick.id);
                            relyingBricks.put(floorTile.brickId, relyingBrickIds);
                        } else {
                            relyingBricks.get(floorTile.brickId).add(brick.id);
                        }
                    });
            Set<Integer> reliedUponBrickIds = footprint.stream()
                    .map(floor::get)
                    .filter(floorTile -> floorTile.floorHeight == highestFloorLevel)
                    .map(FloorTile::getBrickId)
                    .collect(Collectors.toSet());
            reliedUponBricks.put(brick.id, reliedUponBrickIds);

            footprint.forEach(fp -> floor.put(fp, new FloorTile(upperZ, brick.id)));
            settledBricks.add(new Brick(brick.id, brick.x1, brick.y1, lowerZ, brick.x2, brick.y2, upperZ));
        }

        long totalCollapsedBricks = 0;
        for (var brick : settledBricks) {
            Queue<Integer> collapsingBricks = new LinkedList<>();
            collapsingBricks.add(brick.id);
            Set<Integer> collapsedBricks = new HashSet<>();
            collapsedBricks.add(brick.id);
            log.info("if brick {} were to be disintegrated...", brick.id);

            while (!collapsingBricks.isEmpty()) {
                var collapsingBrick = collapsingBricks.remove();
                log.debug("brick {} is collapsing", collapsingBrick);
                Set<Integer> bricksRelyingOnThisBrick = relyingBricks.getOrDefault(collapsingBrick, Set.of());
                for (var relyingBrick : bricksRelyingOnThisBrick) {
                    if (collapsedBricks.containsAll(reliedUponBricks.get(relyingBrick))) {
                        // relying brick collapses!
                        collapsedBricks.add(relyingBrick);
                        collapsingBricks.add(relyingBrick);
                        log.debug("...brick {} would fall!", relyingBrick);
                    } else {
                        log.debug("...brick {} would NOT fall!", relyingBrick);
                    }
                }
            }
            collapsedBricks.remove(brick.id); // initial brick does not count
            log.info("Disintegrating brick {} causes {} other bricks to fall: {}", brick.id, collapsedBricks.size(), collapsedBricks);
            totalCollapsedBricks += collapsedBricks.size();
        }
        log.info("The answer is {}", totalCollapsedBricks);
    }

    private void initFloorHeight() {
        int minX = bricks.stream()
                .mapToInt(Brick::minX)
                .min()
                .orElseThrow();
        int maxX = bricks.stream()
                .mapToInt(Brick::maxX)
                .max()
                .orElseThrow();
        int minY = bricks.stream()
                .mapToInt(Brick::minY)
                .min()
                .orElseThrow();
        int maxY = bricks.stream()
                .mapToInt(Brick::maxY)
                .max()
                .orElseThrow();
        log.info("Tower size: ({},{}) x ({},{}) ({} squares)", minX, minY, maxX, maxY, (1 + maxX - minX) * (1 + maxY - minY));
        for (int x = minX; x <= maxX; ++x) {
            for (int y = minY; y <= maxY; ++y) {
                PlanarCoordinate c = PlanarCoordinate.of(x, y);
                floor.put(c, new FloorTile(0, -1)); // -1 means ground
            }
        }
    }

    private void processLine(String line) {
        var matcher = BRICK_PATTERN.matcher(line);
        if (!matcher.matches()) {
            throw new RuntimeException("Line '%s' does not match pattern".formatted(BRICK_PATTERN));
        }
        bricks.add(new Brick(
                bricks.size(),
                Integer.parseInt(matcher.group("x1")),
                Integer.parseInt(matcher.group("y1")),
                Integer.parseInt(matcher.group("z1")),
                Integer.parseInt(matcher.group("x2")),
                Integer.parseInt(matcher.group("y2")),
                Integer.parseInt(matcher.group("z2"))
        ));
    }
}
