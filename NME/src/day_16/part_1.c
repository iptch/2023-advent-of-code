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

enum direction {
    UP,
    DOWN,
    LEFT,
    RIGHT
};

struct beam_head {
    int x;
    int y;
    enum direction d;
    struct beam_head *next;
};

void do_work(char **lines, int line_count, const int *chars_per_line);
struct beam_head *move_beam(struct beam_head *beam, char **grid, int **energized, int a, int b);
void add_beam(struct beam_head *beam, int x, int y, enum direction d);
void print_energized(int **energized, int a, int b);

int main(int argc, char *argv[]) {
    execute_on_input(INPUT_FILE, &do_work);
    return 0;
}

void print_energized(int **energized, int a, int b) {
    for (int i=0; i<a; i++) {
        for (int j=0; j<b; j++) {
            printf("%c", energized[i][j] != -1 ? '#' : '.');
        }
        printf("\n");
    }
    printf("\n");
}

void add_beam(struct beam_head *beam, int x, int y, enum direction d) {
    struct beam_head *new_beam = (struct beam_head *)malloc(sizeof(struct beam_head));
    new_beam->x = x;
    new_beam->y = y;
    new_beam->d = d;
    new_beam->next = beam->next;
    beam->next = new_beam;
}

struct beam_head *move_beam(struct beam_head *beam, char **grid, int **energized, int a, int b) {
    while (beam->x >=0 && beam->x < a && beam->y >= 0 && beam->y < b && energized[beam->x][beam->y] != beam->d) {
        char tile = grid[beam->x][beam->y];
        enum direction dir = beam->d;
        //print_energized(energized, a, b);
        energized[beam->x][beam->y] = dir;

        if (tile == '.') {
            if (dir == UP) beam->x--;
            if (dir == DOWN) beam->x++;
            if (dir == LEFT) beam->y--;
            if (dir == RIGHT) beam->y++;
        }

        if (tile == '/') {
            if (dir == UP) {beam->y++; beam->d=RIGHT;}
            if (dir == DOWN) {beam->y--; beam->d=LEFT;}
            if (dir == LEFT) {beam->x++; beam->d=DOWN;}
            if (dir == RIGHT) {beam->x--; beam->d=UP;}
        }

        if (tile == '\\') {
            if (dir == UP) {beam->y--; beam->d=LEFT;}
            if (dir == DOWN) {beam->y++; beam->d=RIGHT;}
            if (dir == LEFT) {beam->x--; beam->d=UP;}
            if (dir == RIGHT) {beam->x++; beam->d=DOWN;}
        }

        if (tile == '|') {
            if (dir == UP) beam->x--;
            if (dir == DOWN) beam->x++;
            if (dir == LEFT) {beam->x--;beam->d=UP;add_beam(beam, beam->x+1, beam->y, DOWN);}
            if (dir == RIGHT) {beam->x--;beam->d=UP;add_beam(beam, beam->x+1, beam->y, DOWN);}
        }

        if (tile == '-') {
            if (dir == UP) {beam->y--;beam->d=LEFT;add_beam(beam, beam->x, beam->y+1, RIGHT);}
            if (dir == DOWN) {beam->y--;beam->d=LEFT;add_beam(beam, beam->x, beam->y+1, RIGHT);}
            if (dir == LEFT) beam->y--;
            if (dir == RIGHT) beam->y++;
        }
    }
    struct beam_head *next = beam->next;
    free(beam);
    return next;
}


void do_work(char **lines, int line_count, const int *chars_per_line) {
    struct beam_head *current = (struct beam_head *)malloc(sizeof(struct beam_head));
    // beam enters from top left going to the right
    current->x = 0;
    current->y = 0;
    current->d = RIGHT;
    current->next = NULL;

    // energized tiles
    int **energized = (int **)malloc(sizeof(int *) * line_count);
    for (int i=0; i<line_count; i++) {
        energized[i] = (int *)malloc(sizeof(int) * chars_per_line[i]);
        for (int j=0; j<chars_per_line[i]; j++) {
            energized[i][j] = -1;
        }
    }

    // move beams until all are finished
    while(current) {
        current = move_beam(current, lines, energized, line_count, chars_per_line[0]);
    }

    // count up energized tiles
    int res = 0;
    for (int i=0; i<line_count; i++) {
        for (int j=0; j<chars_per_line[i]; j++) {
            if(energized[i][j] != -1) res++;
        }
        free(energized[i]);
    }
    free(energized);

    printf("%d\n", res);
}