#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>
#include <ctype.h>
#include "aoc_utils/aoc_utils.h"

//#define IS_EXAMPLE
#ifdef IS_EXAMPLE
#define INPUT_FILE "example1.txt"
#define CYCLE_START 2
#define CYCLE_LENGTH 7
#else
#define INPUT_FILE "input.txt"
#define CYCLE_START 111
#define CYCLE_LENGTH 36
#endif

#define CYCLES 1000000000

void do_work(char **lines, int line_count, const int *chars_per_line);
void cycle(char **lines, int line_count, const int *chars_per_line);
int load(char **lines, int line_count, const int *chars_per_line);

int main(int argc, char *argv[]) {
    execute_on_input(INPUT_FILE, &do_work);
    return 0;
}

int load(char **lines, int line_count, const int *chars_per_line) {
    int res = 0;
    for (int i=0; i<line_count; i++) {
        for (int j=0; j<chars_per_line[i]; j++) {
            if (lines[i][j] == 'O') res += line_count-i;
        }
    }
    return res;
}

void cycle(char **lines, int line_count, const int *chars_per_line) {
    // north
    for (int i = 0; i < line_count; i++) {
        for (int j = 0; j < chars_per_line[0]; j++) {
            if (lines[i][j] == 'O') {
                int x = i;
                int y = j;
                while (x - 1 >= 0 && lines[x - 1][y] == '.') {
                    lines[x-1][y] = 'O';
                    lines[x--][y] = '.';
                }
            }
        }
    }

    // west
    for (int j = 0; j < chars_per_line[0]; j++) {
        for (int i = 0; i < line_count; i++) {
            if (lines[i][j] == 'O') {
                int x = i;
                int y = j;
                while (y - 1 >= 0 && lines[x][y - 1] == '.') {
                    lines[x][y-1] = 'O';
                    lines[x][y--] = '.';
                }
            }
        }
    }

    // south
    for (int i = line_count - 1; i >= 0; i--) {
        for (int j = 0; j < chars_per_line[0]; j++) {
            if (lines[i][j] == 'O') {
                int x = i;
                int y = j;
                while (x + 1 < line_count && lines[x + 1][y] == '.') {
                    lines[x+1][y] = 'O';
                    lines[x++][y] = '.';
                }
            }
        }
    }

    // east
    for (int j = chars_per_line[0] - 1; j >= 0; j--) {
        for (int i = 0; i < line_count; i++) {
            if (lines[i][j] == 'O') {
                int x = i;
                int y = j;
                while (y + 1 < chars_per_line[0] && lines[x][y + 1] == '.') {
                    lines[x][y+1] = 'O';
                    lines[x][y++] = '.';
                }
            }
        }
    }
}


void do_work(char **lines, int line_count, const int *chars_per_line) {
    int result_cycle_index = CYCLES - (CYCLE_LENGTH * ((CYCLES - CYCLE_START) / CYCLE_LENGTH) + CYCLE_START);
    for (int i=0; i<CYCLE_START + result_cycle_index; i++) {
        cycle(lines, line_count, chars_per_line);
    }

    printf("%d\n", load(lines, line_count, chars_per_line));
}