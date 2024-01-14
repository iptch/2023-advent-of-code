package dev.brathis.aoc2023.puzzles;

import dev.brathis.aoc2023.common.PuzzleInputLoader;
import lombok.Data;
import lombok.extern.slf4j.Slf4j;

import java.io.BufferedReader;
import java.io.IOException;
import java.util.ArrayList;
import java.util.LinkedList;
import java.util.List;
import java.util.Objects;
import java.util.regex.Pattern;

@Slf4j
public class Day24_1 extends Puzzle {
    public Day24_1(PuzzleInputLoader puzzleInputLoader) {
        super(Day24_1.class, puzzleInputLoader);
    }

    private static final Pattern HAILSTONE_PATTERN = Pattern.compile("^(-?\\d+),\\s+(-?\\d+),\\s+(-?\\d+)\\s+@\\s+(-?\\d+),\\s+(-?\\d+),\\s+(-?\\d+)$");

    @Data
    private static class Hailstone {
        private final long px;
        private final long py;
        private final long pz;
        private final long vx;
        private final long vy;
        private final long vz;

        Double m() {
            if (vx == 0) {
                return null; // vertical line
            }
            return (double) vy / (double) vx;
        }

        Double q() {
            Double m = m();
            if (m == null) {
                return null;  // vertical line
            }
            return (double) py - (double) px * m;
        }

        Double xIntersection(Hailstone other) {
            Double q1 = q();
            Double m1 = m();
            Double q2 = other.q();
            Double m2 = other.m();
            if (q1 == null && q2 == null) {
                return null; // both lines are vertical, no intercept
            }
            if (q1 == null) { // this line is vertical at px
                return (double) px;
            }
            if (q2 == null) { // other line is vertical at other.px
                return (double) other.px;
            }
            if (m1 == m2) { // both lines are parallel
                return null;
            }
            return (q1 - q2) / (m2 - m1);
        }

        Double yIntersection(Hailstone other) {
            Double x = xIntersection(other);
            if (x == null) {
                return null;
            }
            Double m = m();
            Double q = q();
            if (m == null) {
                // this line is vertical
                return other.m() * x + other.q();
            }
            return m() * x + q();
        }

        Double tForX(double x) {
            if (vx == 0) {
                return null; // hailstone always has constant x
            }
            return (x - (double) px) / (double) vx;
        }

        @Override
        public String toString() {
            return "%d, %d, %d @ %d, %d, %d".formatted(px, py, pz, vx, vy, vz);
        }
    }

    private final List<Hailstone> hailstones = new ArrayList<>();

    @Override
    void puzzle(BufferedReader puzzleInput) throws IOException {
        String line = puzzleInput.readLine();
        while (line != null) {
            processLine(line);
            line = puzzleInput.readLine();
        }
        log.info("Hailstones: {}", hailstones);
        long min = 200000000000000L;
        long max = 400000000000000L;
        long xMin = min;
        long xMax = max;
        long yMin = min;
        long yMax = max;
        int intersections = 0;
        for (int i = 0; i < hailstones.size(); ++i) {
            for (int j = i + 1; j < hailstones.size(); ++j) {
                var a = hailstones.get(i);
                var b = hailstones.get(j);
                var xIntercept = a.xIntersection(b);
                var yIntercept = a.yIntersection(b);
                if (xIntercept != null && yIntercept != null) {
                    log.info("{} and {} intersect at ({},{})", a, b, xIntercept, yIntercept);
                    var ta = a.tForX(xIntercept);
                    var tb = b.tForX(xIntercept);
                    if (ta != null && ta < 0 || tb != null && tb < 0) {
                        log.info("{} and {} intersected in the past", a, b);
                        continue;
                    }
                    if (yMin <= yIntercept && yIntercept <= yMax && xMin <= xIntercept && xIntercept <= xMax) {
                        ++intersections;
                    }
                }
            }
        }
        log.info("The answer is {}", intersections);
    }

    private void processLine(String line) {
        var matcher = HAILSTONE_PATTERN.matcher(line);
        if (!matcher.matches()) {
            throw new IllegalArgumentException("%s does not match pattern".formatted(line));
        }
        hailstones.add(new Hailstone(
                Long.parseLong(matcher.group(1)),
                Long.parseLong(matcher.group(2)),
                Long.parseLong(matcher.group(3)),
                Long.parseLong(matcher.group(4)),
                Long.parseLong(matcher.group(5)),
                Long.parseLong(matcher.group(6))
        ));
    }
}
