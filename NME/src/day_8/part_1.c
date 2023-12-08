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

#define NODE_SIZE 3
#define ALPHABET_SIZE 26

struct node {
    char location[NODE_SIZE];
    char left[NODE_SIZE];
    char right[NODE_SIZE];
};

void do_work(char **lines, int line_count, const int *chars_per_line);
int idx(char s[NODE_SIZE]);

int main(int argc, char *argv[]) {
    execute_on_input(INPUT_FILE, &do_work);
    return 0;
}

int idx(char s[NODE_SIZE]) {
    return ALPHABET_SIZE*ALPHABET_SIZE*(s[0]-'A') + ALPHABET_SIZE*(s[1] - 'A') + (s[2] - 'A');
}

void do_work(char **lines, int line_count, const int *chars_per_line) {
    int lookup_table_size = ALPHABET_SIZE * ALPHABET_SIZE * ALPHABET_SIZE;
    int* lookup_table = (int *)malloc(sizeof(int) * lookup_table_size);

    struct node *nodes = (struct node *)malloc(sizeof(struct node) * (line_count-2));
    for (int i=2; i<line_count; i++) {
        memcpy(nodes[i-2].location, lines[i], 3);
        memcpy(nodes[i-2].left, &lines[i][7], 3);
        memcpy(nodes[i-2].right , &lines[i][12], 3);
        lookup_table[idx(nodes[i-2].location)] = i-2;
    }

    int steps = 0;
    struct node current = nodes[lookup_table[idx("AAA")]];
    while (current.location[0] != 'Z' && current.location[1] != 'Z' && current.location[2] != 'Z') {
        if (lines[0][steps % chars_per_line[0]] == 'L') {
            current = nodes[lookup_table[idx(current.left)]];
        } else {
            current = nodes[lookup_table[idx(current.right)]];
        }
        steps++;
    }

    printf("%d", steps);

    free(nodes);
    free(lookup_table);
}