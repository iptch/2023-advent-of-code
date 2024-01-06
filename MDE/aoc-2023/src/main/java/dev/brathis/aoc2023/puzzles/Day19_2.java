package dev.brathis.aoc2023.puzzles;

import dev.brathis.aoc2023.common.PuzzleInputLoader;
import lombok.Data;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;

import java.io.BufferedReader;
import java.io.IOException;
import java.util.*;
import java.util.regex.Pattern;
import java.util.stream.Stream;

@Slf4j
public class Day19_2 extends Puzzle {
    public Day19_2(PuzzleInputLoader puzzleInputLoader) {
        super(Day19_2.class, puzzleInputLoader);
    }

    @Data
    private static class Workflow {
        private final List<Rule> rules;
        private final String defaultDestination;
    }

    @Data
    private static class Rule {
        private final String category;
        private final String operator;
        private final int value;
        private final String destination;

        Rule invert() {
            return new Rule(
                    category,
                    operator.equals(">") ? "<" : ">",
                    operator.equals(">") ? value + 1 : value - 1,
                    destination
            );
        }
    }

    @Data
    @RequiredArgsConstructor
    private static class Range {
        private final int start;    // inclusive
        private final int end;      // exclusive

        static Range initial() {
            return new Range(1, 4001);
        }

        boolean isEmpty() {
            return start >= end;
        }

        long size() {
            if (isEmpty()) {
                return 0;
            }
            return end - start;
        }

        Range reduce(Rule rule) {
            var value = rule.value;
            var operator = rule.operator;
            if (operator.equals(">")) {
                return new Range(Math.max(value + 1, start), end);
            } else if (operator.equals("<")) {
                return new Range(start, Math.min(value, end));
            }
            throw new IllegalArgumentException("Invalid operator '%s'".formatted(operator));
        }

        @Override
        public String toString() {
            return "[%d,%d)".formatted(start, end);
        }
    }

    @Data
    @RequiredArgsConstructor
    private static class Path {
        private final String workflow;
        private final Range x;
        private final Range m;
        private final Range a;
        private final Range s;

        boolean isEmpty() {
            return Stream.of(x, m, a, s).anyMatch(Range::isEmpty);
        }

        long size() {
            return x.size() * m.size() * a.size() * s.size();
        }
    }

    private static final Pattern WORKFLOW_PATTERN = Pattern.compile("^(?<workflowName>[a-z]+)\\{(?<rules>([xmas][<>]\\d+:[a-zAR]+,)+)(?<default>[a-zAR]+)}$");
    private static final Pattern RULE_PATTERN = Pattern.compile("^(?<category>[xmas])(?<operator>[<>])(?<value>\\d+):(?<destination>[a-zAR]+)$");
    private static final String START_WORKFLOW_NAME = "in";
    private static final String END_WORKFLOW_NAME = "A";
    private final Map<String, Workflow> workflows = new HashMap<>();
    private final Queue<Path> paths = new LinkedList<>();
    private final List<Path> solutions = new LinkedList<>();

    @Override
    void puzzle(BufferedReader puzzleInput) throws IOException {
        String line = puzzleInput.readLine();
        while (line != null && !line.isEmpty()) {
            processLine(line);
            line = puzzleInput.readLine();
        }

        paths.add(new Path(START_WORKFLOW_NAME, Range.initial(), Range.initial(), Range.initial(), Range.initial()));
        while (!paths.isEmpty()) {
            Path path = paths.remove();
            if (path.workflow.equals(END_WORKFLOW_NAME)) {
                solutions.add(path);
                continue;
            }

            Workflow workflow = workflows.get(path.workflow);
            if (workflow == null) {
                continue;
            }

            Path remainder = new Path(
                    workflow.defaultDestination,
                    path.x,
                    path.m,
                    path.a,
                    path.s
            );

            for (var rule : workflow.rules) {
                Path newPath = new Path(
                        rule.destination,
                        rule.category.equals("x") ? remainder.x.reduce(rule) : remainder.x,
                        rule.category.equals("m") ? remainder.m.reduce(rule) : remainder.m,
                        rule.category.equals("a") ? remainder.a.reduce(rule) : remainder.a,
                        rule.category.equals("s") ? remainder.s.reduce(rule) : remainder.s
                );

                if (!newPath.isEmpty()) {
                    log.debug("{} -> {}", path.workflow, newPath);
                    paths.add(newPath);
                }

                remainder = new Path(
                        workflow.defaultDestination,
                        rule.category.equals("x") ? remainder.x.reduce(rule.invert()) : remainder.x,
                        rule.category.equals("m") ? remainder.m.reduce(rule.invert()) : remainder.m,
                        rule.category.equals("a") ? remainder.a.reduce(rule.invert()) : remainder.a,
                        rule.category.equals("s") ? remainder.s.reduce(rule.invert()) : remainder.s
                );
            }

            if (!remainder.isEmpty()) {
                log.debug("{} -> {} (default)", path.workflow, remainder);
                paths.add(remainder);
            }
        }

        long answer = solutions.stream()
                .mapToLong(Path::size)
                .sum();
        log.info("The answer is {}", answer);
    }

    private void processLine(String line) {
        final var matcher = WORKFLOW_PATTERN.matcher(line);
        if (!matcher.matches()) {
            throw new IllegalArgumentException("'%s' does not match rule pattern".formatted(line));
        }
        final var workflowName = matcher.group("workflowName");
        final var rules = matcher.group("rules");
        final var defaultDestination = matcher.group("default");
        log.info("{}: {} default={}", workflowName, rules, defaultDestination);
        workflows.put(workflowName, new Workflow(Arrays.stream(rules.split(",")).map(this::parseRuleString).toList(), defaultDestination));
    }

    private Rule parseRuleString(String ruleString) {
        var matcher = RULE_PATTERN.matcher(ruleString);
        if (!matcher.matches()) {
            throw new IllegalArgumentException("'%s' does not match rule pattern".formatted(ruleString));
        }
        return new Rule(
                matcher.group("category"),
                matcher.group("operator"),
                Integer.parseInt(matcher.group("value")),
                matcher.group("destination")
        );
    }
}
