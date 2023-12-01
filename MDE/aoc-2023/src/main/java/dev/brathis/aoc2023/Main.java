package dev.brathis.aoc2023;


import dev.brathis.aoc2023.common.ClasspathPuzzleInputLoader;
import dev.brathis.aoc2023.common.PuzzleInputLoader;
import dev.brathis.aoc2023.common.PuzzleLoader;
import dev.brathis.aoc2023.puzzles.Puzzle;
import lombok.Builder;
import lombok.Getter;

public class Main {
    public static void main(String[] args) throws Exception {

        CommandLineArgs commandLineArgs = parseCommandLineArgs(args);
        PuzzleLoader puzzleLoader = getPuzzleLoader();

        Puzzle puzzle = puzzleLoader.loadPuzzle(commandLineArgs.getDay(), commandLineArgs.getPart());
        if (puzzle == null) {
            System.err.printf("Could not load puzzle for day %d part %d%n", commandLineArgs.getDay(), commandLineArgs.getPart());
            return;
        }

        try {
            if (commandLineArgs.getTest()) {
                runTest(puzzle);
            } else {
                run(puzzle);
            }
        } catch (Exception e) {
            System.err.println("Puzzle solution threw exception");
            throw e;
        }
    }

    private static PuzzleLoader getPuzzleLoader() {
        PuzzleInputLoader puzzleInputLoader = getPuzzleInputLoader();
        return new PuzzleLoader(puzzleInputLoader);
    }

    private static PuzzleInputLoader getPuzzleInputLoader() {
        return new ClasspathPuzzleInputLoader("puzzleInputs");
    }

    private static void run(Puzzle puzzle) throws Exception {
        System.out.printf("Running puzzle for day %d%n", puzzle.getDay());
        puzzle.run();
    }

    private static void runTest(Puzzle puzzle) throws Exception {
        System.out.printf("Running TEST puzzle for day %d%n", puzzle.getDay());
        puzzle.runTest();
    }

    @Getter
    @Builder
    private static class CommandLineArgs {
        private final Integer day;
        private final Integer part;
        private final Boolean test;
    }

    private static CommandLineArgs parseCommandLineArgs(String[] args) {
        if (args.length < 1) {
            final String error = "Specify puzzle day";
            System.err.println(error);
            throw new RuntimeException(error);
        }

        if (args.length < 2) {
            final String error = "Specify puzzle part";
            System.err.println(error);
            throw new RuntimeException(error);
        }

        return CommandLineArgs.builder()
                .day(Integer.parseInt(args[0]))
                .part(Integer.parseInt(args[1]))
                .test(args.length >= 3 && args[2].equals("test"))
                .build();
    }
}
