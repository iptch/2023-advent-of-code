package dev.brathis.aoc2023.puzzles;

import dev.brathis.aoc2023.common.PuzzleInputLoader;
import lombok.extern.slf4j.Slf4j;

import java.io.BufferedReader;
import java.io.IOException;
import java.util.*;
import java.util.regex.Matcher;
import java.util.regex.Pattern;


@Slf4j
public class Day08_2 extends Puzzle {
    public Day08_2(PuzzleInputLoader puzzleInputLoader) {
        super(Day08_2.class, puzzleInputLoader);
    }

    private static final Pattern NODES_PATTERN = Pattern.compile("(?<node>[A-Z\\d]{3}) = \\((?<left>[A-Z\\d]{3}), (?<right>[A-Z\\d]{3})\\)");

    private record Node(String node, String left, String right) {
        boolean isStartNode() {
            return node.charAt(2) == 'A';
        }

        boolean isEndNode() {
            return node.charAt(2) == 'Z';
        }
    }

    private enum ParserState {
        RIGHT_LEFT,
        NODES
    }

    private ParserState parserState = ParserState.RIGHT_LEFT;
    private String instructions;
    private final List<Node> currentNodes = new LinkedList<>();
    private final Map<String, Node> nodes = new HashMap<>();

    @Override
    void puzzle(BufferedReader puzzleInput) throws IOException {
        String line = puzzleInput.readLine();
        while (line != null) {
            if (!line.isEmpty()) {
                processLine(line);
            }
            line = puzzleInput.readLine();
        }

        log.info("Instructions: {}", instructions.length());
        log.info("Nodes: {}", nodes.size());
        log.info("Starting nodes: {}", currentNodes.size());
        Set<Integer> cycles = new HashSet<>();

        for (final var startingNode : currentNodes) {
            List<Integer> terminalCycles = new ArrayList<>();
            int it = 0;
            var node = startingNode;
            while (terminalCycles.size() < 2) {
                if (node.isEndNode()) {
                    terminalCycles.add(it);
                }
                char instruction = instructions.charAt(it % instructions.length());
                if (instruction == 'L') {
                    node = nodes.get(node.left);
                } else {
                    node = nodes.get(node.right);
                }
                ++it;
            }
            int remainder = terminalCycles.get(1) % terminalCycles.get(0);
            log.info("{} hits terminal node after {} and {} iterations, remainder={}", startingNode.node, terminalCycles.get(0), terminalCycles.get(1), remainder);
            assert remainder == 0;  // LCM only works if there is no offset
            cycles.add(terminalCycles.get(0));
        }

        log.info("The answer is {}", lcm(cycles.stream().mapToLong(l -> (long) l).toArray()));
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
        if (node.isStartNode()) {
            currentNodes.add(node);
        }
        nodes.put(node.node, node);
    }

    // thanks, StackOverflow: https://stackoverflow.com/a/4202114
    private static long gcd(long a, long b) {
        while (b > 0) {
            long temp = b;
            b = a % b;
            a = temp;
        }
        return a;
    }

    private static long lcm(long a, long b) {
        return a * (b / gcd(a, b));
    }

    private static long lcm(long[] input) {
        long result = input[0];
        for (int i = 1; i < input.length; i++) result = lcm(result, input[i]);
        return result;
    }
}
