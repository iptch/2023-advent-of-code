#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>
#include <ctype.h>
#include "aoc_utils/aoc_utils.h"

//#define IS_EXAMPLE
#define DEBUG 0
#ifdef IS_EXAMPLE
#define INPUT_FILE "example1.txt"
#define NUM_SEEDS 4
#else
#define INPUT_FILE "input.txt"
#define NUM_SEEDS 20
#endif

#define NUM_MAPS 7

struct map {
    long long source;
    long long destination;
    long long range;
};

struct interval {
    long long start;
    long long end;
    struct interval *next;
};

void do_work(char **lines, int line_count, const int *chars_per_line);
size_t add_interval(struct interval *start, struct interval *to_add);
struct interval *get_interval(struct interval *start);
bool map_interval(struct interval *i, struct map m, struct interval *o1, struct interval *o2, struct interval *o3);
bool intersect(long long start_a, long long end_a, long long start_b, long long end_b);

int main(int argc, char *argv[]) {
    execute_on_input(INPUT_FILE, &do_work);
    return 0;
}

bool intersect(long long start_a, long long end_a, long long start_b, long long end_b) {
    return (start_a <= end_b) && (end_a >= start_b);
}


bool map_interval(struct interval *i, struct map m, struct interval *o1, struct interval *o2, struct interval *o3) {
    if (!intersect(i->start, i->end, m.source, m.source + m.range - 1LL)) {
        o1->start = i->start;
        o1->end = i->end;
        o2->start = -1LL;
        o3->start = -1LL;
        return false;
    }

    long long start = maxll(i->start, m.source);
    long long end = minll(i->end, m.source + m.range - 1LL);
    long long displacement = m.destination - m.source;

    o2->start = start + displacement;
    o2->end = end + displacement;

    if (i->start < start) {
        o1->start = i->start;
        o1->end = start - 1LL;
    } else {
        o1->start = -1LL;
    }

    if (i->end > end) {
        o3->start = end+1LL;
        o3->end = i->end;
    } else {
        o3->start = -1LL;
    }
    return true;
}

size_t add_interval(struct interval *start, struct interval *to_add) {
    size_t res = 1;
    struct interval *current = start;
    while (current->next) {
        if (intersect(current->start, current->end, to_add->start, to_add->end)) {
            current->start = minll(current->start, to_add->start);
            current->end = maxll(current->end, to_add->end);
            while (current->next) {
                current = current->next;
                res++;
            }
            free(to_add);
            return res;
        }
        res++;
        current = current->next;
    }
    if (intersect(current->start, current->end, to_add->start, to_add->end)) {
        current->start = minll(current->start, to_add->start);
        current->end = maxll(current->end, to_add->end);
        free(to_add);
        return res;
    }
    current->next = to_add;
    current->next->next = NULL;
    return res+1;
}

struct interval *get_interval(struct interval *start) {
    struct interval *res = start->next;
    start->next = res->next;
    res->next = NULL;
    return res;
}



void do_work(char **lines, int line_count, const int *chars_per_line) {
    struct interval **seed_intervals = (struct interval **)malloc(sizeof(struct interval *) * (NUM_SEEDS >> 1));
    strtok(lines[0], " ");
    char *ptr = strtok(NULL, " ");
    int a=0;
    while (ptr) {
        struct interval *in = (struct interval *)malloc(sizeof(struct interval));
        in->start = atoll(ptr);
        in->end = atoll(strtok(NULL, " ")) + in->start - 1LL;
        in->next = NULL;
        seed_intervals[a++] = in;
        ptr = strtok(NULL, " ");
    }

    int maps_per_map[NUM_MAPS];
    int b = 0;
    int c = 0;
    for (int i=3; i<line_count; i++) {
        if (strstr(lines[i], "map")) {
            maps_per_map[c] = b-1;
            b = 0;
            c++;
        } else {
            b++;
        }
    }
    maps_per_map[c] = b;

    struct map **maps = (struct map **)malloc(sizeof(struct map *) * NUM_MAPS);
    for (int i=0; i<NUM_MAPS; i++) {
        maps[i] = (struct map *)malloc(sizeof(struct map) * maps_per_map[i]);
    }

    int line_num = 1;
    for (int i=0; i<NUM_MAPS; i++) {
        line_num += 2;
        for (int j=0; j<maps_per_map[i]; j++) {
            struct map current_map;
            current_map.destination = atoll(strtok(lines[line_num++], " "));
            current_map.source = atoll(strtok(NULL, " "));
            current_map.range = atoll(strtok(NULL, " "));
            maps[i][j] = current_map;
        }
    }

    long long res = LLONG_MAX;
    for (int u=0; u<NUM_SEEDS >> 1; u++) {
        struct interval *start_interval = malloc(sizeof(struct interval));
        start_interval->next = NULL;
        start_interval->start = -1LL;
        start_interval->end = -1LL;
        add_interval(start_interval, seed_intervals[u]);

        for (int j = 0; j < NUM_MAPS; j++) {

            if (DEBUG) {
                struct interval *current_ii = start_interval->next;
                while (current_ii) {
                    printf("[%lld,%lld] ", current_ii->start, current_ii->end);
                    current_ii = current_ii->next;
                }
                printf("\n");
            }

            struct interval *new_start_interval = malloc(sizeof(struct interval));
            new_start_interval->next = NULL;
            new_start_interval->start = -1LL;
            new_start_interval->end = -1LL;
            while(start_interval->next) {
                struct interval *current_interval = get_interval(start_interval);
                bool mapped = false;
                for (int k = 0; k < maps_per_map[j]; k++) {
                    struct interval *first_interval = malloc(sizeof(struct interval));
                    struct interval *second_interval = malloc(sizeof(struct interval));
                    struct interval *third_interval = malloc(sizeof(struct interval));
                    if (map_interval(current_interval, maps[j][k], first_interval, second_interval, third_interval)) {
                        if (first_interval->start != -1LL) {
                            add_interval(start_interval, first_interval);
                        } else {
                            free(first_interval);
                        }
                        add_interval(new_start_interval, second_interval);
                        if (third_interval->start != -1LL) {
                            add_interval(start_interval, third_interval);
                        } else {
                            free(third_interval);
                        }
                        mapped = true;
                        break;
                    }
                }
                if (!mapped) {
                    add_interval(new_start_interval, current_interval);
                }
            }

            free(start_interval);
            start_interval = new_start_interval;
        }

        if (DEBUG) {
            struct interval *current_ii = start_interval->next;
            while (current_ii) {
                printf("[%lld,%lld] ", current_ii->start, current_ii->end);
                current_ii = current_ii->next;
            }
            printf("\n\n");
        }

        struct interval *current_i = start_interval->next;
        while (current_i) {
            res = minll(current_i->start, res);
            free(current_i);
            current_i = current_i->next;
        }
        free(start_interval);
    }
    printf("%lld", res);

    free(seed_intervals);
    for (int i=0; i<NUM_MAPS; i++) {
        free(maps[i]);
    }
    free(maps);
}