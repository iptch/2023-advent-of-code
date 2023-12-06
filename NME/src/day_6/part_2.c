#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>
#include <ctype.h>
#include "aoc_utils/aoc_utils.h"

//#define IS_EXAMPLE
#ifdef IS_EXAMPLE
#define INPUT_FILE "example1.txt"
long long time = 71530;
long long dist = 940200;
#else
#define INPUT_FILE "input.txt"
long long time = 63789468;
long long dist = 411127420471035;
#endif


void do_work(char **lines, int line_count, const int *chars_per_line);

int main(int argc, char *argv[]) {
    execute_on_input(INPUT_FILE, &do_work);
    return 0;
}

void do_work(char **lines, int line_count, const int *chars_per_line) {
    int wins = 0;
    for (int j=0; j<time; j++) {
        long long d = j * (time - j);
        if (d > dist) {
            wins++;
        }
    }
    printf("%d\n", wins);
}