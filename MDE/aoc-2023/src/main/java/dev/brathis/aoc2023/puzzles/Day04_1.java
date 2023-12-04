package dev.brathis.aoc2023.puzzles;

import dev.brathis.aoc2023.common.PuzzleInputLoader;
import lombok.extern.slf4j.Slf4j;

import java.io.BufferedReader;
import java.io.IOException;
import java.util.Arrays;
import java.util.Set;
import java.util.function.Predicate;
import java.util.regex.Matcher;
import java.util.regex.Pattern;
import java.util.stream.Collectors;

@Slf4j
public class Day04_1 extends Puzzle {
    public Day04_1(PuzzleInputLoader puzzleInputLoader) {
        super(Day04_1.class, puzzleInputLoader);
    }

    private static final Pattern CARD_PATTERN = Pattern.compile("^Card\\s+\\d+: (?<winning>.*) \\| (?<selected>.*)");

    private record CardDto(Set<Integer> winning, Set<Integer> selected) {};

    @Override
    void puzzle(BufferedReader puzzleInput) throws IOException {
        String line = puzzleInput.readLine();
        long sum = 0;
        while (line != null) {
            CardDto card = parseCard(line);
            long matches = getMatches(card.winning(), card.selected());
            long score = getScore(matches);
            sum += score;
            log.info("Card: {}, matches: {}", card, matches);
            line = puzzleInput.readLine();
        }
        log.info("The answer is {}", sum);
    }

    private CardDto parseCard(String line) {
        Matcher cardMatcher = CARD_PATTERN.matcher(line);
        if (!cardMatcher.matches()) {
            throw new RuntimeException("Invalid line '%s'".formatted(line));
        }
        Set<Integer> winning = Arrays.stream(cardMatcher.group("winning").split("\\s+"))
                .filter(Predicate.not(String::isBlank))
                .map(Integer::parseInt)
                .collect(Collectors.toSet());
        Set<Integer> selected = Arrays.stream(cardMatcher.group("selected").split("\\s+"))
                .filter(Predicate.not(String::isBlank))
                .map(Integer::parseInt)
                .collect(Collectors.toSet());
        return new CardDto(winning, selected);
    }

    private long getMatches(Set<Integer> winning, Set<Integer> selected) {
        return winning.stream()
                .filter(selected::contains)
                .count();
    }

    private long getScore(long matches) {
        if (matches == 0) {
            return 0;
        }
        return (long) Math.pow(2, matches - 1);
    }
}
