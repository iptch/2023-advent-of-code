#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>
#include "aoc_utils/aoc_utils.h"

#define INPUT_FILE "input.txt"

void do_work(char **lines, int line_count, const int *chars_per_line);

int main(int argc, char *argv[]) {
    execute_on_input(INPUT_FILE, &do_work);
    return 0;
}

void do_work(char **lines, int line_count, const int *chars_per_line) {

}