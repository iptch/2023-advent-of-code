package dev.brathis.aoc2023.puzzles;

import dev.brathis.aoc2023.common.PuzzleInputLoader;
import lombok.extern.slf4j.Slf4j;
import org.jgrapht.Graph;
import org.jgrapht.alg.StoerWagnerMinimumCut;
import org.jgrapht.graph.DefaultEdge;
import org.jgrapht.graph.DefaultUndirectedGraph;

import java.io.BufferedReader;
import java.io.IOException;
import java.util.regex.Pattern;

@Slf4j
public class Day25_1 extends Puzzle {
    public Day25_1(PuzzleInputLoader puzzleInputLoader) {
        super(Day25_1.class, puzzleInputLoader);
    }

    private static final Pattern NODE_PATTERN = Pattern.compile("^(?<node>[a-z]{3}): (?<adjacentNodes>([a-z]{3} ?)+)$");

    private final Graph<String, DefaultEdge> graph = new DefaultUndirectedGraph<>(DefaultEdge.class);

    @Override
    void puzzle(BufferedReader puzzleInput) throws IOException {
        String line = puzzleInput.readLine();
        while (line != null) {
            var matcher = NODE_PATTERN.matcher(line);
            if (!matcher.matches()) {
                throw new IllegalArgumentException("'%s' does not match pattern".formatted(line));
            }

            String v = matcher.group("node");
            graph.addVertex(v);
            for (var n : matcher.group("adjacentNodes").split(" ")) {
                if (!graph.containsVertex(n)) {
                    graph.addVertex(n);
                }
                graph.addEdge(v, n);
            }

            line = puzzleInput.readLine();
        }

        var vertices = graph.vertexSet().size();
        var alg = new StoerWagnerMinimumCut<>(graph);
        int minCutSize = alg.minCut().size();
        log.info("Min cut size is {}", minCutSize);
        log.info("The answer is {}", minCutSize * (vertices - minCutSize));
    }
}
