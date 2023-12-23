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
#else
#define INPUT_FILE "input.txt"
#endif

struct point {
    int64_t x;
    int64_t y;
    int64_t distance;
    bool **visited;
    struct point *next;
};

void do_work(char **lines, int line_count, const int *chars_per_line);
void print_path(char **lines, bool **visited, uint64_t n, uint64_t m);

int main(int argc, char *argv[]) {
    execute_on_input(INPUT_FILE, &do_work);
    return 0;
}

void print_path(char **lines, bool **visited, uint64_t n, uint64_t m) {
    for (uint64_t i=0; i<n; i++) {
        for (uint64_t j=0; j<m; j++) {
            char to_print = lines[i][j];
            if (visited[i][j]) to_print = 'O';
            printf("%c", to_print);
        }
        printf("\n");
    }
    printf("\n");
}

void do_work(char **lines, int line_count, const int *chars_per_line) {
    uint64_t n = line_count; uint64_t m = chars_per_line[0];
    bool **visited = (bool **)calloc(n, sizeof(bool *));
    for (uint64_t i=0; i<n; i++) visited[i] = (bool *)calloc(m, sizeof(bool));

    struct point *p = (struct point *)calloc(1, sizeof(struct point));
    p->x = 0LL;
    p->y = 1LL;
    p->distance = 0LL;
    p->visited = visited;
    p->next = NULL;
    p->visited[p->x][p->y] = true;

    int64_t neighbor_offsets[4][2] = {-1, 0, 1, 0, 0, -1, 0, 1};
    char allowed_slopes[4] = {'^', 'v', '<', '>'};
    int64_t max_distance = 0LL;
    while (p) {
        int64_t a_to_mark = -1;
        int64_t b_to_mark = -1;
        uint64_t branches = 0;
        int64_t original_x = p->x;
        int64_t original_y = p->y;
        for (uint64_t i=0; i<4; i++) {
            int64_t a = original_x + neighbor_offsets[i][0];
            int64_t b = original_y + neighbor_offsets[i][1];
            if (a >= 0 && a < n && b >= 0 && b < m && !p->visited[a][b] && (lines[a][b] == '.' || lines[a][b] == allowed_slopes[i])) {
                branches++;
                if (branches == 1) {
                    p->x = a;
                    p->y = b;
                    p->distance++;
                    a_to_mark = a;
                    b_to_mark = b;
                } else if (branches > 1) {
                    struct point *new = (struct point *) calloc(1, sizeof(struct point));
                    new->x = a;
                    new->y = b;
                    new->distance = p->distance;
                    new->visited = (bool **)calloc(n, sizeof(bool *));
                    for (uint64_t j=0; j<n; j++) {
                        new->visited[j] = (bool *)calloc(m, sizeof(bool));
                        for (uint64_t k=0; k<m; k++) {
                            new->visited[j][k] = p->visited[j][k];
                        }
                    }
                    new->visited[a][b] = true;
                    new->next = p->next;
                    p->next = new;
                }
            }
        }
        if (a_to_mark > 0 && b_to_mark > 0) p->visited[a_to_mark][b_to_mark] = true;

        if (p->x == n-1 || !branches) {
            struct point *current = p;
            p = p->next;
            max_distance = maxll(max_distance, current->distance);
            //printf("%lld\n", current->distance);
            //print_path(lines, current->visited, n, m);
            for (uint64_t i=0; i<n; i++) free(current->visited[i]);
            free(current->visited);
            free(current);
        }
    }

    printf("%lld\n", max_distance);
}