package dev.brathis.aoc2023.puzzles;

import dev.brathis.aoc2023.common.PuzzleInputLoader;
import lombok.extern.slf4j.Slf4j;

import java.io.BufferedReader;
import java.io.IOException;
import java.util.*;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

@Slf4j
public class Day12_2 extends Puzzle {
    public Day12_2(PuzzleInputLoader puzzleInputLoader) {
        super(Day12_2.class, puzzleInputLoader);
    }

    private record ConditionRecord(String springs, List<Integer> errorCorrection) {
    }

    private record MemoKey(int charIdx, int groupIdx, int groupOffset) {
    }

    private static final Pattern RECORD_PATTERN = Pattern.compile("^(?<springs>[.#?]+) (?<errorCorrection>(\\d+,?)+)$");

    private final List<ConditionRecord> conditionRecords = new LinkedList<>();
    private final Map<MemoKey, Long> memoMap = new HashMap<>();

    @Override
    void puzzle(BufferedReader puzzleInput) throws IOException {
        parseConditionRecords(puzzleInput);
        log.debug("Read condition records: {}", conditionRecords);
        long totalArrangements = 0;
        for (var conditionRecord : conditionRecords) {
            memoMap.clear();
            long arrangements = countArrangements(conditionRecord.springs, conditionRecord.errorCorrection, 0, 0, 0);
            log.debug("{} {} - {} arrangements", conditionRecord.springs, conditionRecord.errorCorrection, arrangements);
            totalArrangements += arrangements;
        }
        log.info("The answer is {}", totalArrangements);
    }

    private void parseConditionRecords(BufferedReader puzzleInput) throws IOException {
        String line = puzzleInput.readLine();
        while (line != null) {
            Matcher matcher = RECORD_PATTERN.matcher(line);
            if (!matcher.matches()) {
                throw new RuntimeException("Line '%s' did not match".formatted(line));
            }
            List<Integer> errorCorrection = Arrays.stream(repeatString(matcher.group("errorCorrection"), 5, ",").split(","))
                    .mapToInt(Integer::parseInt)
                    .boxed()
                    .toList();
            conditionRecords.add(new ConditionRecord(repeatString(matcher.group("springs"), 5, "?"), errorCorrection));
            line = puzzleInput.readLine();
        }
    }

    private String repeatString(String input, int copies, String separator) {
        var sb = new StringBuilder();
        for (int i = 0; i < copies; ++i) {
            sb.append(input);
            if (i < copies - 1) {
                sb.append(separator);
            }
        }
        return sb.toString();
    }

    private long countArrangements(String pattern, List<Integer> groups, final int charIdx, final int groupIdx, final int groupOffset) {
        final MemoKey key = new MemoKey(charIdx, groupIdx, groupOffset);
        if (memoMap.containsKey(key)) {
            return memoMap.get(key);
        }

        final int maxGroupIdx = groups.size() - 1;
        final int maxGroupOffset = groupIdx <= maxGroupIdx ? groups.get(groupIdx) - 1 : -1;
        final boolean inGroup = groupOffset > 0;
        final boolean currentGroupExhausted = inGroup && groupOffset > maxGroupOffset;
        final boolean groupsExhausted = groupIdx > maxGroupIdx;
        log.debug("charIdx={} groupIdx={} groupOffset={} inGroup={} currentGroupExhausted={} groupsExhausted={} maxGroupOffset={}", charIdx, groupIdx, groupOffset, inGroup, currentGroupExhausted, groupsExhausted, maxGroupOffset);

        if (charIdx == pattern.length()) {
            // we've finished generating an arrangement
            // for it to be valid, there must be no left-over groups
            // i.e. either the groupIdx points beyond the end of the groups
            // or the groupOffset points beyond the end of the last group
            if (groupsExhausted || groupIdx == maxGroupIdx && currentGroupExhausted) {
                return putMemo(key, 1);
            } else {
                return putMemo(key, 0);
            }
        }

        final char currentChar = pattern.charAt(charIdx);

        if (currentChar == '.') {
            if (inGroup && !currentGroupExhausted) {
                return putMemo(key, 0);
            }
            return putMemo(key, countArrangements(pattern, groups, charIdx + 1, inGroup ? groupIdx + 1 : groupIdx, 0));
        } else if (currentChar == '#') {
            if (inGroup && currentGroupExhausted) {
                return putMemo(key, 0);
            }
            if (!inGroup && groupsExhausted) {
                return putMemo(key, 0);
            }
            return putMemo(key, countArrangements(pattern, groups, charIdx + 1, groupIdx, groupOffset + 1));
        } else {
            long arrangementsNextWorking;
            long arrangementsNextBroken;

            // .
            if (inGroup && !currentGroupExhausted) {
                arrangementsNextWorking = 0;
            } else {
                arrangementsNextWorking = countArrangements(pattern, groups, charIdx + 1, inGroup ? groupIdx + 1 : groupIdx, 0);
            }

            // #
            if (inGroup && currentGroupExhausted) {
                arrangementsNextBroken = 0;
            } else if (!inGroup && groupsExhausted) {
                arrangementsNextBroken = 0;
            } else {
                arrangementsNextBroken = countArrangements(pattern, groups, charIdx + 1, groupIdx, groupOffset + 1);
            }

            return putMemo(key, arrangementsNextWorking + arrangementsNextBroken);
        }
    }

    private long putMemo(MemoKey key, long value) {
        memoMap.put(key, value);
        return value;
    }
}
