package dev.brathis.aoc2023.puzzles;

import dev.brathis.aoc2023.common.PuzzleInputLoader;
import lombok.Data;
import lombok.extern.slf4j.Slf4j;

import java.io.BufferedReader;
import java.io.IOException;
import java.util.*;
import java.util.regex.Pattern;

@Slf4j
public class Day20_1 extends Puzzle {
    public Day20_1(PuzzleInputLoader puzzleInputLoader) {
        super(Day20_1.class, puzzleInputLoader);
    }

    private interface Module {
        void handlePulse(String inputModule, boolean pulse);
        String getName();
        List<String> getDestinations();
    }

    @Data
    private class FfModule implements Module {
        private final String name;
        private final List<String> destinations;
        private boolean state = false;

        private void emitPulse(boolean pulse) {
            for (var destination : destinations) {
                pulses.add(new Pulse(name, destination, pulse));
            }
        }

        @Override
        public void handlePulse(String inputModule, boolean pulse) {
            if (!pulse) {
                state = !state;
                emitPulse(state);
            }
        }
    }

    @Data
    private class ConjunctionModule implements Module {
        private final String name;
        private final List<String> destinations;
        private final Map<String, Boolean> inputModuleState = new HashMap<>();

        private void emitPulse(boolean pulse) {
            for (var destination : destinations) {
                pulses.add(new Pulse(name, destination, pulse));
            }
        }

        @Override
        public void handlePulse(String inputModule, boolean pulse) {
            inputModuleState.put(inputModule, pulse);
            emitPulse(!inputModuleState.values().stream().allMatch(p -> p));
        }

        public void addInputModule(String inputModule) {
            inputModuleState.put(inputModule, false);
        }
    }

    @Data
    private class BroadcastModule implements Module {
        private final List<String> destinations;
        @Override
        public void handlePulse(String inputModule, boolean pulse) {
            for (var destination : destinations) {
                pulses.add(new Pulse(getName(), destination, pulse));
            }
        }

        @Override
        public String getName() {
            return "broadcast";
        }
    }

    @Data
    private static class Pulse {
        private final String sender;
        private final String recipient;
        private final boolean value;

        @Override
        public String toString() {
            return "%s -%s-> %s".formatted(sender, value ? "high" : "low", recipient);
        }
    }

    private final Map<String, Module> modules = new HashMap<>();
    private final Queue<Pulse> pulses = new LinkedList<>();

    private static final Pattern MODULE_PATTERN = Pattern.compile("^((?<type>[%&])?(?<name>[a-z]+)) -> (?<destinations>([a-z]+(, )?)+)$");

    @Override
    void puzzle(BufferedReader puzzleInput) throws IOException {
        String line = puzzleInput.readLine();
        while (line != null) {
            processLine(line);
            line = puzzleInput.readLine();
        }
        log.info("Modules: {}", modules);

        // initialize the conjunction modules
        for (var module : modules.values()) {
            for (var destinationName : module.getDestinations()) {
                var targetModule = modules.get(destinationName);
                if (targetModule instanceof ConjunctionModule) {
                    ((ConjunctionModule) targetModule).addInputModule(module.getName());
                }
            }
        }

        int lowPulseCount = 0;
        int highPulseCount = 0;
        for (int i = 0; i < 1000; ++i) {
            // button push
            pulses.add(new Pulse("button", "broadcaster", false));
            // process pulses in order until there are no more pulses
            while (!pulses.isEmpty()) {
                Pulse pulse = pulses.remove();
                log.info("PULSE: {}", pulse);
                Module recipient = modules.get(pulse.recipient);
                if (recipient == null) {
                    log.warn("Recipient module '%s' does not exist".formatted(pulse.recipient));
                } else {
                    recipient.handlePulse(pulse.sender, pulse.value);
                }
                if (pulse.value) {
                    ++highPulseCount;
                } else {
                    ++lowPulseCount;
                }
            }
            log.info("================================================");
        }
        log.info("Sent {} low pulses, {} high pulses", lowPulseCount, highPulseCount);
        log.info("The answer is {}", lowPulseCount * highPulseCount);
    }

    private void processLine(String line) {
        var matcher = MODULE_PATTERN.matcher(line);
        if (!matcher.matches()) {
            throw new IllegalArgumentException("'%s' does not match module pattern".formatted(line));
        }
        modules.put(matcher.group("name"), createModule(
                matcher.group("name"),
                matcher.group("type"),
                Arrays.asList(matcher.group("destinations").split(", "))
        ));
    }

    private Module createModule(String name, String type, List<String> destinations) {
        if (type == null) {
            return new BroadcastModule(destinations);
        }
        if (type.equals("%")) {
            return new FfModule(name, destinations);
        }
        if (type.equals("&")) {
            return new ConjunctionModule(name, destinations);
        }
        throw new IllegalArgumentException("Invalid module type '%s'".formatted(type));
    }
}
