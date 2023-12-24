package dev.brathis.aoc2023.puzzles;

import dev.brathis.aoc2023.common.PuzzleInputLoader;
import lombok.Getter;
import lombok.extern.slf4j.Slf4j;

import java.io.BufferedReader;
import java.io.IOException;
import java.util.*;

@Slf4j
public class Day16_1 extends Puzzle {
    public Day16_1(PuzzleInputLoader puzzleInputLoader) {
        super(Day16_1.class, puzzleInputLoader);
    }

    private enum TileType {
        EMPTY_SPACE("."),
        MIRROR_FORWARD("/"),
        MIRROR_BACKWARD("\\"),
        SPLITTER_VERTICAL("|"),
        SPLITTER_HORIZONTAL("-");

        @Getter
        private final String tileValue;

        TileType(String tileValue) {
            this.tileValue = tileValue;
        }

        static TileType fromString(String string) {
            if (string.equals(".")) {
                return EMPTY_SPACE;
            }
            if (string.equals("/")) {
                return MIRROR_FORWARD;
            }
            if (string.equals("\\")) {
                return MIRROR_BACKWARD;
            }
            if (string.equals("|")) {
                return SPLITTER_VERTICAL;
            }
            if (string.equals("-")) {
                return SPLITTER_HORIZONTAL;
            }
            throw new IllegalArgumentException("Tile '%s' is not valid".formatted(string));
        }
    }

    private record Coordinate(int rowIdx, int colIdx) {
    }

    private enum BeamDirection {
        LEFT,
        RIGHT,
        UP,
        DOWN
    }

    private record Beam(Coordinate coordinate, BeamDirection beamDirection) {
    }

    private record VisitState(Set<BeamDirection> directions) {
    }

    private final Map<Coordinate, TileType> tileMap = new HashMap<>();
    private final List<Beam> beams = new LinkedList<>();
    private final Map<Coordinate, VisitState> visitMap = new HashMap<>();
    private int mapHeight;
    private int mapWidth;

    @Override
    void puzzle(BufferedReader puzzleInput) throws IOException {
        buildTileMap(puzzleInput);
        log.info("Built tile map, width={}, height={}", mapWidth, mapHeight);
        beams.add(new Beam(new Coordinate(0, 0), BeamDirection.RIGHT));
        processBeams();
        int answer = visitMap.size();
        log.info("{} tiles have been energized", answer);
    }

    private void processBeams() {
        while (!beams.isEmpty()) {
            log.info("{} beams bouncing...", beams.size());
            for (int beamIdx = 0; beamIdx < beams.size(); ++beamIdx) {
                Beam beam = beams.get(beamIdx);
                processBeam(beam, beamIdx);
            }
        }
    }

    private void processBeam(Beam beam, int beamIdx) {
        if (!isCoordinateOnMap(beam.coordinate())) {
            beams.remove(beamIdx);
            return;
        }

        if (visitMap.containsKey(beam.coordinate())) {
            VisitState visitState = visitMap.get(beam.coordinate());
            if (visitState.directions.contains(beam.beamDirection())) {
                log.debug("Stopping beam {}", beamIdx);
                // A beam has passed through this same tile in the same direction.
                // This will have no effect on the energization of the tiles,
                // so we can stop here.
                beams.remove(beamIdx);
                return;
            }
            visitState.directions.add(beam.beamDirection());
        } else {
            Set<BeamDirection> directions = new HashSet<>();
            directions.add(beam.beamDirection());
            visitMap.put(beam.coordinate(), new VisitState(directions));
        }

        TileType tileType = getTile(beam.coordinate());
        if (tileType.equals(TileType.EMPTY_SPACE) || doesBeamPassThroughSplitter(tileType, beam.beamDirection())) {
            Coordinate newCoordinate = advanceBeam(beam);
            beams.set(beamIdx, new Beam(newCoordinate, beam.beamDirection()));
        } else if (tileType.equals(TileType.MIRROR_FORWARD)) {
            BeamDirection newDirection = getMirrorForwardDirection(beam.beamDirection());
            Coordinate newCoordinate = advanceBeam(beam, newDirection);
            beams.set(beamIdx, new Beam(newCoordinate, newDirection));
        } else if (tileType.equals(TileType.MIRROR_BACKWARD)) {
            BeamDirection newDirection = getMirrorBackwardDirection(beam.beamDirection());
            Coordinate newCoordinate = advanceBeam(beam, newDirection);
            beams.set(beamIdx, new Beam(newCoordinate, newDirection));
        } else if (tileType.equals(TileType.SPLITTER_HORIZONTAL)) {
            Coordinate leftCoordinate = advanceBeam(beam, BeamDirection.LEFT);
            Coordinate rightCoordinate = advanceBeam(beam, BeamDirection.RIGHT);
            beams.remove(beamIdx);
            beams.add(new Beam(leftCoordinate, BeamDirection.LEFT));
            beams.add(new Beam(rightCoordinate, BeamDirection.RIGHT));
        } else if (tileType.equals(TileType.SPLITTER_VERTICAL)) {
            Coordinate upCoordinate = advanceBeam(beam, BeamDirection.UP);
            Coordinate downCoordinate = advanceBeam(beam, BeamDirection.DOWN);
            beams.remove(beamIdx);
            beams.add(new Beam(upCoordinate, BeamDirection.UP));
            beams.add(new Beam(downCoordinate, BeamDirection.DOWN));
        }
    }

