#include <stdio.h>
#include <string.h>
#include <ctype.h>
#include "aoc_utils/aoc_utils.h"

#define INPUT_FILE "input.txt"
#define DIGIT_COUNT 9


void do_work(char **lines, int line_count, const int *chars_per_line);

int main(int argc, char *argv[]) {
    execute_on_input(INPUT_FILE, &do_work);
    return 0;
}

void do_work(char **lines, int line_count, const int *chars_per_line) {
    char* numbers[DIGIT_COUNT] = {"one", "two", "three", "four", "five", "six", "seven", "eight", "nine"};

    for (int i=0; i<line_count; i++) {
        for (int j=0; j<DIGIT_COUNT; j++) {
            char *ptr = strstr(lines[i], numbers[j]);
            while(ptr) {
                ptr[1] = j + 1 + '0';
                ptr = strstr(lines[i], numbers[j]);
            }
        }
    }

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
