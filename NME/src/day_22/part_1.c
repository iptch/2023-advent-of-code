#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>
#include <stdint.h>
#include "aoc_utils/aoc_utils.h"

//#define IS_EXAMPLE
#ifdef IS_EXAMPLE
#define INPUT_FILE "example1.txt"
#else
#define INPUT_FILE "input.txt"
#endif

struct point {int32_t x; int32_t y; int32_t z;};
struct brick {struct point *start; struct point *end;};

void do_work(char **lines, int line_count, const int *chars_per_line);
int compare_bricks(const void *brick_ptr_ptr_one, const void *brick_ptr_ptr_two);
void drop_brick(struct brick **bricks, size_t brick_index, size_t n);
bool intersect(struct brick *first, struct brick *second);
bool intersect_any(struct brick **bricks, size_t brick_index, size_t n);
bool can_disintegrate(struct brick **bricks, size_t brick_index, size_t n);
int64_t support_count(struct brick **bricks, size_t brick_index, size_t n);


int main(int argc, char *argv[]) {
    execute_on_input(INPUT_FILE, &do_work);
    return 0;
}

int compare_bricks(const void *brick_ptr_ptr_one, const void *brick_ptr_ptr_two) {
    return ((struct brick **)brick_ptr_ptr_one)[0]->start->z - ((struct brick **)brick_ptr_ptr_two)[0]->start->z;
}

int64_t support_count(struct brick **bricks, size_t brick_index, size_t n) {
    struct brick *b = bricks[brick_index];
    struct point start = {b->start->x, b->start->y, b->start->z-1};
    struct point end = {b->end->x, b->end->y, b->start->z-1};
    struct brick lower_brick = {&start, &end};

    int64_t supports = 0;
    for (size_t i=0; i<n; i++) supports += intersect(&lower_brick, bricks[i]);
    return supports;
}

bool can_disintegrate(struct brick **bricks, size_t brick_index, size_t n) {
    struct brick *b = bricks[brick_index];
    struct point start = {b->start->x, b->start->y, b->end->z+1};
    struct point end = {b->end->x, b->end->y, b->end->z+1};
    struct brick upper_brick = {&start, &end};

    for (size_t i=0; i<n; i++) {
        if (intersect(&upper_brick, bricks[i]) && support_count(bricks, i, n) == 1) return false;
    }
    return true;
}

bool intersect_any(struct brick **bricks, size_t brick_index, size_t n) {
    bool result = false;
    for (size_t i=0; i<n; i++) {
        if (i != brick_index) result |= intersect(bricks[brick_index], bricks[i]);
    }
    return result;
}

bool intersect(struct brick *first, struct brick *second) {
    bool result = false;
    for (size_t first_x = first->start->x; first_x <= first->end->x; first_x++) {
        for (size_t first_y = first->start->y; first_y <= first->end->y; first_y++) {
            for (size_t first_z = first->start->z; first_z <= first->end->z; first_z++) {
                for (size_t second_x = second->start->x; second_x <= second->end->x; second_x++) {
                    for (size_t second_y = second->start->y; second_y <= second->end->y; second_y++) {
                        for (size_t second_z = second->start->z; second_z <= second->end->z; second_z++) {
                            result |= first_x == second_x && first_y == second_y && first_z == second_z;
                        }
                    }
                }
            }
        }
    }
    return result;
}

void drop_brick(struct brick **bricks, size_t brick_index, size_t n) {
    struct brick *b = bricks[brick_index];
    b->start->z--; b->end->z--;
    while (b->start->z && !intersect_any(bricks, brick_index, n)) {b->start->z--; b->end->z--;}
    b->start->z++; b->end->z++;
}

void do_work(char **lines, int line_count, const int *chars_per_line) {
    struct brick **bricks = (struct brick **)calloc(line_count, sizeof(struct brick *));

    for (size_t i=0; i<line_count; i++) {
        bricks[i] = (struct brick *)calloc(1, sizeof(struct brick));
        struct point *start = (struct point *)calloc(1, sizeof(struct point));
        struct point *end = (struct point *)calloc(1, sizeof(struct point));

        start->x = atoi(strtok(lines[i], ","));
        start->y = atoi(strtok(NULL, ","));
        start->z = atoi(strtok(NULL, "~"));
        end->x = atoi(strtok(NULL, ","));
        end->y = atoi(strtok(NULL, ","));
        end->z = atoi(strtok(NULL, ","));

        bricks[i]->start = start;
        bricks[i]->end = end;
    }

    int64_t res = 0;

    qsort(bricks, line_count, sizeof(struct brick *), compare_bricks);
    for (size_t i=0; i<line_count; i++) drop_brick(bricks, i, line_count);
    for (size_t i=0; i<line_count; i++) res += can_disintegrate(bricks, i, line_count);

    printf("%lld\n", res);
}