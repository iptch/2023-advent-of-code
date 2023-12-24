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
#define TEST_AREA_MIN 7.0
#define TEST_AREA_MAX 27.0
#else
#define INPUT_FILE "input.txt"
#define TEST_AREA_MIN 200000000000000.0
#define TEST_AREA_MAX 400000000000000.0
#endif

typedef struct stone {
    double x;
    double y;
    double z;
    double dx;
    double dy;
    double dz;
} Stone;

void do_work(char **lines, int line_count, const int *chars_per_line);
Stone *parse_stone(char *s);
bool intersect(Stone *a, Stone *b);

int main(int argc, char *argv[]) {
    execute_on_input(INPUT_FILE, &do_work);
    return 0;
}

Stone *parse_stone(char *s) {
    Stone *new_stone = (Stone *)calloc(1, sizeof(Stone));
    new_stone->x = (double)atoll(strtok(s, ","));
    new_stone->y = (double)atoll(strtok(NULL, ",") + 1);
    new_stone->z = (double)atoll(strtok(NULL, " "));
    new_stone->dx = (double)atoll(strtok(NULL, ",") + 2);
    new_stone->dy = (double)atoll(strtok(NULL, ",") + 1);
    new_stone->dz = (double)atoll(strtok(NULL, ",") + 1);
    return new_stone;
}

bool intersect(Stone *p1, Stone *p2) {
    if (p1->dy * p2->dx == p1->dx * p2->dy) return false; // parallel lines
    double m1 = p1->dy / p1->dx;
    double m2 = p2->dy / p2->dx;
    double x = (m1 * p1->x - m2 * p2->x - p1->y + p2->y) / (m1 - m2);
    double y = m1 * (x - p1->x) + p1->y;
    if (p1->dx > 0 && p1->x > x || p1->dx < 0 && p1->x < x) return false;
    if (p1->dy > 0 && p1->y > y || p1->dy < 0 && p1->y < y) return false;
    if (p2->dx > 0 && p2->x > x || p2->dx < 0 && p2->x < x) return false;
    if (p2->dy > 0 && p2->y > y || p2->dy < 0 && p2->y < y) return false;
    return x >= TEST_AREA_MIN && x <= TEST_AREA_MAX && y >= TEST_AREA_MIN && y <= TEST_AREA_MAX;
}

void do_work(char **lines, int line_count, const int *chars_per_line) {
    Stone **stones = (Stone **)calloc(line_count, sizeof(Stone *));
    for (int i=0; i<line_count; i++) stones[i] = parse_stone(lines[i]);

    int res = 0;
    for (int i=0; i<line_count; i++) {
        for (int j=i+1; j<line_count; j++) res += intersect(stones[i], stones[j]);
    }

    printf("%d\n", res);

    for (int i=0; i<line_count; i++) free(stones[i]);
    free(stones);
}