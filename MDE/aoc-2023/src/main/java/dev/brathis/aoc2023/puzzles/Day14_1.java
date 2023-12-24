package dev.brathis.aoc2023.puzzles;

import dev.brathis.aoc2023.common.PuzzleInputLoader;
import lombok.extern.slf4j.Slf4j;

import java.io.BufferedReader;
import java.io.IOException;
import java.util.ArrayList;
import java.util.List;

@Slf4j
public class Day14_1 extends Puzzle {
    public Day14_1(PuzzleInputLoader puzzleInputLoader) {
        super(Day14_1.class, puzzleInputLoader);
    }

    private record Map(List<String> rows) {
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
                log.info("{} moves\n{}", moves, this);
                previousRows = new ArrayList<>(rows);
            } while (moves > 0);
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

        private void replaceChar(int rowIdx, int colIdx, char c) {
            StringBuilder stringBuilder = new StringBuilder(rows.get(rowIdx));
            stringBuilder.setCharAt(colIdx, c);
            rows.set(rowIdx, stringBuilder.toString());
        }
    }

    private final Map map = new Map(new ArrayList<>());

    @Override
    void puzzle(BufferedReader puzzleInput) throws IOException {
        String line = puzzleInput.readLine();
        while (line != null) {
            if (!line.isEmpty()) {
                processLine(line);
            }
            line = puzzleInput.readLine();
        }
        map.tiltNorth();
        log.info("The answer is {}", map.getLoadNorth());
    }

    void processLine(String line) {
        map.rows.add(line);
    }
}
