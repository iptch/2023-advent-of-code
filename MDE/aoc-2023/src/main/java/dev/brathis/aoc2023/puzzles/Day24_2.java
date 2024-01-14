package dev.brathis.aoc2023.puzzles;

import dev.brathis.aoc2023.common.PuzzleInputLoader;
import lombok.Data;
import lombok.extern.slf4j.Slf4j;

import java.io.BufferedReader;
import java.io.IOException;
import java.math.BigDecimal;
import java.math.RoundingMode;
import java.util.ArrayList;
import java.util.List;
import java.util.regex.Pattern;

@Slf4j
public class Day24_2 extends Puzzle {
    public Day24_2(PuzzleInputLoader puzzleInputLoader) {
        super(Day24_2.class, puzzleInputLoader);
    }

    private static final Pattern HAILSTONE_PATTERN = Pattern.compile("^(-?\\d+),\\s+(-?\\d+),\\s+(-?\\d+)\\s+@\\s+(-?\\d+),\\s+(-?\\d+),\\s+(-?\\d+)$");
    private static final int SCALE = 50;

    @Data
    private static class Hailstone {
        private final long px;
        private final long py;
        private final long pz;
        private final long vx;
        private final long vy;
        private final long vz;

        @Override
        public String toString() {
            return "%d, %d, %d @ %d, %d, %d".formatted(px, py, pz, vx, vy, vz);
        }
    }

    private final List<Hailstone> h = new ArrayList<>();

    @Override
    void puzzle(BufferedReader puzzleInput) throws IOException {
        String line = puzzleInput.readLine();
        while (line != null) {
            processLine(line);
            line = puzzleInput.readLine();
        }
        log.info("Hailstones: {}", h);
        // we only need x, y, z, so in theory we could do with fewer equations than this but oh well
        if (h.size() < 6) {
            throw new IllegalStateException("Need at least 6 hailstones to calculate solution");
        }

        BigDecimal[][] A = {
                {
                        BigDecimal.valueOf(h.get(0).vy - h.get(1).vy),
                        BigDecimal.valueOf(h.get(1).py - h.get(0).py),
                        BigDecimal.valueOf(h.get(1).vx - h.get(0).vx),
                        BigDecimal.valueOf(h.get(0).px - h.get(1).px),
                        BigDecimal.valueOf(0L),
                        BigDecimal.valueOf(0L),
                },
                {
                        BigDecimal.valueOf(h.get(0).vz - h.get(1).vz),
                        BigDecimal.valueOf(h.get(1).pz - h.get(0).pz),
                        BigDecimal.valueOf(0L),
                        BigDecimal.valueOf(0L),
                        BigDecimal.valueOf(h.get(1).vx - h.get(0).vx),
                        BigDecimal.valueOf(h.get(0).px - h.get(1).px),
                },
                {
                        BigDecimal.valueOf(0L),
                        BigDecimal.valueOf(0L),
                        BigDecimal.valueOf(h.get(2).vz - h.get(3).vz),
                        BigDecimal.valueOf(h.get(3).pz - h.get(2).pz),
                        BigDecimal.valueOf(h.get(3).vy - h.get(2).vy),
                        BigDecimal.valueOf(h.get(2).py - h.get(3).py),
                },
                {
                        BigDecimal.valueOf(h.get(3).vy - h.get(2).vy),
                        BigDecimal.valueOf(h.get(2).py - h.get(3).py),
                        BigDecimal.valueOf(h.get(2).vx - h.get(3).vx),
                        BigDecimal.valueOf(h.get(3).px - h.get(2).px),
                        BigDecimal.valueOf(0L),
                        BigDecimal.valueOf(0L),
                },
                {
                        BigDecimal.valueOf(h.get(5).vz - h.get(4).vz),
                        BigDecimal.valueOf(h.get(4).pz - h.get(5).pz),
                        BigDecimal.valueOf(0L),
                        BigDecimal.valueOf(0L),
                        BigDecimal.valueOf(h.get(4).vx - h.get(5).vx),
                        BigDecimal.valueOf(h.get(5).px - h.get(4).px),
                },
                {
                        BigDecimal.valueOf(0L),
                        BigDecimal.valueOf(0L),
                        BigDecimal.valueOf(h.get(5).vz - h.get(4).vz),
                        BigDecimal.valueOf(h.get(4).pz - h.get(5).pz),
                        BigDecimal.valueOf(h.get(4).vy - h.get(5).vy),
                        BigDecimal.valueOf(h.get(5).py - h.get(4).py),
                }
        };

        BigDecimal[] b = {
                BigDecimal.valueOf(h.get(0).vy * h.get(0).px - h.get(1).vy * h.get(1).px + h.get(1).py * h.get(1).vx - h.get(0).py * h.get(0).vx),
                BigDecimal.valueOf(h.get(0).vz * h.get(0).px - h.get(1).vz * h.get(1).px + h.get(1).pz * h.get(1).vx - h.get(0).pz * h.get(0).vx),
                BigDecimal.valueOf(h.get(2).vz * h.get(2).py - h.get(3).vz * h.get(3).py + h.get(3).pz * h.get(3).vy - h.get(2).pz * h.get(2).vy),
                BigDecimal.valueOf(h.get(2).vx * h.get(2).py - h.get(3).vx * h.get(3).py + h.get(3).px * h.get(3).vy - h.get(2).px * h.get(2).vy),
                BigDecimal.valueOf(h.get(4).vx * h.get(4).pz - h.get(5).vx * h.get(5).pz + h.get(5).px * h.get(5).vz - h.get(4).px * h.get(4).vz),
                BigDecimal.valueOf(h.get(4).vy * h.get(4).pz - h.get(5).vy * h.get(5).pz + h.get(5).py * h.get(5).vz - h.get(4).py * h.get(4).vz),
        };

        printMatrix(A, "A");
        printVector(b, "b");

        gauss(A, b);

        printMatrix(A, "A");
        printVector(b, "b");

        BigDecimal[] x = backSubstitution(A, b);
        round(x);
        printVector(x, "x");
        BigDecimal ans = x[0].add(x[2]).add(x[4]);
        log.info("The answer is {}", ans.setScale(0, RoundingMode.HALF_UP));
    }

