#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>
#include <ctype.h>
#include <stdint.h>
#include "aoc_utils/aoc_utils.h"

//#define IS_EXAMPLE
#ifdef IS_EXAMPLE
#define INPUT_FILE "example1.txt"
#else
#define INPUT_FILE "input.txt"
#endif

struct node {
    uint_fast64_t id;
    int neigh_count;
    struct node **neighs;
    int dists[4];
    int x;
    int y;
};

void do_work(char **lines, int line_count, const int *chars_per_line);
void print_path(char **lines, uint64_t n, uint64_t m);
struct node *find_node(struct node **nodes, int x, int y, int n);
struct node *init_node(int x, int y, int idx);
void print_graph(struct node **nodes, int n);
int longest_path(struct node *start, uint_fast64_t visited);
struct node **build_graph(char **lines, int line_count, const int *chars_per_line, int *num_nodes);

int main(int argc, char *argv[]) {
    execute_on_input(INPUT_FILE, &do_work);
    return 0;
}

int longest_path(struct node *start, uint_fast64_t visited) {
    if (start->neigh_count == 0) return 0;
    int res = INT_MIN;
    for (int i=0; i<start->neigh_count; i++) {
        if (!(1LL << start->neighs[i]->id & visited)) {
            int d = start->dists[i] + longest_path(start->neighs[i], visited | 1LL << start->id);
            if (d > res) res = d;
        }
    }
    return res;
}

void print_graph(struct node **nodes, int n) {
    printf("graph {\n");
    for (int i=0; i<n; i++) {
        for (int j=0; j<nodes[i]->neigh_count; j++) {
            if (nodes[i]->id < nodes[i]->neighs[j]->id)
                printf("%d -- %d [label=%d]\n", nodes[i]->id, nodes[i]->neighs[j]->id, nodes[i]->dists[j]);
        }
    }
    printf("}\n");
}

struct node *init_node(int x, int y, int id) {
    struct node *new_node = (struct node *)calloc(1, sizeof(struct node));
    new_node->neigh_count = 0;
    new_node->x = x;
    new_node->y = y;
    new_node->id = id;
    new_node->neighs = (struct node **)calloc(4, sizeof(struct node *));
    return new_node;
}

struct node *find_node(struct node **nodes, int x, int y, int n) {
    for (int i=0; i<n; i++) if (nodes[i]->x == x && nodes[i]->y == y) return nodes[i];
    return NULL;
}

void print_path(char **lines, uint64_t n, uint64_t m) {
    for (uint64_t i=0; i<n; i++) {
        for (uint64_t j=0; j<m; j++) {
            printf("%c", lines[i][j]);
        }
        printf("\n");
    }
    printf("\n");
}

struct node **build_graph(char **lines, int line_count, const int *chars_per_line, int *num_nodes) {
    int n = line_count;
    int m = chars_per_line[0];

    int neighbor_offsets[4][2] = {-1, 0, 1, 0, 0, -1, 0, 1};
    int intersection_count = 0;
    for (int i=0; i<n; i++) {
        for (int j=0; j<m; j++) {
            if (lines[i][j] != '#') lines[i][j] = '.';
            int neighs = 0;
            for (int k=0; k<4; k++) {
                int a = i + neighbor_offsets[k][0];
                int b = j + neighbor_offsets[k][1];
                if (a>=0 && a<n && b>=0 && b<m && lines[a][b] != '#' && lines[i][j] != '#') neighs++;
            }
            if (neighs > 2) {
                intersection_count++;
                lines[i][j] = 'I';
            }
        }
    }
    lines[0][1] = 'I';
    lines[n-1][m-2] = 'I';

    struct node **nodes = (struct node **)calloc(intersection_count + 2, sizeof(struct node *));
    int node_idx = 0;
    for (int i=0; i<n; i++) {
        for (int j=0; j<m; j++) {
            if (lines[i][j] == 'I') {
                nodes[node_idx] = init_node(i, j, node_idx);
                node_idx++;
            }
        }
    }

    intersection_count+=2;

    bool **visited = (bool **)calloc(n, sizeof(bool *));
    for (uint64_t i=0; i<n; i++) visited[i] = (bool *)calloc(m, sizeof(bool));

    for (int i=0; i<n; i++) {
        for (int j=0; j<m; j++) {
            if (lines[i][j] == 'I') {
                struct node *node_start = find_node(nodes, i, j, intersection_count);
                for (int k=0; k<4; k++) {
                    int a = i + neighbor_offsets[k][0];
                    int b = j + neighbor_offsets[k][1];
                    if (a>=0 && a<n && b>=0 && b<m && !visited[a][b] && lines[a][b] != '#') {
                        int dist = 0;
                        while (lines[a][b] != 'I') {
                            visited[a][b] = true;
                            dist++;
                            for (int l=0; l<4; l++) {
                                int x = a + neighbor_offsets[l][0];
                                int y = b + neighbor_offsets[l][1];
                                if (x >= 0 && x < n && y >= 0 && y < m && ((!visited[x][y] && lines[x][y] == '.') || (lines[x][y] == 'I' && dist > 1))) {
                                    visited[x][y] = true;
                                    a = x;
                                    b = y;
                                    break;
                                }
                            }
                        }
                        struct node *node_end = find_node(nodes, a, b, intersection_count);

                        node_start->neighs[node_start->neigh_count] = node_end;
                        node_start->dists[node_start->neigh_count] = dist+1;
                        node_start->neigh_count++;

                        node_end->neighs[node_end->neigh_count] = node_start;
                        node_end->dists[node_end->neigh_count] = dist+1;
                        node_end->neigh_count++;
                    }
                }
            }
        }
    }

    nodes[intersection_count-1]->neigh_count = 0;
    *num_nodes = intersection_count;
    return nodes;
}

void do_work(char **lines, int line_count, const int *chars_per_line) {
    int num_nodes;
    struct node **graph = build_graph(lines, line_count, chars_per_line, &num_nodes);

    //print_path(lines, n, m);
    //print_graph(graph, num_nodes);

    printf("%d\n", longest_path(graph[0], 0));
}