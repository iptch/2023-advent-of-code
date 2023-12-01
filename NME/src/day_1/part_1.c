#include <stdio.h>
#include <ctype.h>
#include "aoc_utils/aoc_utils.h"

#define INPUT_FILE "input.txt"

void do_work(char **lines, int line_count, const int *chars_per_line);

int main(int argc, char *argv[]) {
    execute_on_input(INPUT_FILE, &do_work);
    return 0;
}

void do_work(char **lines, int line_count, const int *chars_per_line) {
    int total = 0;
    for (int i=0; i<line_count; i++) {
        int first = -1;
        int last;
        for (int j=0; j<chars_per_line[i]; j++) {
            char c = lines[i][j];
            if (isdigit(c)) {
                int digit = c - '0';
                if (first == -1) {
                    first = digit;
                }
                last = digit;
            }
        }
        total += (first * 10) + last;
    }
    printf("%d", total);
}