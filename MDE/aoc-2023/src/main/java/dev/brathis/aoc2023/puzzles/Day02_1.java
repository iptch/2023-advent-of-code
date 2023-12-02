package dev.brathis.aoc2023.puzzles;

import dev.brathis.aoc2023.common.PuzzleInputLoader;
import lombok.extern.slf4j.Slf4j;

import java.io.BufferedReader;
import java.io.IOException;
import java.util.LinkedList;
import java.util.List;
import java.util.Map;
import java.util.Set;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

@Slf4j
public class Day02_1 extends Puzzle {
    public Day02_1(PuzzleInputLoader puzzleInputLoader) {
        super(Day02_1.class, puzzleInputLoader);
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
        if (isGamePlausible(draws, AVAILABLE_GEMS)) {
            log.info("game {} is plausible", gameId);
            return gameId;
        }
        log.info("game {} is NOT plausible", gameId);
        return 0;
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

    private boolean isGamePlausible(List<Draw> draws, Map<Color, Integer> availableGems) {
        for (var draw : draws) {
            if (!isDrawPlausible(draw, availableGems)) {
                return false;
            }
        }
        return true;
    }

    private boolean isDrawPlausible(Draw draw, Map<Color, Integer> availableGems) {
        for (var colorDraw : draw.colors) {
            if (!isColorDrawPlausible(colorDraw, availableGems)) {
                return false;
            }
            log.debug("color draw {} is plausible", colorDraw);
        }
        return true;
    }

    private boolean isColorDrawPlausible(ColorDraw colorDraw, Map<Color, Integer> availableGems) {
        return availableGems.get(colorDraw.color) >= colorDraw.quantity;
    }
}
