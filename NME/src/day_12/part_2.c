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

#define MAX_LINE_LENGTH 105
#define MAX_SPRINGS 31
#define MAX_STATES 4

long long memo[MAX_LINE_LENGTH][MAX_SPRINGS][MAX_STATES];

void do_work(char **lines, int line_count, const int *chars_per_line);
long long count(char *record, int record_size, int *counts, int count_idx, int max_count);
long long count_memo(char *record, int record_size, int *counts, int count_idx, int max_count);
bool spring_fits(const char *record, int spring_length);
void reset_memo();

int main(int argc, char *argv[]) {
    execute_on_input(INPUT_FILE, &do_work);
    return 0;
}

void reset_memo() {
    for (int i=0; i<MAX_LINE_LENGTH; i++) {
        for (int j=0; j<MAX_SPRINGS; j++) {
            for (int k=0; k<MAX_STATES; k++) {
                memo[i][j][k] = -1L;
            }
        }
    }
}

bool spring_fits(const char *record, int spring_length) {
    for (int i=0; i<spring_length; i++) {
        if (record[i] == '.') return false;
    }
    return true;
}

long long count_memo(char *record, int record_size, int *counts, int count_idx, int max_count) {
    long long state;
    switch (record[0]) {
        case '\0':
            state = 0L;
            break;
        case '.':
            state = 1L;
            break;
        case '#':
            state = 2L;
            break;
        case '?':
            state = 3L;
            break;
        default:
            fprintf(stderr,"Unexpected character [%c]\n", record[0]);
            exit(1);
    }
    if (record[0] == '\0') state = 0L;
    if (memo[record_size][count_idx][state] == -1L) {
        memo[record_size][count_idx][state] = count(record, record_size, counts, count_idx, max_count);
    }
    return memo[record_size][count_idx][state];
}


long long count(char *record, int record_size, int *counts, int count_idx, int max_count) {
    while (record[0] == '.') { // remove leading dots
        record++;
        record_size--;
    }

    if (strlen(record) == 0) return max_count == count_idx; // '', () is legal

    if (max_count == count_idx) { // s, () is legal as long as there are not #
        bool has_hash = false;
        for (int i=0; i<record_size; i++) {
            if(record[i] == '#') has_hash = true;
        }
        return !has_hash;
    }

    // record starts with #, pop one string
    if (record[0] == '#') {
        if (record_size < counts[count_idx] || !spring_fits(record, counts[count_idx])) return 0; // spring does not fit
        if (record_size == counts[count_idx]) return count_idx == max_count - 1; // fill up, only one spring left
        if (record[counts[count_idx]] == '#') return 0; // must be separated by . or ?
        return count_memo(record + counts[count_idx] + 1, record_size - counts[count_idx] - 1, counts, count_idx+1, max_count); //pop one spring
    }

    // replace ? by #
    record[0] = '#';
    long long left = count_memo(record, record_size, counts, count_idx, max_count);
    record[0] = '?';
    // replace ? by .
    return left + count_memo(record + 1, record_size - 1, counts, count_idx, max_count);
}


void do_work(char **lines, int line_count, const int *chars_per_line) {
    long long res = 0;
    for (int i=0; i<line_count; i++) {
        strtok(lines[i], " ");
        char *counts = strtok(NULL, " ");
        int commas = 0;
        for (int j=0; j< strlen(counts); j++) {
            if (counts[j] == ',') commas++;
        }
        int *groups = (int *)malloc(sizeof(int) * (commas + 1));
        counts = strtok(counts, ",");
        int group_counter = 0;
        while (counts) {
            groups[group_counter++] = atoi(counts);
            counts = strtok(NULL, ",");
        }

        int line_length = strlen(lines[i]);
        char *record_long = (char *)malloc(sizeof(char) * ((line_length * 5) + 5));
        int *groups_long = (int *)malloc(sizeof(int) * (group_counter * 5));
        for (int k=0; k<5; k++) {
            for (int j = 0; j < line_length + 1; j++) {
                record_long[k*line_length + j + k] = lines[i][j];
            }
            record_long[(k+1) * line_length + k] = '?';
        }
        record_long[line_length * 5 + 4] = '\0';
        for (int j=0; j<group_counter * 5; j++) {
            groups_long[j] = groups[j%group_counter];
        }

        reset_memo();
        res += count_memo(record_long, line_length * 5 + 4, groups_long, 0, group_counter * 5);

        free(groups_long);
        free(record_long);
        free(groups);
    }
    printf("%lld\n", res);
}