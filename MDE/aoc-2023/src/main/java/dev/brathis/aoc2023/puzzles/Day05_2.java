package dev.brathis.aoc2023.puzzles;

import dev.brathis.aoc2023.common.PuzzleInputLoader;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;

import java.io.BufferedReader;
import java.io.IOException;
import java.util.*;
import java.util.regex.Matcher;
import java.util.regex.Pattern;
import java.util.stream.Collectors;
import java.util.stream.Stream;

@Slf4j
public class Day05_2 extends Puzzle {
    public Day05_2(PuzzleInputLoader puzzleInputLoader) {
        super(Day05_2.class, puzzleInputLoader);
    }

    private enum ParserState {
        SEEDS,
        BETWEEN_MAPPINGS,
        MAPPING_HEADER,
        MAPPING_CONTENT,
    }

    record Range(Long destinationRangeStart, Long sourceRangeStart, Long length) {
        public boolean mapsInputValue(long inputValue) {
            return inputValue >= sourceRangeStart && inputValue < sourceRangeStart + length;
        }

        public boolean mapsOutputValue(long outputValue) {
            return outputValue >= destinationRangeStart && outputValue < destinationRangeStart + length;
        }

        public long map(long inputValue) {
            assert mapsInputValue(inputValue);
            return inputValue - sourceRangeStart + destinationRangeStart;
        }

        public long reverseMap(long outputValue) {
            assert mapsOutputValue(outputValue);
            return outputValue - destinationRangeStart + sourceRangeStart;
        }
    }

    @RequiredArgsConstructor
    static class Mapping {
        private final String from;
        private final String to;
        private final List<Range> ranges;

        public long map(long inputValue) {
            for (var rangeEntry : ranges) {
                if (rangeEntry.mapsInputValue(inputValue)) {
                    return rangeEntry.map(inputValue);
                }
            }
            return inputValue;
        }

        public Set<Long> reverseMap(Collection<Long> outputValues) {
            Set<Long> inputValues = new HashSet<>();
            for (var outputValue : outputValues) {
                boolean isOutputValueMappedByUnity = true;
                for (var range : ranges) {
                    if (range.mapsOutputValue(outputValue)) {
                        inputValues.add(range.reverseMap(outputValue));
                    }
                    if (isOutputValueMappedByUnity && range.mapsInputValue(outputValue)) {
                        isOutputValueMappedByUnity = false;
                    }
                }
                if (isOutputValueMappedByUnity) {
                    inputValues.add(outputValue);
                }
            }
            return inputValues;
        }

        public Set<Long> getInputsCorrespondingToLocalMinima() {
            Set<Long> inputs = new HashSet<>();
            inputs.add(0L);
            for (var range : ranges) {
                inputs.add(range.sourceRangeStart);
                inputs.add(range.sourceRangeStart + range.length);
            }
            return inputs;
        }
    }

    private ParserState parserState = ParserState.SEEDS;
    private final List<Long> seedStarts = new LinkedList<>();
    private final List<Long> seedLengths = new LinkedList<>();
    private String currentMapFrom = null;
    private String currentMapTo = null;
    private List<Range> currentRanges = new LinkedList<>();
    private final List<Mapping> mappings = new LinkedList<>();

    @Override
    void puzzle(BufferedReader puzzleInput) throws IOException {
        String line = puzzleInput.readLine();
        while (line != null) {
            processLine(line);
            line = puzzleInput.readLine();
        }
        completeMapping();
        log.info("Loaded {} mappings", mappings.size());

        List<Mapping> mappingsReversed = new LinkedList<>(mappings);
        Collections.reverse(mappingsReversed);

        List<Long> inputsCorrespondingToLocalMinima = getInputsCorrespondingToLocalMinima(mappingsReversed).stream()
                .sorted()
                .toList();
        log.info("inputsCorrespondingToLocalMinima: {}", inputsCorrespondingToLocalMinima);

        long minOutput = Long.MAX_VALUE;
        for (int i = 0; i < seedStarts.size(); ++i) {
            var seedStart = seedStarts.get(i);
            var seedLength = seedLengths.get(i);
            // For each seed range, we only check the seed start plus any "local minimum" inputs which are contained
            // in the seed range.
            Set<Long> valuesToEvaluate = getValuesToEvaluate(seedStart, seedLength, inputsCorrespondingToLocalMinima);
            log.info("For range start={} length={}, evaluate values {}", seedStart, seedLength, valuesToEvaluate);
            for (var seed : valuesToEvaluate) {
                long output = mapSeedValue(seed);
                log.debug("{} -> {}", seed, output);
                minOutput = Math.min(minOutput, output);
            }
        }
        log.info("The answer is {}", minOutput);
    }