    private void buildTileMap(BufferedReader puzzleInput) throws IOException {
        String line = puzzleInput.readLine();
        int rowIdx = 0;
        while (line != null) {
            processRow(line, rowIdx);
            line = puzzleInput.readLine();
            ++rowIdx;
        }
        mapHeight = rowIdx;
    }

    private void processRow(String row, int rowIdx) {
        if (rowIdx == 0) {
            mapWidth = row.length();
        }
        for (int colIdx = 0; colIdx < row.length(); ++colIdx) {
            Coordinate c = new Coordinate(rowIdx, colIdx);
            tileMap.put(c, TileType.fromString(Character.toString(row.charAt(colIdx))));
        }
    }

    private TileType getTile(int rowIdx, int colIdx) {
        return tileMap.get(new Coordinate(rowIdx, colIdx));
    }

    private TileType getTile(Coordinate coordinate) {
        return getTile(coordinate.rowIdx(), coordinate.colIdx());
    }

    private Coordinate advanceBeam(Beam beam) {
        return advanceBeam(beam, beam.beamDirection());
    }

    private Coordinate advanceBeam(Beam beam, BeamDirection beamDirection) {
        Coordinate coordinate = beam.coordinate();
        return switch (beamDirection) {
            case RIGHT -> new Coordinate(coordinate.rowIdx(), coordinate.colIdx() + 1);
            case UP -> new Coordinate(coordinate.rowIdx() - 1, coordinate.colIdx());
            case LEFT -> new Coordinate(coordinate.rowIdx(), coordinate.colIdx() - 1);
            case DOWN -> new Coordinate(coordinate.rowIdx() + 1, coordinate.colIdx());
        };
    }

    private boolean isCoordinateOnMap(Coordinate coordinate) {
        return coordinate.rowIdx() >= 0 && coordinate.rowIdx() < mapHeight && coordinate.colIdx() >= 0 && coordinate.colIdx() < mapWidth;
    }

    private BeamDirection getMirrorForwardDirection(BeamDirection direction) {
        return switch (direction) {
            case UP -> BeamDirection.RIGHT;
            case LEFT -> BeamDirection.DOWN;
            case DOWN -> BeamDirection.LEFT;
            case RIGHT -> BeamDirection.UP;
        };
    }

    private BeamDirection getMirrorBackwardDirection(BeamDirection direction) {
        return switch (direction) {
            case UP -> BeamDirection.LEFT;
            case LEFT -> BeamDirection.UP;
            case DOWN -> BeamDirection.RIGHT;
            case RIGHT -> BeamDirection.DOWN;
        };
    }

    private boolean doesBeamPassThroughSplitter(TileType splitterType, BeamDirection beamDirection) {
        if (!Set.of(TileType.SPLITTER_HORIZONTAL, TileType.SPLITTER_VERTICAL).contains(splitterType)) {
            return false;
        }
        return splitterType.equals(TileType.SPLITTER_HORIZONTAL) && Set.of(BeamDirection.RIGHT, BeamDirection.LEFT).contains(beamDirection)
                || splitterType.equals(TileType.SPLITTER_VERTICAL) && Set.of(BeamDirection.UP, BeamDirection.DOWN).contains(beamDirection);
    }
}
