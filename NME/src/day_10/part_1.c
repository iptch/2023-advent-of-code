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

struct point {
    int x;
    int y;
    char pipe;
    struct point *n1;
    struct point *n2;
};

void do_work(char **lines, int line_count, const int *chars_per_line);

int main(int argc, char *argv[]) {
    execute_on_input(INPUT_FILE, &do_work);
    return 0;
}

void do_work(char **lines, int line_count, const int *chars_per_line) {
    struct point **grid = (struct point **)malloc(sizeof(struct point *) * line_count);
    for (int i=0; i<line_count; i++) {
        grid[i] = (struct point *)malloc(sizeof(struct point) * chars_per_line[i]);
    }

    struct point *start = NULL;
    for (int i=0; i<line_count; i++) {
        for (int j=0; j<chars_per_line[i]; j++) {
            grid[i][j].x = i;
            grid[i][j].y = j;
            grid[i][j].pipe = lines[i][j];
            grid[i][j].n1 = NULL;
            grid[i][j].n2 = NULL;
            switch (lines[i][j]) {
                case '.':
                    break;
                case '|':
                    if (i - 1 >= 0) grid[i][j].n1 = &grid[i - 1][j]; // up
                    if (i + 1 < line_count) grid[i][j].n2 = &grid[i + 1][j]; // down
                    break;
                case '-':
                    if (j - 1 >= 0) grid[i][j].n1 = &grid[i][j - 1]; // left
                    if (j + 1 < chars_per_line[i]) grid[i][j].n2 = &grid[i][j + 1]; // right
                    break;
                case 'L':
                    if (i - 1 >= 0) grid[i][j].n1 = &grid[i - 1][j]; // up
                    if (j + 1 < chars_per_line[i]) grid[i][j].n2 = &grid[i][j + 1]; // right
                    break;
                case 'J':
                    if (i - 1 >= 0) grid[i][j].n1 = &grid[i - 1][j]; // up
                    if (j - 1 >= 0) grid[i][j].n2 = &grid[i][j - 1]; // left
                    break;
                case '7':
                    if (i + 1 < line_count) grid[i][j].n1 = &grid[i + 1][j]; // down
                    if (j - 1 >= 0) grid[i][j].n2 = &grid[i][j - 1]; // left
                    break;
                case 'F':
                    if (i + 1 < line_count) grid[i][j].n1 = &grid[i + 1][j]; // down
                    if (j + 1 < chars_per_line[i]) grid[i][j].n2 = &grid[i][j + 1]; // right
                    break;
                case 'S':
                    start = &grid[i][j];
                    if (i - 1 >= 0 && (lines[i - 1][j] == '|' || lines[i - 1][j] == '7' || lines[i - 1][j] == 'F')) {
                        grid[i][j].n1 = &grid[i - 1][j];
                    }
                    if (i + 1 < line_count && (lines[i + 1][j] == '|' || lines[i + 1][j] == 'L' || lines[i + 1][j] == 'J')) {
                        if (grid[i][j].n1) {
                            grid[i][j].n2 = &grid[i + 1][j];
                        } else {
                            grid[i][j].n1 = &grid[i + 1][j];
                        }
                    }
                    if (j - 1 >= 0 && (lines[i][j - 1] == '-' || lines[i][j - 1] == 'L' || lines[i][j - 1] == 'F')) {
                        if (grid[i][j].n1) {
                            grid[i][j].n2 = &grid[i][j-1];
                        } else {
                            grid[i][j].n1 = &grid[i][j-1];
                        }
                    }
                    if (j + 1 < chars_per_line[i] && (lines[i][j + 1] == '-' || lines[i][j + 1] == '7' || lines[i][j + 1] == 'J')) {
                        if (grid[i][j].n1) {
                            grid[i][j].n2 = &grid[i][j + 1];
                        } else {
                            grid[i][j].n1 = &grid[i][j + 1];
                        }
                    }
                    break;
                default:
                    fprintf(stderr, "Unexpected Symbol: %c\n", lines[i][j]);
                    exit(1);

            }
        }
    }

    int **visited = (int **)malloc(sizeof(int *) * line_count);
    for (int i=0; i<line_count; i++) {
        visited[i] = (int *)malloc(sizeof(int) * chars_per_line[i]);
        for (int j=0; j<line_count; j++) {
            visited[i][j] = 0;
        }
    }

    int count = 0;
    struct point *current = start;
    while (count == 0 || current->pipe != 'S') {
        visited[current->x][current->y] = true;
        if (current->n1 && !visited[current->n1->x][current->n1->y] || (count > 1 && current->n1->pipe == 'S')) {
            current = current->n1;
        } else {
            current = current->n2;
        }
        count++;
    }

    printf("%d\n", count / 2);

    for (int i=0; i<line_count; i++) {
        free(grid[i]);
        free(visited[i]);
    }
    free(visited);
    free(grid);
}