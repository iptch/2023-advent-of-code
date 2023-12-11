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
#define DISPLACEMENT 999999

struct star {
    int x;
    int y;
    long long x_new;
    long long y_new;
};

void do_work(char **lines, int line_count, const int *chars_per_line);
struct star *find(struct star *stars, int x, int y, int n);
long long dist(const struct star *s1, const struct star *s2);

int main(int argc, char *argv[]) {
    execute_on_input(INPUT_FILE, &do_work);
    return 0;
}

struct star *find(struct star *stars, int x, int y, int n) {
    for (int i=0; i<n; i++) {
        if (stars[i].x == x && stars[i].y == y) return stars + i;
    }
    return NULL;
}

long long dist(const struct star *s1, const struct star *s2) {
    return llabs(s1->x_new - s2->x_new) + llabs(s1->y_new - s2->y_new);
}



void do_work(char **lines, int line_count, const int *chars_per_line) {
    int n_stars = 0;
    for (int i=0; i<line_count; i++) {
        for (int j=0; j<chars_per_line[i]; j++) {
            if (lines[i][j] == '#') {
                n_stars++;
            }
        }
    }

    struct star *stars = (struct star *)malloc(sizeof(struct star) * n_stars);

    int star_idx = 0;
    int horizontal_count = 0;
    for (int i=0; i<line_count; i++) {
        bool horizontal_empty = true;
        for (int j=0; j<chars_per_line[i]; j++) {
            if (lines[i][j] == '#') {
                stars[star_idx].x = i;
                stars[star_idx].y = j;
                stars[star_idx++].x_new = i + (DISPLACEMENT * horizontal_count);
                horizontal_empty = false;
            }
        }
        if (horizontal_empty) horizontal_count++;
    }

    int vertical_count = 0;
    for (int j=0; j<chars_per_line[0]; j++) {
        bool vertical_empty = true;
        for (int i=0; i<line_count; i++) {
            if (lines[i][j] == '#') {
                find(stars, i, j, n_stars)->y_new = j + (DISPLACEMENT * vertical_count);
                vertical_empty = false;
            }
        }
        if (vertical_empty) vertical_count++;
    }

    long long res = 0;
    for (int i=0; i<n_stars; i++) {
        for (int j=i+1; j<n_stars; j++) {
            res += dist(stars + i, stars + j);
        }
    }

    printf("%lld\n", res);

    free(stars);
}