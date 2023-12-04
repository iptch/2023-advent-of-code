package dev.brathis.aoc2023.puzzles;

import dev.brathis.aoc2023.common.PuzzleInputLoader;
import lombok.extern.slf4j.Slf4j;

import java.io.BufferedReader;
import java.io.IOException;
import java.util.Arrays;
import java.util.HashMap;
import java.util.Map;
import java.util.Set;
import java.util.function.Predicate;
import java.util.regex.Matcher;
import java.util.regex.Pattern;
import java.util.stream.Collectors;

@Slf4j
public class Day04_2 extends Puzzle {
    public Day04_2(PuzzleInputLoader puzzleInputLoader) {
        super(Day04_2.class, puzzleInputLoader);
    }

    private static final Pattern CARD_PATTERN = Pattern.compile("^Card\\s+(?<cardNumber>\\d+): (?<winning>.*) \\| (?<selected>.*)");

    private record CardDto(Integer cardNumber, Set<Integer> winning, Set<Integer> selected) {
        public long getMatches() {
            return winning.stream()
                    .filter(selected::contains)
                    .count();
        }
    }

    ;

    private final Map<Integer, CardDto> cardMap = new HashMap<>();
    private final Map<Integer, Integer> cardCollection = new HashMap<>();

    @Override
    void puzzle(BufferedReader puzzleInput) throws IOException {
        buildCardMap(puzzleInput);
        for (var card : cardMap.values()) {
            int matches = (int) card.getMatches();
            int copies = cardCollection.get(card.cardNumber);
            log.debug("{} copies of card {}, each winning {} new cards", copies, card.cardNumber, matches);
            for (int i = 0; i < copies; ++i) {
                winCards(card.cardNumber, matches);
            }
        }
        int result = cardCollection.values().stream()
                .reduce(0, Integer::sum);
        log.info("The result is {}", result);
    }

    private void buildCardMap(BufferedReader puzzleInput) throws IOException {
        String line = puzzleInput.readLine();
        while (line != null) {
            CardDto card = parseCard(line);
            cardMap.put(card.cardNumber(), card);
            cardCollection.put(card.cardNumber(), 1); // start out with one of each card
            line = puzzleInput.readLine();
        }
    }

    private void winCards(Integer startingCard, Integer numberOfCardsWon) {
        for (int i = startingCard + 1; i < startingCard + 1 + numberOfCardsWon; ++i) {
            log.debug("Won card {} from card {}", i, startingCard);
            incrementCardCount(i);
        }
    }

    private void incrementCardCount(Integer cardNumber) {
        if (!cardCollection.containsKey(cardNumber)) {
            return;
        }
        cardCollection.put(cardNumber, cardCollection.get(cardNumber) + 1);
    }

    private CardDto parseCard(String line) {
        Matcher cardMatcher = CARD_PATTERN.matcher(line);
        if (!cardMatcher.matches()) {
            throw new RuntimeException("Invalid line '%s'".formatted(line));
        }
        Integer cardNumber = Integer.parseInt(cardMatcher.group("cardNumber"));
        Set<Integer> winning = Arrays.stream(cardMatcher.group("winning").split("\\s+"))
                .filter(Predicate.not(String::isBlank))
                .map(Integer::parseInt)
                .collect(Collectors.toSet());
        Set<Integer> selected = Arrays.stream(cardMatcher.group("selected").split("\\s+"))
                .filter(Predicate.not(String::isBlank))
                .map(Integer::parseInt)
                .collect(Collectors.toSet());
        return new CardDto(cardNumber, winning, selected);
    }


    private long getScore(long matches) {
        if (matches == 0) {
            return 0;
        }
        return (long) Math.pow(2, matches - 1);
    }
}
