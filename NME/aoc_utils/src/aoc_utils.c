#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <assert.h>
#include "aoc_utils/aoc_utils.h"

void execute_on_input(const char *filename, void (*do_work)(char **lines, int line_count, const int *chars_per_line)) {
    clock_t begin = clock();

    /* Step 1: Determine number of lines in our input file */
    FILE *fp = fopen(filename, "r");
    if (!fp) {
        fprintf(stderr,"Error opening file [%s]\n", filename);
        exit(1);
    }
    int num_lines = 0;
    int c;
    while ((c = fgetc(fp)) != EOF) {
        if ((char)c == '\n') {
            num_lines++;
        }
    }
    num_lines++;
    fclose(fp);

    /* Step 2: Determine number of characters on each line */
    fp = fopen(filename, "r");
    if (!fp) {
        fprintf(stderr,"Error opening file [%s]\n", filename);
        exit(1);
    }

    int *c_per_line = (int *) malloc(sizeof(int)*num_lines);
    int current_line_char_count = 0;
    int i = 0;
    while ((c = fgetc(fp)) != EOF) {
        if ((char)c == '\n') {
            c_per_line[i++] = current_line_char_count;
            current_line_char_count = 0;
        } else {
            current_line_char_count++;
        }
    }
    c_per_line[i] = current_line_char_count;
    fclose(fp);

    /* Step 3: Read each line */
    fp = fopen(filename, "r");
    if (!fp) {
        fprintf(stderr,"Error opening file [%s]\n", filename);
        exit(1);
    }

    char **line_array = (char **) malloc(sizeof(char *)*num_lines);
    for (int j=0; j<num_lines; j++) {
        line_array[j] = (char *)malloc(sizeof(char)*(c_per_line[j]+1));
    }
    int line_idx = 0;
    int char_idx = 0;
    while ((c = fgetc(fp)) != EOF) {
        if ((char) c == '\n') {
            line_array[line_idx++][char_idx] = '\0';
            char_idx = 0;
        } else {
            line_array[line_idx][char_idx++] = (char)c;
        }
    }
    line_array[line_idx][char_idx] = '\0';

    fclose(fp);

    clock_t end = clock();
    clock_t file_load = end - begin;


    begin = clock();

    do_work(line_array, num_lines, c_per_line);

    end = clock();
    clock_t program_execution = end - begin;

    begin = clock();
    for (int j=0; j<num_lines; j++) {
        free(line_array[j]);
    }
    free(line_array);
    free(c_per_line);
    end = clock();
    clock_t resources_unload = end - begin;

    printf("                            \n");
    printf("File load:            %ld ms\n", file_load);
    printf("Program execution:    %ld ms\n", program_execution);
    printf("Resources unloaded:   %ld ms\n", resources_unload);
}

int min(int a, int b) {
    return a < b ? a : b;
}

int max(int a, int b) {
    return -min(-a, -b);
}

long long minll(long long a, long long b) {
    return a < b ? a : b;
}

long long maxll(long long a, long long b) {
    return -minll(-a, -b);
}

struct queue *queue_init(void *item) {
    struct queue *q = (struct queue *)malloc(sizeof(struct queue));
    q->item = item;
    q->next = NULL;
    return q;
}


void queue_add(struct queue *q, void *item) {
    assert(q);
    struct queue *prev = q;
    struct queue *curr = q->next;
    while (curr) {
        prev = curr;
        curr = curr->next;
    }
    prev->next = (struct queue *)malloc(sizeof(struct queue));
    prev->next->item = item;
    prev->next->next = NULL;
}

/* *
 * pops first item
 * returns new queue head
 * puts items in item_ptr
 * */
struct queue *queue_pop(struct queue *q, void **item_ptr) {
    assert(q);
    *item_ptr = q->item;
    struct queue *res = q->next;
    free(q);
    return res;
}