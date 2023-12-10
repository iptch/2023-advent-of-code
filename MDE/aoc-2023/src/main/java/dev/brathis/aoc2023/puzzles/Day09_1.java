package dev.brathis.aoc2023.puzzles;

import dev.brathis.aoc2023.common.PuzzleInputLoader;
import lombok.extern.slf4j.Slf4j;

import java.io.BufferedReader;
import java.io.IOException;
import java.util.ArrayList;
import java.util.LinkedList;
import java.util.List;
import java.util.Stack;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

@Slf4j
public class Day09_1 extends Puzzle {
    public Day09_1(PuzzleInputLoader puzzleInputLoader) {
        super(Day09_1.class, puzzleInputLoader);
    }

    private record Sequence(List<Integer> series) {
        Sequence reduce() {
            List<Integer> newSeries = new ArrayList<>();
            Integer previous = null;
            for (var val : series) {
                if (previous == null) {
                    previous = val;
                    continue;
                }
                newSeries.add(val - previous);
                previous = val;
            }
            return new Sequence(newSeries);
        }

        boolean isAllZeros() {
            return series.stream().allMatch(i -> i == 0);
        }

        Integer lastValue() {
            return series.stream()
                    .skip(series.size() - 1)
                    .findFirst()
                    .orElse(null);
        }

        Sequence extend(int last) {
            List<Integer> newSeries = new ArrayList<>(series);
            newSeries.add(last);
            return new Sequence(newSeries);
        }

        Sequence extrapolate() {
            Sequence sec = this;
            Stack<Sequence> sequenceStack = new Stack<>();
            while (!sec.isAllZeros()) {
                log.debug("vvv {}", sec);
                sequenceStack.push(sec);
                sec = sec.reduce();
            }
            int lastValue = 0;
            while (!sequenceStack.isEmpty()) {
                log.debug("^^^ {}", sec);
                sec = sequenceStack.pop();
                sec = sec.extend(sec.lastValue() + lastValue);
                lastValue = sec.lastValue();
            }
            return sec;
        }
    }

    private final List<Sequence> sequences = new LinkedList<>();

    @Override
    void puzzle(BufferedReader puzzleInput) throws IOException {
        String line = puzzleInput.readLine();
        while (line != null) {
            if (!line.isEmpty()) {
                processLine(line);
            }
            line = puzzleInput.readLine();
        }

        int answer = 0;
        for (var sequence : sequences) {
            var exSequence = sequence.extrapolate();
            log.info("Extrapolated: {}", exSequence);
            answer += exSequence.lastValue();
        }
        log.info("Answer: {}", answer);
    }

    private void processLine(String line) {
        Matcher lineMatcher = Pattern.compile("-?\\d+").matcher(line);
        List<Integer> series = new ArrayList<>();
        while (lineMatcher.find()) {
            series.add(Integer.parseInt(lineMatcher.group(0)));
        }
        sequences.add(new Sequence(series));
    }
}
