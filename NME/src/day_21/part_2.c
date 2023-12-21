#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include "aoc_utils/aoc_utils.h"

#define INPUT_FILE "input.txt"
#define EXPANDING_FACTOR 7
#define ITERATIONS 328
#define STEPS 26501365

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
    printf("\n");
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

    n *= EXPANDING_FACTOR; m *= EXPANDING_FACTOR;
    char **new_lines = (char **)calloc(n, sizeof(char *));
    for (int64_t i=0; i<n; i++) {
        new_lines[i] = (char *)calloc(m, sizeof(char));
        for (int64_t j=0; j<m; j++) {
            new_lines[i][j] = lines[i%line_count][j%chars_per_line[0]];
        }
    }
    lines = new_lines;

    int64_t **grid = init_grid(n, m);
    int64_t **new_grid = init_grid(n, m);
    grid[x + (EXPANDING_FACTOR / 2) * line_count][y + (EXPANDING_FACTOR / 2) * chars_per_line[0]] = 1;

    int64_t a0 = 0;
    int64_t a1 = 0;
    int64_t a2 = 0;
    for (int64_t s=0; s<ITERATIONS; s++) {
        //print_grid(grid, lines, n, m);
        if (s == line_count / 2) a0 = count_steps(grid, n, m);
        if (s == line_count / 2 + line_count) a1 = count_steps(grid, n, m);
        if (s == line_count / 2 + line_count * 2) a2 = count_steps(grid, n, m);

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

    /**
     * We have a generic quadratic equation
     *
     * f(x) = x0 + x1 * x + x2 * x^2
     *
     * because the marked tiles grow quadratically and
     * because there is a loop starting at STEP=65 and repeating every 131 STEPs
     * We therefore know that the following equations hold (x is the loop counter)
     *
     * x=0 | x0             = num_steps(65)
     * x=1 | x0 +  x1 +  x2 = num_steps(65 + 131)
     * x=2 | x0 + 2x1 + 4x2 = num_steps(65 + 2*131)
     *
     * Lets define
     *
     * a0 = num_steps(65)
     * a1 = num_steps(65 + 131)
     * a2 = num_steps(65 + 2*131)
     *
     * Then
     *
     * x0 = a0
     * x1 = -1.5a0 + 2a1 - 0.5a2
     * x2 = 0.5a0 - a1 + 0.5a2
     *
     * We need to walk a total of 26501365 steps, which is 65 + 202300 * 131, thus exactly 202300 loops and 65 steps
     *
     * THIS DOES NOT WORK FOR THE EXAMPLE INPUT
     */

    int64_t loops = (STEPS - line_count / 2) / line_count;

    int64_t x0 = a0;
    int64_t x1 = -3*a0/2 + 2*a1 - a2/2;
    int64_t x2 = a0/2 - a1 + a2/2;

    printf("%lld\n", x0 + loops * x1 + loops * loops * x2 );

    free(new_lines);
    free(new_grid);
    free(grid);
}