package dev.brathis.aoc2023.puzzles;

import dev.brathis.aoc2023.common.PuzzleInputLoader;
import lombok.extern.slf4j.Slf4j;

import java.io.BufferedReader;
import java.io.IOException;
import java.util.*;
import java.util.stream.Collectors;

@Slf4j
public class Day13_2 extends Puzzle {
    public Day13_2(PuzzleInputLoader puzzleInputLoader) {
        super(Day13_2.class, puzzleInputLoader);
    }

    private enum MirrorType {
        HORIZONTAL,
        VERTICAL,
    }

    private record Smudge(int rowIdx, int colIdx) {
    }

    private record Mirror(MirrorType type, int rowOrColIdx) {
        int getScore() {
            return type.equals(MirrorType.HORIZONTAL) ? 100 * rowOrColIdx : rowOrColIdx;
        }
    }

    private record Pattern(List<String> rows) {
        int getWidth() {
            return rows.get(0).length();
        }

        int getHeight() {
            return rows.size();
        }

        String getRow(int idx) {
            return rows.get(idx);
        }

        String getColumn(int idx) {
            return rows.stream()
                    .map(row -> String.valueOf(row.charAt(idx)))
                    .collect(Collectors.joining());
        }

        @Override
        public String toString() {
            StringBuilder builder = new StringBuilder("\n");
            for (var row : rows) {
                builder.append(row);
                builder.append("\n");
            }
            return builder.toString();
        }
    }

    private final List<Pattern> patterns = new ArrayList<>();
    private Pattern currentPattern = null;

    @Override
    void puzzle(BufferedReader puzzleInput) throws IOException {
        String line = puzzleInput.readLine();
        while (line != null) {
            if (!line.isEmpty()) {
                processLine(line);
            } else {
                completePattern();
            }
            line = puzzleInput.readLine();
        }
        completePattern();

        log.info("Found {} patterns", patterns.size());

        int score = 0;
        for (var pattern : patterns) {
            Set<Mirror> mirrors = findMirrors(pattern);
            if (mirrors.isEmpty()) {
                throw new RuntimeException("Did not find a mirror");
            }
            if (mirrors.size() > 1) {
                throw new RuntimeException("Found %d mirrors".formatted(mirrors.size()));
            }
            Mirror mirror = mirrors.iterator().next();
            List<Smudge> smudgeCandidates = findSmudgeCandidates(pattern);
            if (smudgeCandidates.isEmpty()) {
                throw new RuntimeException("Did not find smudge candidates");
            }
            log.info("Found original mirror {} with smudge candidates {}", mirror, smudgeCandidates);

            boolean foundNewMirror = false;
            for (var smudge : smudgeCandidates) {
                log.info("Testing smudge {}", smudge);
                Pattern patternWithoutSmudge = getPatternWithoutSmudge(pattern, smudge);
                log.debug("Pattern: {}", patternWithoutSmudge);
                Set<Mirror> mirrorsForPatternWithoutSmudge = findMirrors(patternWithoutSmudge);
                Set<Mirror> newMirrors = findNewMirrors(mirrorsForPatternWithoutSmudge, mirror);
                if (!newMirrors.isEmpty()) {
                    if (newMirrors.size() > 1) {
                        throw new RuntimeException("Found %d new mirrors".formatted(newMirrors.size()));
                    }
                    Mirror newMirror = newMirrors.iterator().next();
                    log.info("Found new mirror {}", newMirror);
                    score += newMirror.getScore();
                    foundNewMirror = true;
                    break;
                }
            }
            if (!foundNewMirror) {
                throw new RuntimeException("Could not find new mirror");
            }
        }
        log.info("The answer is {}", score);
    }

    Set<Mirror> findNewMirrors(Set<Mirror> foundMirrors, Mirror existingMirror) {
        Set<Mirror> newMirrors = new HashSet<>(foundMirrors);
        newMirrors.remove(existingMirror);
        return newMirrors;
    }

    List<Smudge> findSmudgeCandidates(Pattern pattern) {
        List<Smudge> smudgeCandidates = new LinkedList<>();
        for (int rowIdxA = 0; rowIdxA < pattern.getHeight(); ++rowIdxA) {
            for (int rowIdxB = rowIdxA + 1; rowIdxB < pattern.getHeight(); ++rowIdxB) {
                // Check for almost matches, where the rows differ in exactly one position and save that position.
                Integer smudge = findSmudge(pattern.getRow(rowIdxA), pattern.getRow(rowIdxB));
                if (smudge != null) {
                    log.debug("Rows\n{} (idx {})\n{} (idx {})\nhave possible smudge at column idx {}",
                            pattern.getRow(rowIdxA), rowIdxA,
                            pattern.getRow(rowIdxB), rowIdxB,
                            smudge
                    );
                    smudgeCandidates.add(new Smudge(rowIdxA, smudge));
                    smudgeCandidates.add(new Smudge(rowIdxB, smudge));
                }
            }
        }
        for (int colIdxA = 0; colIdxA < pattern.getWidth(); ++colIdxA) {
            for (int colIdxB = colIdxA + 1; colIdxB < pattern.getWidth(); ++colIdxB) {
                // Check for almost matches, where the columns differ in exactly one position and save that position.
                Integer smudge = findSmudge(pattern.getColumn(colIdxA), pattern.getColumn(colIdxB));
                if (smudge != null) {
                    log.debug("Columns\n{} (idx {})\n{} (idx {})\nhave possible smudge at row idx {}",
                            pattern.getColumn(colIdxA), colIdxA,
                            pattern.getColumn(colIdxB), colIdxB,
                            smudge
                    );
                    smudgeCandidates.add(new Smudge(smudge, colIdxA));
                    smudgeCandidates.add(new Smudge(smudge, colIdxB));
                }
            }
        }
        return smudgeCandidates;
    }

