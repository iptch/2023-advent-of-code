package dev.brathis.aoc2023.puzzles;

import dev.brathis.aoc2023.common.PuzzleInputLoader;
import lombok.extern.slf4j.Slf4j;

import java.io.BufferedReader;
import java.io.IOException;
import java.util.*;
import java.util.regex.Matcher;
import java.util.regex.Pattern;
import java.util.stream.Collectors;

@Slf4j
public class Day12_1 extends Puzzle {
    public Day12_1(PuzzleInputLoader puzzleInputLoader) {
        super(Day12_1.class, puzzleInputLoader);
    }

    private record ConditionRecord(String springs, List<Integer> errorCorrection) {}

    private static final Pattern RECORD_PATTERN = Pattern.compile("^(?<springs>[.#?]+) (?<errorCorrection>(\\d+,?)+)$");

    private final List<ConditionRecord> conditionRecords = new LinkedList<>();

    @Override
    void puzzle(BufferedReader puzzleInput) throws IOException {
        parseConditionRecords(puzzleInput);
        log.info("Read condition records: {}", conditionRecords);
        long totalMatchingVariants = 0;
        for (var conditionRecord : conditionRecords) {
            Set<String> variants = generateVariants(conditionRecord.springs);
            Pattern pattern = generateRegex(conditionRecord.errorCorrection);
            log.info("Generated {} variants and pattern {} for input {}", variants.size(), pattern, conditionRecord.springs);
            long matchingVariants = variants.stream()
                    .map(pattern::matcher)
                    .filter(Matcher::matches)
                    .count();
            log.info("{} variants match", matchingVariants);
            totalMatchingVariants += matchingVariants;
        }
        log.info("The answer is {}", totalMatchingVariants);
    }

    private void parseConditionRecords(BufferedReader puzzleInput) throws IOException {
        String line = puzzleInput.readLine();
        while (line != null) {
            Matcher matcher = RECORD_PATTERN.matcher(line);
            if (!matcher.matches()) {
                throw new RuntimeException("Line '%s' did not match".formatted(line));
            }
            List<Integer> errorCorrection = Arrays.stream(matcher.group("errorCorrection").split(","))
                    .mapToInt(Integer::parseInt)
                    .boxed()
                    .toList();
            conditionRecords.add(new ConditionRecord(matcher.group("springs"), errorCorrection));
            line = puzzleInput.readLine();
        }
    }

    private Set<String> generateVariants(String conditionReport) {
        if (!conditionReport.contains("?")) {
            return Set.of(conditionReport);
        }
        String working = conditionReport.replaceFirst("\\?", ".");
        String broken = conditionReport.replaceFirst("\\?", "#");
        Set<String> variants = new HashSet<>();
        variants.addAll(generateVariants(working));
        variants.addAll(generateVariants(broken));
        return variants;
    }

    private Pattern generateRegex(List<Integer> consecutiveGroups) {
        String groups = consecutiveGroups.stream()
                .map("#{%d}"::formatted)
                .collect(Collectors.joining("\\.+"));
        return Pattern.compile("^\\.*%s\\.*$".formatted(groups));
    }
}
