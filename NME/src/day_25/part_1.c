#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>
#include <ctype.h>
#include <stdint.h>
#include "aoc_utils/aoc_utils.h"

//#define IS_EXAMPLE
#ifdef IS_EXAMPLE
#define NODE_1_EDGE_1 "hfx"
#define NODE_2_EDGE_1 "pzl"
#define NODE_1_EDGE_2 "bvb"
#define NODE_2_EDGE_2 "cmg"
#define NODE_1_EDGE_3 "nvd"
#define NODE_2_EDGE_3 "jqt"
#define INPUT_FILE "example1.txt"
#else
#define NODE_1_EDGE_1 "kzh"
#define NODE_2_EDGE_1 "rks"
#define NODE_1_EDGE_2 "dgt"
#define NODE_2_EDGE_2 "tnz"
#define NODE_1_EDGE_3 "ddc"
#define NODE_2_EDGE_3 "gqm"
#define INPUT_FILE "input.txt"
#endif

typedef struct Node {
    char *name;
    bool visited;
    int neighbors_count;
    struct Node **neighbors;
    struct Node *next;
} Node;

void do_work(char **lines, int line_count, const int *chars_per_line);
Node *add_node(Node *first_node, char *name);
Node *find_node(Node *first_node, char *name_to_find);
bool is_critical_edge(char *a, char *b);
int64_t compute_component_size(Node *start);

int main(int argc, char *argv[]) {
    execute_on_input(INPUT_FILE, &do_work);
    return 0;
}

int64_t compute_component_size(Node *start) {
    if (start->visited) return 0;
    start->visited = true;
    int64_t res = 1LL;
    for (int i=0; i<start->neighbors_count; i++) res += compute_component_size(start->neighbors[i]);
    return res;
}

bool is_critical_edge(char *a, char *b) {
    if (strcmp(a, NODE_1_EDGE_1) == 0 && strcmp(b, NODE_2_EDGE_1) == 0) return true;
    if (strcmp(a, NODE_2_EDGE_1) == 0 && strcmp(b, NODE_1_EDGE_1) == 0) return true;

    if (strcmp(a, NODE_1_EDGE_2) == 0 && strcmp(b, NODE_2_EDGE_2) == 0) return true;
    if (strcmp(a, NODE_2_EDGE_2) == 0 && strcmp(b, NODE_1_EDGE_2) == 0) return true;

    if (strcmp(a, NODE_1_EDGE_3) == 0 && strcmp(b, NODE_2_EDGE_3) == 0) return true;
    if (strcmp(a, NODE_2_EDGE_3) == 0 && strcmp(b, NODE_1_EDGE_3) == 0) return true;

    return false;
}

Node *add_node(Node *first_node, char *name) {
    Node *new_node = (Node *)calloc(1, sizeof(Node));
    new_node->name = name;
    new_node->next = first_node->next;
    new_node->neighbors = (Node **)calloc(20, sizeof(Node *));
    first_node->next = new_node;
    return new_node;
}

Node *find_node(Node *first_node, char *name_to_find) {
    Node *current = first_node;
    while (current) {
        if (strcmp(name_to_find, current->name) == 0) return current;
        current = current->next;
    }
    return NULL;
}



void do_work(char **lines, int line_count, const int *chars_per_line) {
    Node *head = (Node *)calloc(1, sizeof(Node));
    head->name = "dummy_node";

    for (int i=0; i<line_count; i++) {
        char *source_name = strtok(lines[i], ":");
        Node *source = find_node(head, source_name);
        if (!source) source = add_node(head, source_name);

        char *dest_name = strtok(NULL, " ");
        while (dest_name) {
            Node *dest = find_node(head, dest_name);
            if (!dest) dest = add_node(head, dest_name);

            if (!is_critical_edge(source_name, dest_name)) {
                dest->neighbors[dest->neighbors_count++] = source;
                source->neighbors[source->neighbors_count++] = dest;
            } else {
                printf("critical edge skipped: %s -> %s\n", source_name, dest_name);
            }
            dest_name = strtok(NULL, " ");
        }
    }

    int64_t component_one_size = compute_component_size(find_node(head, NODE_1_EDGE_1));
    int64_t component_two_size = compute_component_size(find_node(head, NODE_2_EDGE_1));

    printf("%lld * %lld = %lld\n", component_one_size, component_two_size, component_one_size*component_two_size);
}