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
    struct point *next;
};

enum direction {R,D,L,U};

void do_work(char **lines, int line_count, const int *chars_per_line);
void print_grid(int **grid, int h, int w);
void add(struct point *q, int x, int y);

int main(int argc, char *argv[]) {
    execute_on_input(INPUT_FILE, &do_work);
    return 0;
}

void print_grid(int **grid, int h, int w) {
    for (int i=0; i<h; i++) {
        for (int j=0; j<w; j++) printf("%c", grid[i][j] ? '#' : '.');
        printf("\n");
    }
    printf("\n");
}

void add(struct point *q, int x, int y) {
    struct point *new = (struct point *)malloc(sizeof(struct point));
    new->x = x;
    new->y = y;
    new->next = q->next;
    q->next = new;
}

void do_work(char **lines, int line_count, const int *chars_per_line) {
    int x = 0; int y = 0;
    int maxX = x; int minX = x;
    int maxY = y; int minY = y;
    int *distances = (int *)malloc(sizeof(int) * line_count);
    int border_size = 0;
    for (int i=0; i<line_count; i++) {
        int dist = atoi(strtok(lines[i] + 2, " "));
        distances[i] = dist;
        border_size += dist;
        switch (lines[i][0]) {
            case 'U': x-=dist; minX=min(minX, x); break;
            case 'D': x+=dist; maxX=max(maxX, x); break;
            case 'L': y-=dist; minY=min(minY, y); break;
            case 'R': y+=dist; maxY=max(maxY, y); break;
        }
    }

    int h = maxX - minX + 1; int w = maxY - minY + 1;

    int **grid = (int **)malloc(sizeof(int *) * h);
    for (int i=0; i<h; i++) grid[i] = (int *)calloc(w, sizeof(int));

    x = -minX; y = -minY;
    for (int i=0; i<line_count; i++) {
        switch (lines[i][0]) {
            case 'U': for (int j=0; j<distances[i]; j++) grid[x--][y] = 1; break;
            case 'D': for (int j=0; j<distances[i]; j++) grid[x++][y] = 1; break;
            case 'L': for (int j=0; j<distances[i]; j++) grid[x][y--] = 1; break;
            case 'R': for (int j=0; j<distances[i]; j++) grid[x][y++] = 1; break;
        }
    }

    //print_grid(grid, h, w);

    struct point *q = (struct point *)malloc(sizeof(struct point));
    q->x = h / 2;
    q->y = w / 2;
    q->next = NULL;
    while (q) {
        grid[q->x][q->y] = 1;
        if (q->x+1<h && !grid[q->x+1][q->y]) add(q, q->x+1, q->y);
        if (q->x-1>=0 && !grid[q->x-1][q->y]) add(q, q->x-1, q->y);
        if (q->y+1<w && !grid[q->x][q->y+1]) add(q, q->x, q->y+1);
        if (q->y-1>=0 && !grid[q->x][q->y-1]) add(q, q->x, q->y-1);
        q = q->next;
    }

    //print_grid(grid, h, w);

    int res = 0;
    for (int i=0; i<h; i++) {
        for (int j=0; j<w; j++) res += grid[i][j];
    }

    printf("%d\n", res);

    for (int i=0; i<h; i++) free(grid[i]);
    free(grid);
    free(distances);

}