    private void gauss(BigDecimal[][] A, BigDecimal[] b) {
        final int rows = A.length;
        final int cols = A[0].length;
        if (rows != cols) {
            throw new IllegalArgumentException("Matrix A needs to be square");
        }
        if (rows != b.length) {
            throw new IllegalArgumentException("Vector b must have same number of rows as A");
        }
        for (int pivot = 0; pivot < rows - 1; ++pivot) {
            final BigDecimal pivotValue = A[pivot][pivot];
            log.info("pivoting from A[{}][{}] = [{}]", pivot, pivot, pivotValue);
            for (int row = pivot + 1; row < rows; ++row) {
                final BigDecimal rowValue = A[row][pivot];
                log.debug("eliminating row {}, value={}", row, rowValue);
                if (rowValue.equals(BigDecimal.ZERO)) {
                    continue;
                }
                for (int col = pivot; col < cols; ++col) {
                    BigDecimal newValue = A[row][col].subtract(A[pivot][col].divide(pivotValue, SCALE, RoundingMode.HALF_UP).multiply(rowValue));
                    log.debug("updating A[{}][{}] = {} -> {}", row, col, A[row][col], newValue);
                    log.info("{} - {} / {} * {} = {}", A[row][col], A[row][col], pivotValue, rowValue, newValue);
                    A[row][col] = newValue;
                }
                b[row] = b[row].subtract(b[pivot].divide(pivotValue, SCALE, RoundingMode.HALF_UP).multiply(rowValue));
            }
            printMatrix(A, "A");
        }
    }

    private BigDecimal[] backSubstitution(BigDecimal[][] A, BigDecimal[] b) {
        final int size = A.length;
        final BigDecimal[] x = new BigDecimal[size];

        for (int row = size - 1; row >= 0; --row) {
            // erase all values to the right of the diagonal
            for (int col = row + 1; col < size; ++col) {
                final BigDecimal value = A[row][col];
                b[row] = b[row].subtract(value.multiply(x[col]));
                A[row][col] = BigDecimal.ZERO;
            }
            x[row] = b[row].divide(A[row][row], SCALE, RoundingMode.HALF_UP);
        }

        return x;
    }

    private void round(BigDecimal[] x) {
        for (int i = 0; i < x.length; ++i) {
            x[i] = x[i].setScale(1, RoundingMode.HALF_UP);
        }
    }

    private void printMatrix(BigDecimal[][] A, String symbol) {
        var sb = new StringBuilder("\n");
        for (int row = 0; row < A.length; ++row) {
            for (int col = 0; col < A[0].length; ++col) {
                sb.append(A[row][col]);
                sb.append(" ");
            }
            sb.append("\n");
        }
        log.info("{}={}", symbol, sb);
    }

    private void printVector(BigDecimal[] b, String symbol) {
        var sb = new StringBuilder("\n");
        for (int row = 0; row < b.length; ++row) {
            sb.append(b[row]);
            sb.append("\n");
        }
        log.info("{}={}", symbol, sb);
    }

    private void processLine(String line) {
        var matcher = HAILSTONE_PATTERN.matcher(line);
        if (!matcher.matches()) {
            throw new IllegalArgumentException("%s does not match pattern".formatted(line));
        }
        h.add(new Hailstone(
                Long.parseLong(matcher.group(1)),
                Long.parseLong(matcher.group(2)),
                Long.parseLong(matcher.group(3)),
                Long.parseLong(matcher.group(4)),
                Long.parseLong(matcher.group(5)),
                Long.parseLong(matcher.group(6))
        ));
    }
}
