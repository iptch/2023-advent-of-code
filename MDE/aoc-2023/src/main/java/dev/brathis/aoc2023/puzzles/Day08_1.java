package dev.brathis.aoc2023.puzzles;

import dev.brathis.aoc2023.common.PuzzleInputLoader;
import lombok.extern.slf4j.Slf4j;

import java.io.BufferedReader;
import java.io.IOException;
import java.util.HashMap;
import java.util.Map;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

@Slf4j
public class Day08_1 extends Puzzle {
    public Day08_1(PuzzleInputLoader puzzleInputLoader) {
        super(Day08_1.class, puzzleInputLoader);
    }

    private static final Pattern NODES_PATTERN = Pattern.compile("(?<node>[A-Z]{3}) = \\((?<left>[A-Z]{3}), (?<right>[A-Z]{3})\\)");

    private record Node(String node, String left, String right) {}

    private enum ParserState {
        RIGHT_LEFT,
        NODES
    }

    private ParserState parserState = ParserState.RIGHT_LEFT;
    private String instructions;

    private Map<String, Node> nodes = new HashMap<>();
    private Node currentNode;
    private int currentInstructionIndex = 0;

    @Override
    void puzzle(BufferedReader puzzleInput) throws IOException {
        String line = puzzleInput.readLine();
        while (line != null) {
            if (!line.isEmpty()) {
                processLine(line);
            }
            line = puzzleInput.readLine();
        }

        log.info("Instructions: {}", instructions);
        log.info("Nodes: {}", nodes);
        currentNode = nodes.get("AAA");
        long requiredSteps = 0L;
        while (!currentNode.node.equals("ZZZ")) {
            log.info("Step {} node {}", requiredSteps, currentNode.node);
            if (instructions.charAt(currentInstructionIndex) == 'L') {
                currentNode = nodes.get(currentNode.left);
            } else {
                currentNode = nodes.get(currentNode.right);
            }
            ++requiredSteps;
            currentInstructionIndex = (currentInstructionIndex + 1) % instructions.length();
        }
        log.info("Found ZZZ after {} steps", requiredSteps);
    }

    private void processLine(String line) {
        if (parserState.equals(ParserState.RIGHT_LEFT)) {
            processLineRightLeft(line);
            parserState = ParserState.NODES;
        } else {
            processLineNodes(line);
        }
    }

    private void processLineRightLeft(String line) {
        instructions = line;
    }

    private void processLineNodes(String line) {
        Matcher lineMatcher = NODES_PATTERN.matcher(line);
        if (!lineMatcher.matches()) {
            throw new RuntimeException("Line '%s' does not match pattern".formatted(line));
        }
        Node node = new Node(lineMatcher.group("node"), lineMatcher.group("left"), lineMatcher.group("right"));
        nodes.put(node.node, node);
    }
}
