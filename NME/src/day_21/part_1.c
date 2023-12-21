#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>
#include <ctype.h>
#include <stdint.h>
#include "aoc_utils/aoc_utils.h"

//#define IS_EXAMPLE
#ifdef IS_EXAMPLE
#define INPUT_FILE "example1.txt"
#define STEPS 6
#else
#define INPUT_FILE "input.txt"
#define STEPS 64
#endif

void do_work(char **lines, int line_count, const int *chars_per_line);
int64_t **init_grid(int64_t n, int64_t m);
void print_grid(int64_t **grid, char **lines, int64_t n, int64_t m);
int64_t count_steps(int64_t **grid, int64_t n, int64_t m);
void swap_grids(int64_t ***old, int64_t ***new);
void clear_grid(int64_t **grid, int64_t n, int64_t m);


int main(int argc, char *argv[]) {
    execute_on_input(INPUT_FILE, &do_work);
    return 0;
}

void swap_grids(int64_t ***old, int64_t ***new) {
    int64_t **temp_grid = *old;
    *old = *new;
    *new = temp_grid;
}

void clear_grid(int64_t **grid, int64_t n, int64_t m) {
    for (int64_t i=0; i<n; i++) {
        for (int64_t j=0; j<m; j++) grid[i][j] = 0;
    }
}


void print_grid(int64_t **grid, char **lines, int64_t n, int64_t m) {
    for (int64_t i=0; i<n; i++) {
        for (int64_t j=0; j<m; j++) {
            if (grid[i][j]) printf("O");
            else if (lines[i][j] == '#') printf("#");
            else printf(".");
        }
        printf("\n");
    }
    printf("\n");
    fflush(stdout);
}

int64_t count_steps(int64_t **grid, int64_t n, int64_t m) {
    int64_t res = 0;
    for (int64_t i=0; i<n; i++) for (int64_t j=0; j<m; j++) res += grid[i][j];
    return res;
}

int64_t **init_grid(int64_t n, int64_t m) {
    int64_t **grid = (int64_t **)calloc(n, sizeof(int64_t *));
    for (int64_t i=0; i<n; i++) grid[i] = (int64_t *)calloc(m, sizeof(int64_t));
    return grid;
}

void do_work(char **lines, int line_count, const int *chars_per_line) {
    int64_t n = line_count;
    int64_t m = chars_per_line[0];
    int64_t x; int64_t y;
    for (int64_t i=0; i<n; i++) {
        for (int64_t j=0; j<m; j++) {
            if (lines[i][j] == 'S') {
                x = i;
                y = j;
                lines[i][j] = '.';
            }
        }
    }

    int64_t **grid = init_grid(n, m);
    int64_t **new_grid = init_grid(n, m);
    grid[x][y] = 1;
    for (int64_t s=0; s<STEPS; s++) {
        for (int64_t i=0; i<n; i++) {
            for (int64_t j=0; j<m; j++) {
                if (i-1 >= 0 && lines[i-1][j] == '.') new_grid[i-1][j] |= grid[i][j];
                if (i+1  < n && lines[i+1][j] == '.') new_grid[i+1][j] |= grid[i][j];
                if (j-1 >= 0 && lines[i][j-1] == '.') new_grid[i][j-1] |= grid[i][j];
                if (i+1  < m && lines[i][j+1] == '.') new_grid[i][j+1] |= grid[i][j];
            }
        }

        swap_grids(&grid, &new_grid);
        clear_grid(new_grid, n, m);
    }

    printf("%lld\n", count_steps(grid, n, m));

    free(new_grid);
    free(grid);
}