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
public class Day06_2 extends Puzzle {
    public Day06_2(PuzzleInputLoader puzzleInputLoader) {
        super(Day06_2.class, puzzleInputLoader);
    }

    private record TimeDistance(long time, long distance) {}
    private static final Pattern LINE_PATTERN = Pattern.compile("^(?<label>Time|Distance):(\\s+)(?<values>.*)");

    private final List<Long> times = new LinkedList<>();
    private final List<Long> distances = new LinkedList<>();
    private final List<TimeDistance> records = new LinkedList<>();
    @Override
    void puzzle(BufferedReader puzzleInput) throws IOException {
        String line = puzzleInput.readLine();
        while (line != null) {
            processLine(line);
            line = puzzleInput.readLine();
        }
        buildRecords();
        log.info("Records: {}", records);

        long product = 1;
        for (var record : records) {
            long numberOfWaysToBeatRecord = 0;
            long raceDuration = record.time;
            for (long chargingDuration = 0; chargingDuration < raceDuration; ++chargingDuration) {
                long remainingTime = raceDuration - chargingDuration;
                long distanceTravelled = remainingTime * chargingDuration;
                if (distanceTravelled > record.distance) {
                    ++numberOfWaysToBeatRecord;
                }
            }
            log.info("There are {} ways to beat {}", numberOfWaysToBeatRecord, record);
            product *= numberOfWaysToBeatRecord;
        }
        log.info("The solution is {}", product);
    }

    void processLine(String line) {
        Matcher lineMatcher = LINE_PATTERN.matcher(line);
        if (!lineMatcher.matches()) {
            throw new RuntimeException("Line '%s' does not match pattern".formatted(line));
        }
        String valueType = lineMatcher.group("label");
        String values = lineMatcher.group("values").replaceAll("\\s+", "");
        List<Long> list = valueType.equals("Time") ? times : distances;
        list.add(Long.parseLong(values));
    }

    void buildRecords() {
        assert times.size() == distances.size();
        for (int i = 0; i < times.size(); ++i) {
            records.add(new TimeDistance(times.get(i), distances.get(i)));
        }
    }

}
