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
long long solve(char **lines, int start, int length, int width);
void invert(char **lines, int a, int b);
int reflect(char **lines, int start, int length, int width, long long solution_to_skip);

int main(int argc, char *argv[]) {
    execute_on_input(INPUT_FILE, &do_work);
    return 0;
}

void invert(char **lines, int a, int b) {
    if (lines[a][b] == '.') {
        lines [a][b] = '#';
    } else {
        lines[a][b] = '.';
    }
}

int reflect(char **lines, int start, int length, int width, long long solution_to_skip) {
    // vertical reflection
    for (int i=0; i<width-1; i++) {
        int size_on_each_side = min(i + 1, width - i - 1);
        bool is_reflection = true;
        for (int j=0; j<size_on_each_side; j++) {
            for (int k=start; k<start + length; k++) {
                if (lines[k][i-j] != lines[k][i+j+1]) is_reflection = false;
            }
        }
        if (is_reflection && (solution_to_skip != (i+1))) return i+1;
    }

    // horizontal reflection
    for (int i=0; i<length-1; i++) {
        int size_on_each_side = min(i + 1, length - i - 1);
        bool is_reflection = true;
        for (int j=0; j<size_on_each_side; j++) {
            for (int k=0; k<width; k++) {
                if (lines[start+i-j][k] != lines[start+i+j+1][k]) is_reflection = false;
            }
        }
        if (is_reflection && (solution_to_skip != (i+1)*100)) return (i+1)*100;
    }
    return -1;
}

long long solve(char **lines, int start, int length, int width) {
    long long original = reflect(lines, start, length, width, -1);
    for (int a=start; a<start+length; a++) {
        for (int b = 0; b < width; b++) {
            invert(lines, a, b);
            long long r = reflect(lines, start, length, width, original);
            if (r != -1 && r != original) return r;
            invert(lines, a, b);
        }
    }
    return -1;
}


void do_work(char **lines, int line_count, const int *chars_per_line) {
    int start_idx = 0;
    long long res = 0;
    for (int i=0; i<line_count; i++) {
        if (chars_per_line[i] == 0) {
            res += solve(lines, start_idx, i - start_idx, chars_per_line[start_idx]);
            start_idx = i+1;
        }
    }
    res += solve(lines, start_idx, line_count - start_idx, chars_per_line[line_count-1]);
    printf("%lld\n", res);
}