package dev.brathis.aoc2023.puzzles;

import dev.brathis.aoc2023.common.PuzzleInputLoader;
import lombok.extern.slf4j.Slf4j;

import java.io.BufferedReader;
import java.io.IOException;
import java.util.*;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

@Slf4j
public class Day15_2 extends Puzzle {
    public Day15_2(PuzzleInputLoader puzzleInputLoader) {
        super(Day15_2.class, puzzleInputLoader);
    }

    private static final Pattern STEP_PATTERN = Pattern.compile("^(?<label>[a-z]+)(?<op>[-=])(?<focalLength>\\d?)$");

    private record Lens(String label, int focalLength) {
    }

    private final Map<Integer, List<Lens>> boxes = new HashMap<>();

    @Override
    void puzzle(BufferedReader puzzleInput) throws IOException {
        String line = puzzleInput.readLine();
        processInput(line).forEach(this::handleStep);

        int totalFocusingPower = 0;
        for (int boxHash = 0; boxHash < 256; ++boxHash) {
            if (boxes.containsKey(boxHash)) {
                List<Lens> lenses = boxes.get(boxHash);
                for (int lensIdx = 0; lensIdx < lenses.size(); ++lensIdx) {
                    log.debug("Processing box {} lens {}", boxHash, lensIdx);
                    totalFocusingPower += (boxHash + 1) * (lensIdx + 1) * lenses.get(lensIdx).focalLength();
                }
            }
        }
        log.info("The answer is {}", totalFocusingPower);
    }

    List<String> processInput(String input) {
        return Arrays.asList(input.split(","));
    }

    private void handleStep(String input) {
        Matcher matcher = STEP_PATTERN.matcher(input);
        if (!matcher.matches()) {
            throw new RuntimeException("Step '%s' does not match pattern".formatted(input));
        }
        String label = matcher.group("label");
        int boxHash = doHash(label);

        if (matcher.group("op").equals("=")) {
            int focalLength = Integer.parseInt(matcher.group("focalLength"));
            upsertLens(boxHash, label, focalLength);
        } else {
            removeLens(boxHash, label);
        }
    }

    private void upsertLens(int boxHash, String label, int focalLength) {
        log.debug("upsertLens(boxHash={} label={} focalLength={})", boxHash, label, focalLength);
        if (!boxes.containsKey(boxHash)) {
            boxes.put(boxHash, new LinkedList<>());
        }
        List<Lens> lenses = boxes.get(boxHash);
        Lens newLens = new Lens(label, focalLength);
        int lensIdx = getLensIdx(lenses, label);
        if (lensIdx == -1) {
            lenses.add(newLens);
        } else {
            lenses.set(lensIdx, newLens);
        }
    }

    private void removeLens(int boxHash, String label) {
        log.debug("removeLens(boxHash={} label={})", boxHash, label);
        if (boxes.containsKey(boxHash)) {
            List<Lens> lenses = boxes.get(boxHash);
            lenses.removeIf(lens -> lens.label().equals(label));
        }
    }

    private int doHash(String input) {
        int currentValue = 0;
        for (char c : input.toCharArray()) {
            currentValue += (int) c;
            currentValue *= 17;
            currentValue %= 256;
        }
        log.debug("HASH of {} is {}", input, currentValue);
        return currentValue;
    }

    private int getLensIdx(List<Lens> lenses, String label) {
        for (int i = 0; i < lenses.size(); ++i) {
            Lens lens = lenses.get(i);
            if (lens.label().equals(label)) {
                return i;
            }
        }
        return -1;
    }
}
