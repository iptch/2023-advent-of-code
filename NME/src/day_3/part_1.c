#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>
#include <ctype.h>
#include "aoc_utils/aoc_utils.h"

#define INPUT_FILE "input.txt"

void do_work(char **lines, int line_count, const int *chars_per_line);
int scan(bool **visited, char **lines, int m, int n, int i, int j);

int main(int argc, char *argv[]) {
    execute_on_input(INPUT_FILE, &do_work);
    return 0;
}

void do_work(char **lines, int line_count, const int *chars_per_line) {
    bool **visited = (bool **)calloc(line_count, sizeof(bool *));
    for (int i=0; i<line_count; i++) {
        visited[i] = (bool *) calloc(chars_per_line[i], sizeof(bool));
    }
    int res = 0;
    for (int i=0; i<line_count; i++) {
        for (int j=0; j<chars_per_line[i]; j++) {
            char c = lines[i][j];
            if (!isdigit(c) && c != '.') {
                res += scan((bool **) visited, lines, line_count, chars_per_line[j], i, j);
            }
        }
    }
    printf("%d\n", res);

    for (int i=0; i<line_count; i++) {
        free(visited[i]);
    }
    free(visited);
}

int scan(bool **visited, char **lines, int m, int n, int i, int j) {
    int res = 0;
    for (int a=-1; a<=1; a++) {
        for (int b=-1; b<=1; b++) {
            int x = i+a;
            int y = j+b;
            if (x >= 0 && x < n && y >= 0 && y < m) {
                if (!visited[x][y] && isdigit(lines[x][y])) {
                    int start = y;
                    int end = y;
                    while (start-1 >= 0 && isdigit(lines[x][start-1])) {
                        start -= 1;
                    }
                    while (end+1 < n && isdigit(lines[x][end+1])) {
                        end += 1;
                    }
                    int radix = 1;
                    for (int u=end; u>=start; u--) {
                        res += radix * (lines[x][u] - '0');
                        radix *= 10;
                        visited[x][u] = true;
                    }
                }
            }
        }
    }
    return res;
}
