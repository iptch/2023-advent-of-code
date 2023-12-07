package dev.brathis.aoc2023.puzzles;

import dev.brathis.aoc2023.common.PuzzleInputLoader;
import lombok.Getter;
import lombok.extern.slf4j.Slf4j;

import java.io.BufferedReader;
import java.io.IOException;
import java.util.*;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

@Slf4j
public class Day07_1 extends Puzzle {
    public Day07_1(PuzzleInputLoader puzzleInputLoader) {
        super(Day07_1.class, puzzleInputLoader);
    }

    private static final Pattern LINE_PATTERN = Pattern.compile("^(?<hand>\\w+) (?<bid>\\d+)");

    enum HandType {
        FIVE_OF_A_KIND(7),
        FOUR_OF_A_KIND(6),
        FULL_HOUSE(5),
        THREE_OF_A_KIND(4),
        TWO_PAIR(3),
        ONE_PAIR(2),
        NOTHING(1);

        @Getter
        private final int rank;

        HandType(int rank) {
            this.rank = rank;
        }
    }

    private class Hand implements Comparable<Hand> {
        @Getter
        private final String hand;
        @Getter
        private final Long bid;
        private final Map<Character, Integer> occurrenceMap = new HashMap<>();
        @Getter
        private HandType type;

        Hand(String hand, Long bid) {
            this.hand = hand;
            this.bid = bid;
            buildOccurrenceMap();
            determineType();
        }

        private void buildOccurrenceMap() {
            for (char c : hand.toCharArray()) {
                if (!occurrenceMap.containsKey(c)) {
                    occurrenceMap.put(c, 1);
                } else {
                    occurrenceMap.put(c, occurrenceMap.get(c) + 1);
                }
            }
        }

        private void determineType() {
            if (isFiveOfAKind()) {
                this.type = HandType.FIVE_OF_A_KIND;
            } else if (isFourOfAKind()) {
                this.type = HandType.FOUR_OF_A_KIND;
            } else if (isFullHouse()) {
                this.type = HandType.FULL_HOUSE;
            } else if (isThreeOfAKind()) {
                this.type = HandType.THREE_OF_A_KIND;
            } else if (isTwoPair()) {
                this.type = HandType.TWO_PAIR;
            } else if (isOnePair()) {
                this.type = HandType.ONE_PAIR;
            } else if (isNothing()) {
                this.type = HandType.NOTHING;
            } else {
                throw new RuntimeException("Could not determine type of hand '%d'".formatted(hand));
            }
        }

        private boolean isFiveOfAKind() {
            return occurrenceMap.keySet().size() == 1;
        }

        private boolean isFourOfAKind() {
            return occurrenceMap.keySet().size() == 2
                    && occurrenceMap.containsValue(1);
        }

        private boolean isFullHouse() {
            return occurrenceMap.keySet().size() == 2
                    && occurrenceMap.containsValue(2);
        }

        private boolean isThreeOfAKind() {
            return occurrenceMap.keySet().size() == 3
                    && occurrenceMap.containsValue(3);
        }

        private boolean isTwoPair() {
            return occurrenceMap.keySet().size() == 3
                    && occurrenceMap.containsValue(2);
        }

        private boolean isOnePair() {
            return occurrenceMap.keySet().size() == 4
                    && occurrenceMap.containsValue(2);
        }

        private boolean isNothing() {
            return occurrenceMap.keySet().size() == 5;
        }

        @Override
        public int compareTo(Hand other) {
            if (this.type.rank > other.type.rank) {
                return 1;
            }
            if (this.type.rank < other.type.rank) {
                return -1;
            }
            for (int i = 0; i < 5; ++i) {
                if (cardValue(this.hand.charAt(i)) > cardValue(other.hand.charAt(i))) {
                    return 1;
                }
                if (cardValue(this.hand.charAt(i)) < cardValue(other.hand.charAt(i))) {
                    return -1;
                }
            }
            return 0;
        }

        private static int cardValue(char c) {
            return switch (c) {
                case '2' -> 1;
                case '3' -> 2;
                case '4' -> 3;
                case '5' -> 4;
                case '6' -> 5;
                case '7' -> 6;
                case '8' -> 7;
                case '9' -> 8;
                case 'T' -> 9;
                case 'J' -> 10;
                case 'Q' -> 11;
                case 'K' -> 12;
                case 'A' -> 13;
                default -> throw new RuntimeException("Invalid card letter '%s'".formatted(c));
            };
        }
    }

    private final List<Hand> hands = new LinkedList<>();

    @Override
    void puzzle(BufferedReader puzzleInput) throws IOException {
        String line = puzzleInput.readLine();
        while (line != null) {
            processLine(line);
            line = puzzleInput.readLine();
        }

        for (var hand : hands) {
            log.info("Hand '{}' is of type '{}'", hand.getHand(), hand.getType());
        }

        long winnings = 0L;
        List<Hand> handsSorted = new LinkedList<>(hands);
        Collections.sort(handsSorted);
        for (int i = 0; i < handsSorted.size(); ++i) {
            int rank = i + 1;
            log.info("Rank {}: {} bid {}", rank, handsSorted.get(i).getHand(), handsSorted.get(i).getBid());
            winnings += handsSorted.get(i).getBid() * rank;
        }
        log.info("The answer is {}", winnings);
    }

    private void processLine(String line) {
        Matcher lineMatcher = LINE_PATTERN.matcher(line);
        if (!lineMatcher.matches()) {
            throw new RuntimeException("Line '%s' does not match pattern".formatted(line));
        }
        hands.add(new Hand(lineMatcher.group("hand"), Long.parseLong(lineMatcher.group("bid"))));
    }
}
