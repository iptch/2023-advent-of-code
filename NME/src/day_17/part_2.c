#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>
#include <ctype.h>
#include "aoc_utils/aoc_utils.h"

//#define IS_EXAMPLE
#ifdef IS_EXAMPLE
#define INPUT_FILE "example1.txt"
#define GRID_SIZE_X 13
#define GRID_SIZE_Y 13
#else
#define INPUT_FILE "input.txt"
#define GRID_SIZE_X 141
#define GRID_SIZE_Y 141
#endif
#define STRAIGHT_LINE 10
#define DIRECTION 4

enum direction {
    UP,
    DOWN,
    LEFT,
    RIGHT
};

struct min_queue {
    int val;
    int x;
    int y;
    int straight_line;
    enum direction d;
    struct min_queue *next;
};

int shortest_path[GRID_SIZE_X][GRID_SIZE_Y][STRAIGHT_LINE][DIRECTION];

void do_work(char **lines, int line_count, const int *chars_per_line);
void init_shortest_path();
struct min_queue *best(int val, struct min_queue *q, int **grid, int n, int m);
struct min_queue *push(struct min_queue *q, int val, int x, int y, int straight_line, enum direction d);
int compute_best();


int main(int argc, char *argv[]) {
    execute_on_input(INPUT_FILE, &do_work);
    return 0;
}

int compute_best() {
    int res = INT_MAX;
    for (int k=0; k<STRAIGHT_LINE; k++) {
        for (int l=0; l<DIRECTION; l++) {
            res = min(res, shortest_path[GRID_SIZE_X-1][GRID_SIZE_Y-1][k][l]);
        }
    }
    return res;
}

struct min_queue *pop(struct min_queue *q) {
    struct min_queue *res = q->next;
    free(q);
    return res;
}

/* linear scan, min-heap would be more efficient */
struct min_queue *push(struct min_queue *q, int val, int x, int y, int straight_line, enum direction d) {
    struct min_queue *new_elem = (struct min_queue *)malloc(sizeof(struct min_queue));
    new_elem->val = val;
    new_elem->x = x;
    new_elem->y = y;
    new_elem->straight_line = straight_line;
    new_elem->d = d;

    if (!q) {
        new_elem->next = NULL;
        return new_elem;
    }

    if (q->val > val) {
        new_elem->next = q;
        return new_elem;
    }

    struct min_queue *prev = q;
    struct min_queue *curr = q->next;
    while (curr) {
        if (curr->val > val) {
            prev->next = new_elem;
            new_elem->next = curr;
            return q;
        }

        prev = curr;
        curr = curr->next;
    }

    prev->next = new_elem;
    new_elem->next = NULL;
    return q;
}

void init_shortest_path() {
    for (int i=0; i<GRID_SIZE_X; i++) {
        for (int j=0; j<GRID_SIZE_Y; j++) {
            for (int k=0; k<STRAIGHT_LINE; k++) {
                for (int l=0; l<DIRECTION; l++) {
                    shortest_path[i][j][k][l] = INT_MAX;
                }
            }
        }
    }
}

struct min_queue *best(int val, struct min_queue *q, int **grid, int n, int m) {
    int grid_val = grid[q->x][q->y];
    struct min_queue *res = q->next;
    q->next = NULL;

    if (shortest_path[q->x][q->y][q->straight_line][q->d] <= val + grid_val) {
        free(q);
        return res;
    }

    shortest_path[q->x][q->y][q->straight_line][q->d] = val + grid_val;

    if (q->x == n-1 && q->y == m-1) {
        free(q);
        return res;
    }

    // go up
    if (q->d != DOWN && !(q->d == UP && q->straight_line == 10)) {
        if (q->d != UP && q->x-4>=0) {
            res = push(res, val + grid_val + grid[q->x-1][q->y] + grid[q->x-2][q->y] + grid[q->x-3][q->y], q->x-4, q->y, 4, UP);
        } else if (q->d == UP && q->x-1>=0) {
            res = push(res, val + grid_val, q->x - 1, q->y, q->straight_line + 1, UP);
        }
    }

    // go down
    if (q->d != UP && !(q->d == DOWN && q->straight_line == 10)) {
        if (q->d != DOWN && q->x+4<n) {
            res = push(res, val + grid_val + grid[q->x+1][q->y] + grid[q->x+2][q->y] + grid[q->x+3][q->y], q->x+4, q->y, 4, DOWN);
        } else if (q->d == DOWN && q->x+1<n) {
            res = push(res, val + grid_val, q->x + 1, q->y, q->straight_line + 1, DOWN);
        }
    }

    // go left
    if (q->d != RIGHT && !(q->d == LEFT && q->straight_line == 10)) {
        if (q->d != LEFT && q->y-4>=0) {
            res = push(res, val + grid_val + grid[q->x][q->y-1] + grid[q->x][q->y-2] + grid[q->x][q->y-3], q->x, q->y-4, 4, LEFT);
        } else if (q->d == LEFT && q->y-1>=0) {
            res = push(res, val + grid_val, q->x, q->y-1, q->straight_line + 1, LEFT);
        }
    }

    // go right
    if (q->d != LEFT && !(q->d == RIGHT && q->straight_line == 10)) {
        if (q->d != RIGHT && q->y+4<m) {
            res = push(res, val + grid_val + grid[q->x][q->y+1] + grid[q->x][q->y+2] + grid[q->x][q->y+3], q->x, q->y+4, 4, RIGHT);
        } else if (q->d == RIGHT && q->y+1<m) {
            res = push(res, val + grid_val, q->x, q->y+1, q->straight_line + 1, RIGHT);
        }
    }

    free(q);
    return res;
}


void do_work(char **lines, int line_count, const int *chars_per_line) {
    init_shortest_path();
    int **grid = (int **)malloc(sizeof(int *) * line_count);
    for (int i=0; i<line_count; i++) {
        grid[i] = (int *)malloc(sizeof(int) * chars_per_line[i]);
        for (int j=0; j<chars_per_line[i]; j++) {
            grid[i][j] = lines[i][j] - '0';
        }
    }

    struct min_queue *q = (struct min_queue *)malloc(sizeof(struct min_queue));
    q->val = -grid[0][0];
    q->x = 0;
    q->y = 0;
    q->straight_line = 0;
    q->d = UP;
    q->next = (struct min_queue *)malloc(sizeof(struct min_queue));
    q->next->val = -grid[0][0];
    q->next->x = 0;
    q->next->y = 0;
    q->next->straight_line = 0;
    q->next->d = LEFT;
    q->next->next = NULL;

    while (q) {
        q = best(q->val, q, grid, line_count, chars_per_line[0]);
    }

    printf("%d\n", compute_best());

    for(int i=0; i<line_count; i++) free(grid[i]);
    free(grid);
}