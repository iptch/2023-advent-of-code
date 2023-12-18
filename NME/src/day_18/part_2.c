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

enum direction {R,D,L,U};

struct interval {
    long long start;
    long long end;
    bool change;
    struct interval *next;
};

void do_work(char **lines, int line_count, const int *chars_per_line);
struct interval *add_interval(struct interval *i, long long s, long long e, bool change);
long long sum_up(struct interval *i);

int main(int argc, char *argv[]) {
    execute_on_input(INPUT_FILE, &do_work);
    return 0;
}

long long sum_up(struct interval *i) {
    bool out = true;
    struct interval *curr = i;
    long long idx = 0;
    long long res = 0;
    while (curr) {
        if (!out) res += curr->start - idx; // add space between if not outside of border
        res += curr->end - curr->start + 1; // add border
        idx = curr->end + 1; // move index to end of current interval
        if (curr->change) out = !out; // switch inside->outside or outside->inside if interval is inverting
        curr = curr->next; // go to next interval
    }
    return res;
}


struct interval *add_interval(struct interval *i, long long s, long long e, bool change) {
    struct interval *new_interval = (struct interval *)malloc(sizeof(struct interval));
    new_interval->start = s;
    new_interval->end = e;
    new_interval->change = change;

    if (!i) {
        new_interval->next = NULL;
        return new_interval;
    }

    if (s == e && (i->start == s || i->end == s)) {
        free(new_interval);
        return i;
    }

    if (i->start > e) {
        new_interval->next = i;
        return new_interval;
    }

    struct interval *prev = i;
    struct interval *curr = i->next;
    while (curr) {
        if (s == e && (curr->start == s || curr->end == s)) {
            free(new_interval);
            return i;
        }
        if (curr->start > e) {
            new_interval->next = i;
            prev->next = new_interval;
            new_interval->next = curr;
            return i;
        }
        prev = curr;
        curr = curr->next;
    }
    new_interval->next = NULL;
    prev->next = new_interval;
    return i;
}

void do_work(char **lines, int line_count, const int *chars_per_line) {
    long long x = 0; long long y = 0;
    long long maxX = x; long long minX = x;
    long long  maxY = y; long long  minY = y;
    long long  *distances = (long long  *)malloc(sizeof(long long) * line_count);
    enum direction *directions = (enum direction *)malloc(sizeof(enum direction) * line_count);
    for (int i=0; i<line_count; i++) {
        strtok(lines[i], "#") + 2;
        char *hex = strtok(NULL, "#");
        enum direction dir = hex[5] - '0';
        directions[i] = dir;
        hex[5] = '\0';
        long long dist = strtoll(hex, NULL, 16);
        distances[i] = dist;
        switch (dir) {
            case U: x-=dist; minX=minll(minX, x); break;
            case D: x+=dist; maxX=maxll(maxX, x); break;
            case L: y-=dist; minY=minll(minY, y); break;
            case R: y+=dist; maxY=maxll(maxY, y); break;
        }
    }
    long long h = maxX - minX + 1; long long w = maxY - minY + 1;

    struct interval **scan_line = (struct interval **)calloc(h, sizeof(struct interval *));
    x = -minX; y = -minY;
    for (int i=0; i<line_count; i++) {
        switch (directions[i]) {
            case U:
                for (int j=0; j<distances[i]; j++) {
                    scan_line[x] = add_interval(scan_line[x], y, y, true);
                    x--;
                }
                break;
            case D:
                for (int j=0; j<distances[i]; j++) {
                    scan_line[x] = add_interval(scan_line[x], y, y, true);
                    x++;
                }
                break;
            case L:
                for (int j=0; j<distances[i]; j++) y--;
                scan_line[x] = add_interval(scan_line[x], y, y + distances[i], directions[(i-1+line_count)%line_count] == directions[(i+1)%line_count]);
                break;
            case R:
                for (int j=0; j<distances[i]; j++) y++;
                scan_line[x] = add_interval(scan_line[x], y - distances[i], y, directions[(i-1)%line_count] == directions[(i+1)%line_count]);
                break;
        }
    }

    long long res = 0;
    for (int i=0; i<h; i++) res += sum_up(scan_line[i]);

    printf("%lld\n", res);

    free(distances);
    free(directions);
    free(scan_line);
}