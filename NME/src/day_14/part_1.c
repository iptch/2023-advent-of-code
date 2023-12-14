#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>
#include <ctype.h>
#include "aoc_utils/aoc_utils.h"

//#define IS_EXAMPLE
#ifdef IS_EXAMPLE
#define INPUT_FILE "example1.txt"
#else
#define INPUT_FILE "input.txt"
#endif

void do_work(char **lines, int line_count, const int *chars_per_line);
void move_rock(char **lines, int x, int y);

int main(int argc, char *argv[]) {
    execute_on_input(INPUT_FILE, &do_work);
    return 0;
}

void move_rock(char **lines, int x, int y) {
    while (x-1 >= 0 && lines[x-1][y] == '.') {
        lines[x-1][y] = 'O';
        lines[x--][y] = '.';
    }
}


void do_work(char **lines, int line_count, const int *chars_per_line) {
    for (int i=0; i<line_count; i++) {
        for (int j=0; j<chars_per_line[i]; j++) {
            if (lines[i][j] == 'O') move_rock(lines, i, j);
        }
    }

    int res = 0;
    for (int i=0; i<line_count; i++) {
        for (int j=0; j<chars_per_line[i]; j++) {
            if (lines[i][j] == 'O') res += line_count-i;
        }
    }
    printf("%d\n", res);
}