    Pattern getPatternWithoutSmudge(Pattern pattern, Smudge smudge) {
        Pattern newPattern = new Pattern(new ArrayList<>());
        for (int rowIdx = 0; rowIdx < pattern.getHeight(); ++rowIdx) {
            if (rowIdx == smudge.rowIdx) {
                StringBuilder stringBuilder = new StringBuilder();
                for (int colIdx = 0; colIdx < pattern.getWidth(); ++colIdx) {
                    char originalChar = pattern.rows.get(rowIdx).charAt(colIdx);
                    if (colIdx == smudge.colIdx) {
                        stringBuilder.append(originalChar == '.' ? '#' : '.');
                    } else {
                        stringBuilder.append(originalChar);
                    }
                }
                newPattern.rows.add(stringBuilder.toString());
            } else {
                newPattern.rows.add(pattern.rows.get(rowIdx));
            }
        }
        return newPattern;
    }

    Set<Mirror> findMirrors(Pattern pattern) {
        Set<Mirror> mirrors = new HashSet<>();
        List<Integer> horizontalMirrorIndices = findHorizontalMirrors(pattern);
        List<Integer> verticalMirrorIndices = findVerticalMirrors(pattern);
        horizontalMirrorIndices.forEach(idx -> mirrors.add(new Mirror(MirrorType.HORIZONTAL, idx)));
        verticalMirrorIndices.forEach(idx -> mirrors.add(new Mirror(MirrorType.VERTICAL, idx)));
        return mirrors;
    }

    void processLine(String line) {
        if (currentPattern == null) {
            currentPattern = new Pattern(new ArrayList<>());
        }
        currentPattern.rows.add(line);
    }

    void completePattern() {
        patterns.add(currentPattern);
        currentPattern = null;
    }

    List<Integer> findHorizontalMirrors(Pattern pattern) {
        List<Integer> lowerReflectionLines = new LinkedList<>();
        int mirrorTop = 0;
        int mirrorBottom = 1;
        while (mirrorBottom < pattern.getHeight()) {
            if (patternHasHorizontalMirrorAt(pattern, mirrorTop, mirrorBottom)) {
                log.debug("Found horizontal mirror at ({}, {})", mirrorTop, mirrorBottom);
                lowerReflectionLines.add(mirrorBottom);
            }
            ++mirrorTop;
            ++mirrorBottom;
        }
        return lowerReflectionLines;
    }

    boolean patternHasHorizontalMirrorAt(Pattern pattern, int mirrorTop, int mirrorBottom) {
        int cursorTop = mirrorTop;
        int cursorBottom = mirrorBottom;
        while (cursorTop >= 0 && cursorBottom < pattern.getHeight()) {
            if (!pattern.getRow(cursorTop).equals(pattern.getRow(cursorBottom))) {
                return false;
            }
            --cursorTop;
            ++cursorBottom;
        }
        return true;
    }

    Integer findSmudge(String a, String b) {
        List<Integer> smudges = new LinkedList<>();
        for (int i = 0; i < a.length(); ++i) {
            if (a.charAt(i) != b.charAt(i)) {
                smudges.add(i);
                if (smudges.size() > 1) {
                    return null;
                }
            }
        }
        if (!smudges.isEmpty()) {
            return smudges.get(0);
        }
        return null;
    }

    List<Integer> findVerticalMirrors(Pattern pattern) {
        List<Integer> rightReflectionLines = new LinkedList<>();
        int mirrorLeft = 0;
        int mirrorRight = 1;
        while (mirrorRight < pattern.getWidth()) {
            if (patternHasVerticalMirrorAt(pattern, mirrorLeft, mirrorRight)) {
                log.debug("Found vertical mirror at ({}, {})", mirrorLeft, mirrorRight);
                rightReflectionLines.add(mirrorRight);
            }
            ++mirrorLeft;
            ++mirrorRight;
        }
        return rightReflectionLines;
    }

    boolean patternHasVerticalMirrorAt(Pattern pattern, int mirrorLeft, int mirrorRight) {
        int cursorLeft = mirrorLeft;
        int cursorRight = mirrorRight;
        while (cursorLeft >= 0 && cursorRight < pattern.getWidth()) {
            if (!pattern.getColumn(cursorLeft).equals(pattern.getColumn(cursorRight))) {
                return false;
            }
            --cursorLeft;
            ++cursorRight;
        }
        return true;
    }
}
