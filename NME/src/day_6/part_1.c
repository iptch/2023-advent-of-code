#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>
#include <ctype.h>
#include "aoc_utils/aoc_utils.h"

//#define IS_EXAMPLE
#ifdef IS_EXAMPLE
#define INPUT_FILE "example1.txt"
#define RACES 3
int times[RACES] = {7, 15, 30};
int distances[RACES] = {9, 40, 200};
#else
#define INPUT_FILE "input.txt"
#define RACES 4
int times[] = {63, 78, 94, 68};
int distances[] = {411, 1274, 2047, 1035};
#endif


void do_work(char **lines, int line_count, const int *chars_per_line);

int main(int argc, char *argv[]) {
    execute_on_input(INPUT_FILE, &do_work);
    return 0;
}

void do_work(char **lines, int line_count, const int *chars_per_line) {
    int res = 1;
    for (int i=0; i<RACES; i++) {
        int time = times[i];
        int dist = distances[i];
        int wins = 0;
        for (int j=0; j<time; j++) {
            int d = j * (time - j);
            if (d > dist) {
                wins++;
            }
        }
        res *= wins;
    }
    printf("%d\n", res);
}