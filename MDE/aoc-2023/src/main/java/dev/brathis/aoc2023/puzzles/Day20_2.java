package dev.brathis.aoc2023.puzzles;

import dev.brathis.aoc2023.common.PuzzleInputLoader;
import lombok.Data;
import lombok.extern.slf4j.Slf4j;

import java.io.BufferedReader;
import java.io.IOException;
import java.util.*;
import java.util.regex.Pattern;
import java.util.stream.Collectors;

@Slf4j
public class Day20_2 extends Puzzle {
    public Day20_2(PuzzleInputLoader puzzleInputLoader) {
        super(Day20_2.class, puzzleInputLoader);
    }

    private interface Module {
        void handlePulse(long cycle, String inputModule, boolean pulse);

        String getName();

        List<String> getDestinations();
    }

    @Data
    private class FfModule implements Module {
        private final String name;
        private final List<String> destinations;
        private boolean state = false;
        private long lastHighPulseCycle = 0;

        private void emitPulse(boolean pulse) {
            for (var destination : destinations) {
                pulses.add(new Pulse(name, destination, pulse));
            }
        }

        @Override
        public void handlePulse(long cycle, String inputModule, boolean pulse) {
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
        private long lastHighPulse = 0;
        private long lastPeriod = 0;

        private void emitPulse(boolean pulse) {
            for (var destination : destinations) {
                pulses.add(new Pulse(name, destination, pulse));
            }
        }

        @Override
        public void handlePulse(long cycle, String inputModule, boolean pulse) {
            inputModuleState.put(inputModule, pulse);
            if (inputModuleState.values().stream().allMatch(p -> p)) {
                emitPulse(false);
            } else {
                // if the module is on the watchlist, log the period with which it outputs a high pulse
                if (watch.contains(name)) {
                    long period = cycle - lastHighPulse;
                    if (period != lastPeriod && lastPeriod != 0) {
                        // the lcm approach only works if our assumption that the period of the feeder modules is constant,
                        // holds true.
                        throw new RuntimeException("%s: lastPeriod=%d period=%d".formatted(name, lastPeriod, period));
                    } else if (lastPeriod == 0) {
                        log.info("{} hi: {} last={} period={}", name, cycle, lastHighPulse, period);
                        periods.add(period);
                    }
                    lastHighPulse = cycle;
                    lastPeriod = period;
                }

                emitPulse(true);
            }
        }

        public void addInputModule(String inputModule) {
            inputModuleState.put(inputModule, false);
        }
    }

    @Data
    private class BroadcastModule implements Module {
        private final List<String> destinations;

        @Override
        public void handlePulse(long cycle, String inputModule, boolean pulse) {
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
    private Set<String> watch;
    private final Set<Long> periods = new HashSet<>();

    private static final Pattern MODULE_PATTERN = Pattern.compile("^((?<type>[%&])?(?<name>[a-z]+)) -> (?<destinations>([a-z]+(, )?)+)$");

    @Override
    void puzzle(BufferedReader puzzleInput) throws IOException {
        // A low pulse at 'rx' requires a low pulse at the output of the conjunction module which feeds it.
        // This conjunction module has inputs, which all need to emit a high pulse.
        // To calculate this, we have these conjunction modules track their toggle cycles.
        // Assuming that the toggling happens at a fixed period, we can calculate the lcm of the cycles
        // to find the first cycle when they coincide.

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

        // find the module which feeds into 'rx'
        String feedModule = modules.values().stream()
                .filter(module -> module.getDestinations().contains("rx"))
                .map(Module::getName)
                .findFirst()
                .orElseThrow();
        log.info("Module {} feeds into rx", feedModule);
        assert modules.get(feedModule) instanceof ConjunctionModule;

        // find the conjunction modules which feed into the feeder module
        watch = modules.values().stream()
                .filter(module -> module.getDestinations().contains(feedModule))
                .map(Module::getName)
                .collect(Collectors.toSet());
        log.info("Conjunction modules {} feed into {}", watch, feedModule);
        assert watch.stream().map(modules::get).allMatch(module -> module instanceof ConjunctionModule);

        boolean lowPulseAtRx = false;
        long buttonPushes = 0;
        while (!lowPulseAtRx) {
            // button push
            ++buttonPushes;
            pulses.add(new Pulse("button", "broadcaster", false));
            // process pulses in order until there are no more pulses
            while (!pulses.isEmpty()) {
                Pulse pulse = pulses.remove();
                log.debug("PULSE: {}", pulse);

                Module recipient = modules.get(pulse.recipient);
                if (recipient == null) {
                    if (pulse.recipient.equals("rx") && !pulse.value) {
                        log.info("rx received low pulse");
                        lowPulseAtRx = true;
                    }
                } else {
                    recipient.handlePulse(buttonPushes, pulse.sender, pulse.value);
                }
            }
            log.debug("================================================");
            if (periods.size() == watch.size()) {
                log.info("Collected periods from all feeder modules");
                log.info("The answer is {}", lcm(periods.stream().mapToLong(p -> p).toArray()));
                return;
            }
        }
        // will never get here
        log.info("The answer is {}", buttonPushes);
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

    // thanks, StackOverflow: https://stackoverflow.com/a/4202114
    private static long gcd(long a, long b) {
        while (b > 0) {
            long temp = b;
            b = a % b;
            a = temp;
        }
        return a;
    }

    private static long lcm(long a, long b) {
        return a * (b / gcd(a, b));
    }

    private static long lcm(long[] input) {
        long result = input[0];
        for (int i = 1; i < input.length; i++) result = lcm(result, input[i]);
        return result;
    }
}
