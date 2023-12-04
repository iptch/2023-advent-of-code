#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>
#include "aoc_utils/aoc_utils.h"

//#define IS_EXAMPLE

#ifdef IS_EXAMPLE
#define INPUT_FILE "example1.txt"
#define WIN_NUMS 5
#define MY_NUMS 8
#define FIRST_NUM_IDX 8
#else
#define INPUT_FILE "input.txt"
#define WIN_NUMS 10
#define MY_NUMS 25
#define FIRST_NUM_IDX 10
#endif

void do_work(char **lines, int line_count, const int *chars_per_line);
int get_digit(char c) {
    if (c == ' ') {
        return 0;
    } else {
        return c - '0';
    }
}

int main(int argc, char *argv[]) {
    execute_on_input(INPUT_FILE, &do_work);
    return 0;
}

void do_work(char **lines, int line_count, const int *chars_per_line) {
    int *copies = (int *) malloc(sizeof(int) * line_count);
    for (int i=0; i<line_count; i++) {
        copies[i] = 1;
    }
    for (int i=0; i<line_count; i++) {
        int num_winners = 0;
        int winners[WIN_NUMS];
        for (int j=0; j<WIN_NUMS; j++) {
            winners[j] = 10 * (get_digit(lines[i][FIRST_NUM_IDX + 3*j])) + get_digit(lines[i][FIRST_NUM_IDX + 3*j + 1]);
        }
        for (int j=0; j<MY_NUMS; j++) {
            int draw = 10 * (get_digit(lines[i][FIRST_NUM_IDX + WIN_NUMS*3 + 2 + 3*j])) + get_digit(lines[i][FIRST_NUM_IDX + WIN_NUMS*3 + 2 + 3*j + 1]);
            for (int k=0; k<WIN_NUMS; k++) {
                if (winners[k] == draw) {
                    num_winners++;
                }
            }
        }
        for (int j=0; j<num_winners; j++) {
            copies[i+j+1] += copies[i];
        }
    }
    int score = 0;
    for (int i=0; i<line_count; i++) {
        score += copies[i];
    }
    printf("%d\n", score);
    free(copies);
}