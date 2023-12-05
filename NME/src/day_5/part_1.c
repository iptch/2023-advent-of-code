#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>
#include <ctype.h>
#include "aoc_utils/aoc_utils.h"

//#define IS_EXAMPLE
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

void do_work(char **lines, int line_count, const int *chars_per_line);
long long map_seed(long long seed, struct map *m);

int main(int argc, char *argv[]) {
    execute_on_input(INPUT_FILE, &do_work);
    return 0;
}

long long map_seed(long long seed, struct map *m) {
    if (seed < m->source || seed > m->source + m->range) {
        return -1LL;
    }
    return seed + (m->destination - m->source);
}

void do_work(char **lines, int line_count, const int *chars_per_line) {
    long long seeds[NUM_SEEDS];
    strtok(lines[0], " ");
    char *ptr = strtok(NULL, " ");
    int a=0;
    while (ptr) {
        seeds[a++] = atoll(ptr);
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
    for (int i=0; i<NUM_SEEDS; i++) {
        long long seed = seeds[i];
        for (int j=0; j<NUM_MAPS; j++) {
            for (int k=0; k<maps_per_map[j]; k++) {
                long long new_seed = map_seed(seed, &maps[j][k]);
                if (new_seed != -1LL) {
                    seed = new_seed;
                    break;
                }
            }
        }
        res = minll(res, seed);
    }

    printf("%lld", res);

    for (int i=0; i<NUM_MAPS; i++) {
        free(maps[i]);
    }
    free(maps);
}