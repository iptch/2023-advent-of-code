package dev.brathis.aoc2023.puzzles;

import dev.brathis.aoc2023.common.PuzzleInputLoader;
import lombok.extern.slf4j.Slf4j;

import java.io.BufferedReader;
import java.io.IOException;
import java.util.HashMap;
import java.util.LinkedList;
import java.util.List;
import java.util.Map;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

@Slf4j
public class Day02_2 extends Puzzle {
    public Day02_2(PuzzleInputLoader puzzleInputLoader) {
        super(Day02_2.class, puzzleInputLoader);
    }

    private enum Color {
        RED,
        GREEN,
        BLUE
    }

    private record ColorDraw(Color color, Integer quantity) {};
    private record Draw(List<ColorDraw> colors) {};
    private static final Pattern GAME_ID_PATTERN = Pattern.compile("^Game (?<gameId>\\d+)");
    private static final Pattern DRAW_PATTERN = Pattern.compile("(?<draw>(\\d+ (red|green|blue)(, )?)+(; )?)");
    private static final Pattern COLOR_DRAW_PATTERN = Pattern.compile("(?<quantity>\\d+) (?<color>red|green|blue)(, )?");
    private static final Map<Color, Integer> AVAILABLE_GEMS = Map.of(
            Color.RED, 12,
            Color.GREEN, 13,
            Color.BLUE, 14
    );

    @Override
    void puzzle(BufferedReader puzzleInput) throws IOException {
        String line = puzzleInput.readLine();
        int sum = 0;
        while (line != null) {
            sum += processLine(line);
            line = puzzleInput.readLine();
        }
        log.info("The answer is {}", sum);
    }

    private int processLine(String line) {
        int gameId = getGameId(line);
        List<Draw> draws = getDraws(line);
        Map<Color, Integer> minimumSet = getMinimumSet(draws);
        log.info("game {} requires at least {}", gameId, minimumSet);
        return getPower(minimumSet);
    }

    private List<Draw> getDraws(String line) {
        Matcher drawMatcher = DRAW_PATTERN.matcher(line);
        List<Draw> draws = new LinkedList<>();
        while (drawMatcher.find()) {
            String drawString = drawMatcher.group("draw");
            log.debug("Found draw: {}", drawString);
            List<ColorDraw> colorDraws = getColorDraws(drawString);
            draws.add(new Draw(colorDraws));
        }
        return draws;
    }

    private List<ColorDraw> getColorDraws(String draw) {
        Matcher colorDrawMatcher = COLOR_DRAW_PATTERN.matcher(draw);
        List<ColorDraw> colorDraws = new LinkedList<>();
        while (colorDrawMatcher.find()) {
            var colorDraw = new ColorDraw(Color.valueOf(colorDrawMatcher.group("color").toUpperCase()), Integer.parseInt(colorDrawMatcher.group("quantity")));
            colorDraws.add(colorDraw);
            log.debug("Found color draw with color {} quantity {}", colorDraw.color, colorDraw.quantity);
        }
        return colorDraws;
    }

    private int getGameId(String line) {
        Matcher gameIdMatcher = GAME_ID_PATTERN.matcher(line);
        if (!gameIdMatcher.find()) {
            log.error("Failed to match line '{}'", line);
            throw new RuntimeException();
        }
        int gameId = Integer.parseInt(gameIdMatcher.group("gameId"));
        log.debug("found game ID {}", gameId);
        return gameId;
    }

    private Map<Color, Integer> getMinimumSet(List<Draw> draws) {
        Map<Color, Integer> minimumSet = new HashMap<>(Map.of(
                Color.RED, 0,
                Color.GREEN, 0,
                Color.BLUE, 0
        ));
        for (var draw : draws) {
            for (var colorDraw : draw.colors) {
                minimumSet.put(colorDraw.color, Math.max(minimumSet.get(colorDraw.color), colorDraw.quantity));
            }
        }
        return minimumSet;
    }

    private int getPower(Map<Color, Integer> minimumSet) {
        return minimumSet.values().stream()
                .mapToInt(Integer::intValue)
                .reduce(1, (a, b) -> a * b);
    }
}
