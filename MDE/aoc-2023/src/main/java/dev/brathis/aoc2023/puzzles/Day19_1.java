package dev.brathis.aoc2023.puzzles;

import dev.brathis.aoc2023.common.PuzzleInputLoader;
import lombok.Data;
import lombok.extern.slf4j.Slf4j;

import java.io.BufferedReader;
import java.io.IOException;
import java.util.*;
import java.util.regex.Pattern;

@Slf4j
public class Day19_1 extends Puzzle {
    public Day19_1(PuzzleInputLoader puzzleInputLoader) {
        super(Day19_1.class, puzzleInputLoader);
    }

    @Data
    private static class Workflow {
        private final List<String> rules;
        private final String defaultDestination;
    }

    @Data
    private static class Rule {
        private final String category;
        private final String operator;
        private final int value;
        private final String destination;

        boolean matches(Rating rating) {
            return applyOperator(getCategory(rating), value);
        }

        private int getCategory(Rating rating) {
            if (category.equals("x")) {
                return rating.x;
            }
            if (category.equals("m")) {
                return rating.m;
            }
            if (category.equals("a")) {
                return rating.a;
            }
            if (category.equals("s")) {
                return rating.s;
            }
            throw new IllegalArgumentException("Invalid category '%s'".formatted(category));
        }

        private boolean applyOperator(int left, int right) {
            if (operator.equals("<")) {
                return left < right;
            } else if (operator.equals(">")) {
                return left > right;
            }
            throw new IllegalStateException("Unknown operator '%s'".formatted(operator));
        }
    }

    @Data
    private static class Rating {
        private final int x;
        private final int m;
        private final int a;
        private final int s;

        int sum() {
            return x + m + a + s;
        }
    }
    private static final Pattern WORKFLOW_PATTERN = Pattern.compile("^(?<workflowName>[a-z]+)\\{(?<rules>([xmas][<>]\\d+:[a-zAR]+,)+)(?<default>[a-zAR]+)}$");
    private static final Pattern RATING_PATTERN = Pattern.compile("^\\{x=(?<x>\\d+),m=(?<m>\\d+),a=(?<a>\\d+),s=(?<s>\\d+)}");
    private static final Pattern RULE_PATTERN = Pattern.compile("^(?<category>[xmas])(?<operator>[<>])(?<value>\\d+):(?<destination>[a-zAR]+)$");
    private static final String START_WORKFLOW_NAME = "in";
    boolean inputRulesComplete = false;
    private final Map<String, Workflow> workflows = new HashMap<>();
    private final List<Rating> ratings = new LinkedList<>();

    @Override
    void puzzle(BufferedReader puzzleInput) throws IOException {
        String line = puzzleInput.readLine();
        while (line != null) {
            if (line.isEmpty()) {
                inputRulesComplete = true;
            } else {
                processLine(line);
            }
            line = puzzleInput.readLine();
        }

        int sum = 0;
        for (var rating : ratings) {
            String decision = processRating(rating);
            log.info("Rating {}: {}", rating, decision);
            if (decision.equals("A")) {
                sum += rating.sum();
            }
        }
        log.info("The answer is {}", sum);
    }

    private void processLine(String line) {
        if (inputRulesComplete) {
            processLineRating(line);
        } else {
            processLineWorkflow(line);
        }
    }

    private void processLineWorkflow(String line) {
        final var matcher = WORKFLOW_PATTERN.matcher(line);
        if (!matcher.matches()) {
            throw new IllegalArgumentException("'%s' does not match rule pattern".formatted(line));
        }
        final var workflowName = matcher.group("workflowName");
        final var rules = matcher.group("rules");
        final var defaultRule = matcher.group("default");
        log.info("{}: {} default={}", workflowName, rules, defaultRule);
        workflows.put(workflowName, new Workflow(Arrays.asList(rules.split(",")), defaultRule));
    }

    private void processLineRating(String line) {
        final var matcher = RATING_PATTERN.matcher(line);
        if (!matcher.matches()) {
            throw new IllegalArgumentException("'%s' does not match rating pattern".formatted(line));
        }
        final var x = Integer.parseInt(matcher.group("x"));
        final var m = Integer.parseInt(matcher.group("m"));
        final var a = Integer.parseInt(matcher.group("a"));
        final var s = Integer.parseInt(matcher.group("s"));
        log.info("x={}, m={}, a={}, s={}", x, m, a, s);
        ratings.add(new Rating(x, m, a, s));
    }

    private String processRating(Rating rating) {
        String workflowName = START_WORKFLOW_NAME;
        while (!Set.of("A", "R").contains(workflowName)) {
            Workflow workflow = workflows.get(workflowName);
            workflowName = applyWorkflow(workflow, rating);
        }
        return workflowName;
    }

    private String applyWorkflow(Workflow workflow, Rating rating) {
        for (var ruleString : workflow.rules) {
            Rule rule = parseRuleString(ruleString);
            if (rule.matches(rating)) {
                return rule.destination;
            }
        }
        return workflow.defaultDestination;
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