    private Set<Long> getValuesToEvaluate(long seedStart, long seedLength, List<Long> inputsCorrespondingToLocalMinima) {
        Set<Long> valuesToEvaluate = new HashSet<>();
        valuesToEvaluate.add(seedStart);
        final var seedRangeMax = seedStart + seedLength - 1;
        for (var candidate : inputsCorrespondingToLocalMinima) {
            if (candidate >= seedStart && candidate <= seedRangeMax) {
                valuesToEvaluate.add(candidate);
            }
        }
        return valuesToEvaluate;
    }

    private void processLine(String line) {
        switch (parserState) {
            case SEEDS -> processLineSeeds(line);
            case BETWEEN_MAPPINGS -> processLineBetweenMaps(line);
            case MAPPING_HEADER -> processLineMappingHeader(line);
            case MAPPING_CONTENT -> processLineMappingContent(line);
        }
    }

    private void processLineSeeds(String line) {
        Matcher seedsMatcher = Pattern.compile("((?<seedStart>\\d+)\\s+(?<seedLength>\\d+)\\s*)").matcher(line);
        while (seedsMatcher.find()) {
            long seedStart = Long.parseLong(seedsMatcher.group("seedStart"));
            long seedLength = Long.parseLong(seedsMatcher.group("seedLength"));
            seedStarts.add(seedStart);
            seedLengths.add(seedLength);
        }
        parserState = ParserState.BETWEEN_MAPPINGS;
    }

    private void processLineBetweenMaps(String line) {
        assert line.isEmpty();
        parserState = ParserState.MAPPING_HEADER;
    }

    private void processLineMappingHeader(String line) {
        Matcher mapHeaderMatcher = Pattern.compile("^(?<from>\\w+)-to-(?<to>\\w+) map:").matcher(line);
        if (!mapHeaderMatcher.matches()) {
            throw new RuntimeException("Line '%s' does not match pattern".formatted(line));
        }
        log.debug("Mapping from {} to {}", mapHeaderMatcher.group("from"), mapHeaderMatcher.group("to"));
        currentMapFrom = mapHeaderMatcher.group("from");
        currentMapTo = mapHeaderMatcher.group("to");
        parserState = ParserState.MAPPING_CONTENT;
    }

    private void processLineMappingContent(String line) {
        Pattern mapContentPattern = Pattern.compile("(\\d+)\\s+(\\d+)\\s+(\\d+)");
        if (line.isEmpty()) {
            completeMapping();
            return;
        }
        Matcher mapContentMatcher = mapContentPattern.matcher(line);
        if (!mapContentMatcher.matches()) {
            throw new RuntimeException("Line '%s' does not match pattern".formatted(line));
        }
        Range range = new Range(
                Long.parseLong(mapContentMatcher.group(1)),
                Long.parseLong(mapContentMatcher.group(2)),
                Long.parseLong(mapContentMatcher.group(3)));
        log.debug("Found range: {}", range);
        currentRanges.add(range);
    }

    private void completeMapping() {
        var mapping = new Mapping(currentMapFrom, currentMapTo, currentRanges);
        log.debug("Found mapping {}", mapping);
        mappings.add(mapping);
        currentMapFrom = null;
        currentMapTo = null;
        currentRanges = new LinkedList<>();
        parserState = ParserState.MAPPING_HEADER;
    }

    private long mapSeedValue(long seed) {
        long out = seed;
        for (var mapping : mappings) {
            out = mapping.map(out);
        }
        log.debug("{} maps to {}", seed, out);
        return out;
    }

    public static Set<Long> getInputsCorrespondingToLocalMinima(List<Mapping> mappingsInReverseOrder) {
        // buckle up, here it goes...
        Set<Long> minima = null;
        for (var mapping : mappingsInReverseOrder) {
            if (minima == null) {
                minima = mapping.getInputsCorrespondingToLocalMinima();
                continue;
            }
            minima = Stream.concat(
                    mapping.getInputsCorrespondingToLocalMinima().stream(), // input-mapped output minima of current layer
                    mapping.reverseMap(minima).stream()                     // back-propagated output minima of subsequent layers
            ).collect(Collectors.toSet());
        }
        return minima;
    }
}
