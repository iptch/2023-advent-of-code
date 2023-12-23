package dev.brathis.aoc2023.puzzles;

import dev.brathis.aoc2023.common.PuzzleInputLoader;
import lombok.extern.slf4j.Slf4j;

import java.io.BufferedReader;
import java.io.IOException;
import java.util.*;

@Slf4j
public class Day14_2 extends Puzzle {
    public Day14_2(PuzzleInputLoader puzzleInputLoader) {
        super(Day14_2.class, puzzleInputLoader);
    }

    private static final int CYCLES = 1000000000;

    private record RockMap(List<String> rows) {
        void tiltNorth() {
            List<String> previousRows = new ArrayList<>(rows);
            int moves;
            do {
                moves = 0;
                for (int rowIdx = 1; rowIdx < getHeight(); ++rowIdx) {
                    String northRow = rows.get(rowIdx - 1);
                    StringBuilder stringBuilder = new StringBuilder();
                    for (int colIdx = 0; colIdx < getWidth(); ++colIdx) {
                        char c = previousRows.get(rowIdx).charAt(colIdx);
                        if (c == '#') {
                            stringBuilder.append('#');
                        } else if (c == '.') {
                            stringBuilder.append('.');
                        } else {
                            if (northRow.charAt(colIdx) == '.') {
                                replaceChar(rowIdx - 1, colIdx, 'O');
                                stringBuilder.append('.');
                                ++moves;
                            } else {
                                stringBuilder.append('O');
                            }
                        }
                    }
                    rows.set(rowIdx, stringBuilder.toString());
                }
                log.debug("{} moves\n{}", moves, this);
                previousRows = new ArrayList<>(rows);
            } while (moves > 0);
        }

        void rotateClockwise() {
            List<String> newRows = new ArrayList<>();
            for (int colIdx = 0; colIdx < getWidth(); ++colIdx) {
                newRows.add(getCol(colIdx));
            }
            rows.clear();
            rows.addAll(newRows);
        }

        void cycle() {
            // north is up
            tiltNorth();
            rotateClockwise();
            // west is up
            tiltNorth();
            rotateClockwise();
            // south is up
            tiltNorth();
            rotateClockwise();
            // east is up
            tiltNorth();
            rotateClockwise();
        }

        String getCol(int colIdx) {
            StringBuilder colStringBuilder = new StringBuilder();
            for (int rowIdx = getHeight() - 1; rowIdx >= 0; --rowIdx) {
                var row = rows.get(rowIdx);
                colStringBuilder.append(row.charAt(colIdx));
            }
            return colStringBuilder.toString();
        }

        int getLoadNorth() {
            int load = 0;
            for (int rowIdx = 0; rowIdx < getHeight(); ++rowIdx) {
                int loadPerRock = getHeight() - rowIdx;
                String row = rows.get(rowIdx);
                load += row.chars()
                        .filter(c -> c == 'O')
                        .count() * loadPerRock;
            }
            return load;
        }

        int getHeight() {
            return rows.size();
        }

        int getWidth() {
            return rows.get(0).length();
        }

        @Override
        public String toString() {
            return String.join("\n", rows);
        }

        @Override
        public int hashCode() {
            return rows.hashCode();
        }

        private void replaceChar(int rowIdx, int colIdx, char c) {
            StringBuilder stringBuilder = new StringBuilder(rows.get(rowIdx));
            stringBuilder.setCharAt(colIdx, c);
            rows.set(rowIdx, stringBuilder.toString());
        }
    }

    private record MapState(int hash, int cycle, int load) {}

    private final RockMap rockMap = new RockMap(new ArrayList<>());
    private final Map<Integer, MapState> mapStatesByHash = new HashMap<>();
    private final List<Integer> loadsByCycles = new ArrayList<>();

    @Override
    void puzzle(BufferedReader puzzleInput) throws IOException {
        String line = puzzleInput.readLine();
        while (line != null) {
            if (!line.isEmpty()) {
                processLine(line);
            }
            line = puzzleInput.readLine();
        }
        for (int i = 0; i < CYCLES; ++i) {
            log.info("Load after {} cycles: {}", i, rockMap.getLoadNorth());
            log.debug("State after {} cycles: {}", i, rockMap.hashCode());
            if (mapStatesByHash.containsKey(rockMap.hashCode())) {
                var mapState = mapStatesByHash.get(rockMap.hashCode());
                log.info("Board state after cycle {} is same as after cycle {}", i, mapState.cycle);
                int offset = mapState.cycle;
                int period = i - mapState.cycle;
                int index = offset + ((CYCLES - offset) % period);
                int answer = loadsByCycles.get(index);
                log.info("Load after cycle {} is same as after cycle {}: {}", CYCLES, index, answer);
                return;
            } else {
                mapStatesByHash.put(rockMap.hashCode(), new MapState(rockMap.hashCode(), i, rockMap.getLoadNorth()));
                loadsByCycles.add(rockMap.getLoadNorth());
            }
            log.debug("Map after {} cycles:\n{}", i, rockMap);
            rockMap.cycle();
        }
        log.info("The answer is {}", rockMap.getLoadNorth());
    }

    void processLine(String line) {
        rockMap.rows.add(line);
    }
}
