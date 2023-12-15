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
int hash(const char *label, int n);

int main(int argc, char *argv[]) {
    execute_on_input(INPUT_FILE, &do_work);
    return 0;
}

int hash(const char *label, int n) {
    int res = 0;
    for (int i=0; i<n; i++) {
        res = 17*(res + label[i]);
        res = res % 256;
    }
    return res;
}

void do_work(char **lines, int line_count, const int *chars_per_line) {
    int res = 0;
    char *ins = strtok(lines[0], ",");
    while (ins) {
        res += hash(ins, strlen(ins));
        ins = strtok(NULL, ",");
    }
    printf("%d\n", res);
}