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
public class Day06_1 extends Puzzle {
    public Day06_1(PuzzleInputLoader puzzleInputLoader) {
        super(Day06_1.class, puzzleInputLoader);
    }

    private record TimeDistance(int time, int distance) {}
    private static final Pattern LINE_PATTERN = Pattern.compile("^(?<label>Time|Distance):(\\s+)(?<values>.*)");
    private static final Pattern VALUES_PATTERN = Pattern.compile("((?<value>\\d+)\\s*)");

    private final List<Integer> times = new LinkedList<>();
    private final List<Integer> distances = new LinkedList<>();
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

        int product = 1;
        for (var record : records) {
            int numberOfWaysToBeatRecord = 0;
            int raceDuration = record.time;
            for (int chargingDuration = 0; chargingDuration < raceDuration; ++chargingDuration) {
                int remainingTime = raceDuration - chargingDuration;
                int distanceTravelled = remainingTime * chargingDuration;
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
        String values = lineMatcher.group("values");
        Matcher valuesMatcher = VALUES_PATTERN.matcher(values);
        while (valuesMatcher.find()) {
            List<Integer> list = valueType.equals("Time") ? times : distances;
            list.add(Integer.parseInt(valuesMatcher.group("value")));
        }
    }

    void buildRecords() {
        assert times.size() == distances.size();
        for (int i = 0; i < times.size(); ++i) {
            records.add(new TimeDistance(times.get(i), distances.get(i)));
        }
    }

}
