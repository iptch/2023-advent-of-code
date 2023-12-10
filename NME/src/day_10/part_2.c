#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>
#include <ctype.h>
#include "aoc_utils/aoc_utils.h"

//#define IS_EXAMPLE
#ifdef IS_EXAMPLE
#define INPUT_FILE "example4.txt"
#define CLOCKWISE 1
#else
#define INPUT_FILE "input.txt"
#define CLOCKWISE 1
#endif

struct point {
    int x;
    int y;
    char pipe;
    struct point *n1;
    struct point *n2;
};

struct coord {
    int x;
    int y;
};

void do_work(char **lines, int line_count, const int *chars_per_line);
void flood(int x, int y, int **grid, char **lines, int n, int m);
void print_grid(int **grid, char **lines, int a, int b);

int main(int argc, char *argv[]) {
    execute_on_input(INPUT_FILE, &do_work);
    return 0;
}

void print_grid(int **grid, char **lines, int a, int b) {
    for (int i=0; i<a; i++) {
        for (int j=0; j<b; j++) {
            int state = grid[i][j];
            char c = ' ';
            if (state == 1) c = lines[i][j];
            if (state == 2) c = 'X';
            printf("%c", c);
        }
        printf("\n");
    }
    printf("\n");
}

void flood(int x, int y, int **grid, char **lines, int n, int m) {
    if (grid[x][y] != 2) {
        return;
    }

    struct coord *c = (struct coord *)malloc(sizeof(struct coord));
    c->x = x;
    c->y = y;

    struct queue *q = queue_init(c);
    while (q) {
        struct coord *to_fill = (struct coord *)malloc(sizeof(struct coord));
        q = queue_pop(q, (void **)&to_fill);
        int a = to_fill->x;
        int b = to_fill->y;
        free(to_fill);
        int s[4] = {1, -1, 0, 0};
        int t[4] = {0, 0, 1, -1};
        for (int i=0; i<4; i++) {
            int u = a + s[i];
            int v = b + t[i];
            if (u >= 0 && u < n && v >= 0 && v < m && grid[u][v] == 0) {
                struct coord *neigh = (struct coord *) malloc(sizeof(struct coord));
                neigh->x = u;
                neigh->y = v;
                grid[u][v] = 2;
                if (!q) {
                    q = queue_init(neigh);
                } else {
                    queue_add(q, neigh);
                }
            }

        }
    }
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
        for (int j=0; j<chars_per_line[i]; j++) {
            visited[i][j] = 0;
        }
    }

    int count = 0;
    struct point *current = start;
    while (count == 0 || current->pipe != 'S') {
        visited[current->x][current->y] = 1;
        struct point *next;
        if (CLOCKWISE) {
            if (current->n1 && visited[current->n1->x][current->n1->y] != 1 ||
                (count > 1 && current->n1->pipe == 'S')) {
                next = current->n1;
            } else {
                next = current->n2;
            }
        } else {
            if (current->n2 && visited[current->n2->x][current->n2->y] != 1 ||
                (count > 1 && current->n2->pipe == 'S')) {
                next = current->n2;
            } else {
                next = current->n1;
            }
        }

        if (current->x - 1 == next->x) { //going up, right is in
            if (current->y + 1 < chars_per_line[current->x] && visited[current->x][current->y + 1] != 1) visited[current->x][current->y + 1] = 2;
            if (next->y + 1 < chars_per_line[next->x] && visited[next->x][next->y + 1] != 1) visited[next->x][next->y + 1] = 2;
        }
        if (current->x + 1 == next->x) { //going down, left is in
            if (current->y - 1 >= 0 && visited[current->x][current->y - 1] != 1) visited[current->x][current->y - 1] = 2;
            if (next->y - 1 >= 0 && visited[next->x][next->y - 1] != 1) visited[next->x][next->y - 1] = 2;
        }
        if (current->y - 1 == next->y) { //going left, up is in
            if (current->x - 1 >= 0 && visited[current->x - 1][current->y] != 1) visited[current->x - 1][current->y] = 2;
            if (next->x - 1 >= 0 && visited[next->x - 1][next->y] != 1) visited[next->x - 1][next->y] = 2;
        }
        if (current->y + 1 == next->y) { //going right, down is in
            if (current->x + 1 < line_count && visited[current->x + 1][current->y] != 1) visited[current->x + 1][current->y] = 2;
            if (next->x + 1 < line_count && visited[next->x + 1][next->y] != 1) visited[next->x + 1][next->y] = 2;
        }

        current = next;
        count++;
    }

    //print_grid(visited, lines, line_count, chars_per_line[0]);

    for (int i=0; i<line_count; i++) {
        for (int j=0; j<chars_per_line[i]; j++) {
            flood(i, j, visited, lines, line_count, chars_per_line[0]);
        }
    }

    //print_grid(visited, lines, line_count, chars_per_line[0]);

    int res = 0;
    for (int i=0; i<line_count; i++) {
        for (int j=0; j<chars_per_line[i]; j++) {
            if (visited[i][j] == 2) res++;
        }
    }

    printf("%d\n", res);

    for (int i=0; i<line_count; i++) {
        free(grid[i]);
        free(visited[i]);
    }
    free(visited);
    free(grid);
}