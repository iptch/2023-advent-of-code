package dev.brathis.aoc2023.puzzles;

import dev.brathis.aoc2023.common.PuzzleInputLoader;
import lombok.extern.slf4j.Slf4j;

import java.io.BufferedReader;
import java.io.IOException;
import java.util.LinkedList;
import java.util.List;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

@Slf4j
public class Day05_1 extends Puzzle {
    public Day05_1(PuzzleInputLoader puzzleInputLoader) {
        super(Day05_1.class, puzzleInputLoader);
    }

    private enum ParserState {
        SEEDS,
        BETWEEN_MAPS,
        MAP_HEADER,
        MAP_CONTENT,
    }

    private record RangeEntry(Long destinationRangeStart, Long sourceRangeStart, Long length) {
        public boolean containsValue(long value) {
            return value >= sourceRangeStart && value < sourceRangeStart + length;
        }

        public Long map(long inputValue) {
            assert containsValue(inputValue);
            return inputValue - sourceRangeStart + destinationRangeStart;
        }
    };
    private record Range(String from, String to, List<RangeEntry> rangeEntries) {
        public long map(long inputValue) {
            for (var rangeEntry : rangeEntries) {
                if (rangeEntry.containsValue(inputValue)) {
                    return rangeEntry.map(inputValue);
                }
            }
            return inputValue;
        }
    };
    private ParserState parserState = ParserState.SEEDS;
    private List<Long> seeds = new LinkedList<>();
    private String currentMapFrom = null;
    private String currentMapTo = null;
    private List<RangeEntry> currentRangeEntries = new LinkedList<>();
    private List<Range> ranges = new LinkedList<>();

    @Override
    void puzzle(BufferedReader puzzleInput) throws IOException {
        String line = puzzleInput.readLine();
        while (line != null) {
            processLine(line);
            line = puzzleInput.readLine();
        }
        completeMap();
        log.info("Loaded {} ranges", ranges.size());

        long lowest = Long.MAX_VALUE;
        for (long seed : seeds) {
            lowest = Math.min(lowest, mapSeedValue(seed));
        }
        log.info("The answer is {}", lowest);
    }

    private void processLine(String line) {
        switch (parserState) {
            case SEEDS -> processLineSeeds(line);
            case BETWEEN_MAPS -> processLineBetweenMaps(line);
            case MAP_HEADER -> processLineMapHeader(line);
            case MAP_CONTENT -> processLineMapContent(line);
        }
    }

    private void processLineSeeds(String line) {
        Matcher seedsMatcher = Pattern.compile("((?<seed>\\d+)\\s?)").matcher(line);
        while (seedsMatcher.find()) {
            long seed = Long.parseLong(seedsMatcher.group("seed"));
            seeds.add(seed);
            log.debug("Found seed {}", seed);
        }
        parserState = ParserState.BETWEEN_MAPS;
    }

    private void processLineBetweenMaps(String line) {
        assert line.isEmpty();
        parserState = ParserState.MAP_HEADER;
    }

    private void processLineMapHeader(String line) {
        Matcher mapHeaderMatcher = Pattern.compile("^(?<from>\\w+)-to-(?<to>\\w+) map:").matcher(line);
        if (!mapHeaderMatcher.matches()) {
            throw new RuntimeException("Line '%s' does not match pattern".formatted(line));
        }
        log.debug("Mapping from {} to {}", mapHeaderMatcher.group("from"), mapHeaderMatcher.group("to"));
        currentMapFrom = mapHeaderMatcher.group("from");
        currentMapTo = mapHeaderMatcher.group("to");
        parserState = ParserState.MAP_CONTENT;
    }

    private void processLineMapContent(String line) {
        Pattern mapContentPattern = Pattern.compile("(\\d+)\\s+(\\d+)\\s+(\\d+)");
        if (line.isEmpty()) {
            completeMap();
            return;
        }
        Matcher mapContentMatcher = mapContentPattern.matcher(line);
        if (!mapContentMatcher.matches()) {
            throw new RuntimeException("Line '%s' does not match pattern".formatted(line));
        }
        RangeEntry rangeEntry = new RangeEntry(
                Long.parseLong(mapContentMatcher.group(1)),
                Long.parseLong(mapContentMatcher.group(2)),
                Long.parseLong(mapContentMatcher.group(3)));
        log.debug("Found map entry: {}", rangeEntry);
        currentRangeEntries.add(rangeEntry);
    }

    private void completeMap() {
        var range = new Range(currentMapFrom, currentMapTo, currentRangeEntries);
        log.debug("Found range {}", range);
        ranges.add(range);
        currentMapFrom = null;
        currentMapTo = null;
        currentRangeEntries = new LinkedList<>();
        parserState = ParserState.MAP_HEADER;
    }

    private long mapSeedValue(long seed) {
        long out = seed;
        for (var range : ranges) {
            out = range.map(out);
        }
        log.debug("{} maps to {}", seed, out);
        return out;
    }
}
