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
int compute_energy(int **energized, int a, int b);
int one_pass(int x, int y, enum  direction d, char **grid, int a, int b);

int main(int argc, char *argv[]) {
    execute_on_input(INPUT_FILE, &do_work);
    return 0;
}

int one_pass(int x, int y, enum  direction d, char **grid, int a, int b) {
    struct beam_head *current = (struct beam_head *)malloc(sizeof(struct beam_head));
    // beam enters from top left going to the right
    current->x = x;
    current->y = y;
    current->d = d;
    current->next = NULL;

    // energized tiles
    int **energized = (int **)malloc(sizeof(int *) * a);
    for (int i=0; i<a; i++) {
        energized[i] = (int *)malloc(sizeof(int) * b);
        for (int j=0; j<b; j++) {
            energized[i][j] = -1;
        }
    }

    // move beams until all are finished
    while(current) {
        current = move_beam(current, grid, energized, a, b);
    }

    int res = compute_energy(energized, a, b);

    for (int i=0; i<a; i++) free(energized[i]);
    free(energized);

    return res;
}

int compute_energy(int **energized, int a, int b) {
    int res = 0;
    for (int i=0; i<a; i++) {
        for (int j=0; j<b; j++) {
            if(energized[i][j] != -1) res++;
        }
    }
    return res;
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
    int res = 0;
    for (int i=0; i<line_count; i++) {
        res = max(res, one_pass(i, 0, RIGHT, lines, line_count, chars_per_line[0]));
        res = max(res, one_pass(i, chars_per_line[0]-1, LEFT, lines, line_count, chars_per_line[0]));
    }
    for (int i=0; i<chars_per_line[0]; i++) {
        res = max(res, one_pass(0, i, DOWN, lines, line_count, chars_per_line[0]));
        res = max(res, one_pass(line_count-1, i, UP, lines, line_count, chars_per_line[0]));
    }
    printf("%d\n", res);
}