package dev.brathis.aoc2023.puzzles;

import org.junit.Test;
import org.junit.jupiter.api.Disabled;

import java.util.List;
import java.util.Set;

import static dev.brathis.aoc2023.puzzles.Day05_2.getInputsCorrespondingToLocalMinima;
import static org.assertj.core.api.Assertions.assertThat;

public class Day05_2Test {

    @Test
    public void test_reverseMap() {
        // given
        var mapping = getTestMapping();

        // when
        final Set<Long> outputs = Set.of(
                0L, 3L, 12L, 20L, 24L
        );
        var inputs = mapping.reverseMap(outputs);

        // then
        assertThat(inputs).isEqualTo(Set.of(
            0L, 3L, 7L, 10L, 20L, 14L, 24L
        ));
    }

    @Test
    public void test_getInputsCorrespondingToLocalMinima() {
        // given
        var mapping = getTestMapping();

        // when
        var inputs = mapping.getInputsCorrespondingToLocalMinima();

        // then
        assertThat(inputs).isEqualTo(Set.of(0L, 5L, 10L, 20L, 22L, 24L));
    }

    /**
     * in   out     minimum
     * ====================
     * 0    10      x
     * 1    11
     * 2    12
     * 3    3       x
     * 4    4
     * 5    10      x
     * 6    11
     * 7    12
     * 8    13
     * 9    14
     * 10   20      x
     * 11   21
     * 12   22
     * 13   23
     * 14   24
     * 15   25
     * 16   0       x
     * 17   27      x
     * 18   28
     * 19   29
     * 20   20      x
     * 21   21
     * 22   5       x
     * 23   6
     * 24   24      x
     * 25   25
     * 26   0       x
     * 27   27      x
     * 28   28
     * 29   29
     * 30   30
     * 31   31
     * 32   32
     * 33   33
     * 34   34
     * 35   35
     * 36   36
     * 37   37
     * 38   38
     * 39   39
     */
    @Test
    @Disabled("for calculating composite mappings")
    public void test_compositeMapping() {
        // given
        var mapping1 = getTestMapping();
        var mapping2 = getTestMappingWithRangeStartingAtZero();

        // when
        for (long i = 0L; i < 40L; ++i) {
            long out = mapping2.map(mapping1.map(i));
            System.out.printf("%d   %d%n", i, out);
        }
    }

    @Test
    public void test_getInputsCorrespondingToLocalMinimaForComposites() {
        // given
        var mapping1 = getTestMapping();
        var mapping2 = getTestMappingWithRangeStartingAtZero();

        // when
        Set<Long> compositeMinima = getInputsCorrespondingToLocalMinima(List.of(mapping2, mapping1));

        // then
        assertThat(compositeMinima).isEqualTo(Set.of(
                0L, 3L, 5L, 10L, 16L, 17L, 20L, 22L, 24L, 26L, 27L
        ));
    }

    private static Day05_2.Mapping getTestMapping() {
        /*
            in      out     range       minimum?
            ====================================
            0       0                   x
            1       1
            2       2
            3       3
            4       4
            5       10      A           x
            6       11      A
            7       12      A
            8       13      A
            9       14      A
            10      20      B           x
            11      21      B
            12      22      B
            13      23      B
            14      24      B
            15      25      B
            16      26      B
            17      27      B
            18      28      B
            19      29      B
            20      20                  x
            21      21
            22      5       C           x
            23      6       C
            24      24                  x
            25      25
            ...
         */
        return new Day05_2.Mapping("", "", List.of(
                new Day05_2.Range(10L, 5L, 5L),     // A
                new Day05_2.Range(20L, 10L, 10L),   // B
                new Day05_2.Range(5L, 22L, 2L)      // C
        ));
    }

    private static Day05_2.Mapping getTestMappingWithRangeStartingAtZero() {
        /*
            in      out     range       minimum?
            ====================================
            0       10      A           x
            1       11      A
            2       12      A
            3       3                   x
            4       4
            5       5
            6       6
            7       7
            8       8
            9       9
            10      10
            ...
            25      25
            26      0       B           x
            27      27                  x
            28      28
            ...
         */
        return new Day05_2.Mapping("", "", List.of(
                new Day05_2.Range(10L, 0L, 3L),     // A
                new Day05_2.Range(0L, 26L, 1L)      // B
        ));
    }
}
