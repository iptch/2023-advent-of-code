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

struct map_entry {
    char *label;
    long long focal_length;
    struct map_entry *next;
};

void do_work(char **lines, int line_count, const int *chars_per_line);
int hash(const char *label, int n);
void remove_lens(const char *label);
void add_lens(char *label, int focal_length);
long long compute_score();
void init_hashmap();

struct map_entry *HASH_MAP[256];

int main(int argc, char *argv[]) {
    execute_on_input(INPUT_FILE, &do_work);
    return 0;
}

void init_hashmap() {
    for (int i=0; i<256; i++) {
        HASH_MAP[i] = NULL;
    }
}

long long compute_score() {
    long long res = 0;
    for (int i=0; i<256; i++) {
        if (HASH_MAP[i]) {
            long long box_pos = 1L;
            struct map_entry *current = HASH_MAP[i];
            while (current) {
                res += ((i+1) * box_pos++ * current->focal_length);
                current = current->next;
            }
        }
    }
    return res;
}

int hash(const char *label, int n) {
    int res = 0;
    for (int i=0; i<n; i++) {
        res = 17*(res + label[i]);
        res = res % 256;
    }
    return res;
}

void remove_lens(const char *label) {
    int box = hash(label, strlen(label));
    struct map_entry *prev = HASH_MAP[box];

    if (!prev) {
        return;
    }

    if (!strcmp(prev->label, label)) {
        HASH_MAP[box] = prev->next;
        free(prev);
        return;
    }

    struct map_entry *current = prev->next;
    while (current) {
        if (!strcmp(current->label, label)) {
            prev->next = current->next;
            free(current);
            return;
        }

        prev = current;
        current = current->next;
    }
}

void add_lens(char *label, int focal_length) {
    int box = hash(label, strlen(label));
    struct map_entry *current = HASH_MAP[box];

    if (!current) {
        HASH_MAP[box] = (struct map_entry *)malloc(sizeof(struct map_entry));
        HASH_MAP[box]->label = label;
        HASH_MAP[box]->focal_length = focal_length;
        HASH_MAP[box]->next = NULL;
        return;
    }

    while (current) {

        if (!strcmp(current->label, label)) {
            current->focal_length = focal_length;
            return;
        }

        if (!current->next) {
            current->next = (struct map_entry *)malloc(sizeof(struct map_entry));
            current->next->label = label;
            current->next->focal_length = focal_length;
            current->next->next = NULL;
            return;
        }

        current = current->next;
    }
}


void do_work(char **lines, int line_count, const int *chars_per_line) {
    init_hashmap();
    char *current_instruction = strtok(lines[0], ",");
    while (current_instruction) {
        size_t ins_len = strlen(current_instruction);
        if (current_instruction[ins_len - 2] == '=') {
            int focal_length = atoi(current_instruction + strlen(current_instruction) - 1);
            current_instruction[ins_len- 2] = '\0';
            add_lens(current_instruction, focal_length);
        } else {
            current_instruction[ins_len - 1] = '\0';
            remove_lens(current_instruction);
        }
        current_instruction = strtok(NULL, ",");
    }
    printf("%lld\n", compute_score());
}