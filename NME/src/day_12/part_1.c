#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>
#include <ctype.h>
#include "aoc_utils/aoc_utils.h"

//#define IS_EXAMPLE
#ifdef IS_EXAMPLE
#define INPUT_FILE "example2.txt"
#else
#define INPUT_FILE "input.txt"
#endif

void do_work(char **lines, int line_count, const int *chars_per_line);
int count(char *record, int record_size, int *counts, int count_idx, int max_count);
int count_memo(char *record, int record_size, int *counts, int count_idx, int max_count);
bool spring_fits(char *record, int spring_length);

int main(int argc, char *argv[]) {
    execute_on_input(INPUT_FILE, &do_work);
    return 0;
}

bool spring_fits(char *record, int spring_length) {
    for (int i=0; i<spring_length; i++) {
        if (record[i] == '.') return false;
    }
    return true;
}

int count_memo(char *record, int record_size, int *counts, int count_idx, int max_count) {
    return count(record, record_size, counts, count_idx, max_count);
}


int count(char *record, int record_size, int *counts, int count_idx, int max_count) {
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
    int left = count_memo(record, record_size, counts, count_idx, max_count);
    record[0] = '?';
    // replace ? by .
    return left + count_memo(record + 1, record_size - 1, counts, count_idx, max_count);
}


void do_work(char **lines, int line_count, const int *chars_per_line) {
    int res = 0;
    for (int i=0; i<line_count; i++) {
        strtok(lines[i], " ");
        char *counts = strtok(NULL, " ");
        int commas = 0;
        for (int i=0; i< strlen(counts); i++) {
            if (counts[i] == ',') commas++;
        }
        int *groups = (int *)malloc(sizeof(int) * (commas + 1));
        counts = strtok(counts, ",");
        int group_counter = 0;
        while (counts) {
            groups[group_counter++] = atoi(counts);
            counts = strtok(NULL, ",");
        }

        res += count_memo(lines[i], strlen(lines[i]), groups, 0, group_counter);

        free(groups);
    }
    printf("%d\n", res);

}