#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>
#include <ctype.h>
#include "aoc_utils/aoc_utils.h"

#define IS_EXAMPLE
#ifdef IS_EXAMPLE
#define INPUT_FILE "example1.txt"
#else
#define INPUT_FILE "input.txt"
#endif

struct step {
    char *name;
    char condition_variable;
    char condition_operation;
    int condition_constant;
    struct step *next_if_true;
    struct step *next_if_false;
};

struct part {
    long long x_min; long long x_max;
    long long m_min; long long m_max;
    long long a_min; long long a_max;
    long long s_min; long long s_max;
    struct step *current_step;
    struct part *next_part;
};


void do_work(char **lines, int line_count, const int *chars_per_line);
struct step *find(struct step **steps, const char *name, size_t n);
struct part *add(struct part *head, struct part *new_part);
void print_part_chain(struct part *head);

int main(int argc, char *argv[]) {
    execute_on_input(INPUT_FILE, &do_work);
    return 0;
}

void print_part_chain(struct part *head) {
    struct part *curr = head;
    while (curr) {
        printf("%s x(%lld,%lld), m(%lld,%lld), a(%lld,%lld), s(%lld,%lld) | ", curr->current_step->name, curr->x_min, curr->x_max, curr->m_min, curr->m_max, curr->a_min, curr->a_max, curr->s_min, curr->s_max);
        curr = curr->next_part;
    }
    printf("\n");
}


struct part *add(struct part *head, struct part *new_part) {
    if (!head) return new_part;
    new_part->next_part = head->next_part;
    head->next_part = new_part;
    return head;
}

struct step *find(struct step **steps, const char *name, size_t n) {
    for (int i=0; i<n; i++) {
        if (!strcmp(steps[i]->name, name)) return steps[i];
    }
    return NULL;
}

void do_work(char **lines, int line_count, const int *chars_per_line) {
    struct step **steps = (struct step **)malloc(sizeof(struct step *) * line_count);
    int step_idx = 2;

    steps[0] = (struct step *)calloc(1, sizeof(struct step));
    steps[0]->name = "A";

    steps[1] = (struct step *)calloc(1, sizeof(struct step));
    steps[1]->name = "R";


    for (int i=0; i<line_count; i++) {
        if (chars_per_line[i] == 0) break;

        char *rest = strstr(lines[i], "{");
        size_t l = rest - lines[i];
        char *name = (char *)malloc(sizeof(char) * (l + 1));
        strncpy(name, rest - l, l);
        name[l] = '\0';
        struct step *s = (struct step *)calloc(1, sizeof(struct step));
        s->name = name;
        steps[step_idx++] = s;

    }

    for (int i=0; i<step_idx-2; i++) {
        char *name = strtok(lines[i], "{");
        size_t name_len = strlen(name);
        struct step *current = find(steps, name, step_idx);
        struct step *previous = NULL;
        char *transition = strtok(NULL, ",");
        char condition_count = '0';
        while (transition) {
            if (transition[1] == '<' || transition[1] == '>') {
                char var = transition[0];
                char condition = transition[1];
                char *if_true = strstr(transition + 2, ":") + 1;
                if_true[-1] = '\0';
                char *condition_constant = transition + 2;

                current->condition_variable = var;
                current->condition_operation = condition;
                current->condition_constant = atoi(condition_constant);
                current->next_if_true = find(steps, if_true, step_idx);
                //printf("%s -> %s\n", current->name, current->next_if_true->name);

                if (previous) {
                    previous->next_if_false = current;
                    //printf("%s -> %s\n", previous->name, previous->next_if_false->name);
                }

                previous = current;
                current = (struct step *)calloc(1, sizeof(struct step));
                char *new_name = (char *)malloc(sizeof(char) * (name_len + 2));
                strcpy(new_name, name);
                new_name[name_len] = condition_count++;
                new_name[name_len+1] = '\0';
                current->name = new_name;
            } else {
                transition[strlen(transition) - 1] = '\0';
                previous->next_if_false = find(steps, transition, step_idx);
                //printf("%s -> %s\n", previous->name, previous->next_if_false->name);
                free(current);
            }
            transition = strtok(NULL, ",");
        }
    }

    struct step *start = find(steps, "in", step_idx);
    struct part *head = (struct part *)calloc(1, sizeof(struct part));
    head->x_min = 1; head->x_max = 4000;
    head->m_min = 1; head->m_max = 4000;
    head->a_min = 1; head->a_max = 4000;
    head->s_min = 1; head->s_max = 4000;
    head->current_step = start;
    head->next_part = NULL;

    long long res = 0LL;
    while (head) {
        //print_part_chain(head);
        char v = head->current_step->condition_variable;
        char o = head->current_step->condition_operation;
        int n = head->current_step->condition_constant;
        struct step *nt = head->current_step->next_if_true;
        struct step *nf = head->current_step->next_if_false;

        struct part *new_part = (struct part *)calloc(1, sizeof(struct part));
        new_part->x_min = head->x_min; new_part->x_max = head->x_max;
        new_part->m_min = head->m_min; new_part->m_max = head->m_max;
        new_part->a_min = head->a_min; new_part->a_max = head->a_max;
        new_part->s_min = head->s_min; new_part->s_max = head->s_max;
        new_part->current_step = NULL;
        new_part->next_part = NULL;

        switch(v) {
            case 'x':
                if (o == '<') {
                    if (head->x_max >= n && head->x_min < n) {head->x_max = n-1; head->current_step = nt;new_part->x_min = n; new_part->current_step = nf;head = add(head, new_part);}
                    else if (head->x_max < n) head->current_step = nt;
                    else head->current_step = nf;
                } else if (o == '>') {
                    if (head->x_max > n && head->x_min <= n) {head->x_max = n; head->current_step = nf;new_part->x_min = n+1; new_part->current_step = nt;head = add(head, new_part);}
                    else if (head->x_max <= n) head->current_step = nf;
                    else head->current_step = nt;
                }
                break;
            case 'm':
                if (o == '<') {
                    if (head->m_max >= n && head->m_min < n) {head->m_max = n-1; head->current_step = nt;new_part->m_min = n; new_part->current_step = nf;head = add(head, new_part);}
                    else if (head->m_max < n) head->current_step = nt;
                    else head->current_step = nf;
                } else if (o == '>') {
                    if (head->m_max > n && head->m_min <= n) {head->m_max = n; head->current_step = nf;new_part->m_min = n+1; new_part->current_step = nt;head = add(head, new_part);}
                    else if (head->m_max <= n) head->current_step = nf;
                    else head->current_step = nt;
                }
                break;
            case 'a':
                if (o == '<') {
                    if (head->a_max >= n && head->a_min < n) {head->a_max = n-1; head->current_step = nt;new_part->a_min = n; new_part->current_step = nf;head = add(head, new_part);}
                    else if (head->a_max < n) head->current_step = nt;
                    else head->current_step = nf;
                } else if (o == '>') {
                    if (head->a_max > n && head->a_min <= n) {head->a_max = n; head->current_step = nf;new_part->a_min = n+1; new_part->current_step = nt;head = add(head, new_part);}
                    else if (head->a_max <= n) head->current_step = nf;
                    else head->current_step = nt;
                }
                break;
            case 's':
                if (o == '<') {
                    if (head->s_max >= n && head->s_min < n) {head->s_max = n-1;head->current_step = nt;new_part->s_min = n;new_part->current_step = nf;head = add(head, new_part);}
                    else if (head->s_max < n) head->current_step = nt;
                    else head->current_step = nf;
                } else if (o == '>') {
                    if (head->s_max > n && head->s_min <= n) {head->s_max = n;head->current_step = nf;new_part->s_min = n+1;new_part->current_step = nt;head = add(head, new_part);}
                    else if (head->s_max <= n) head->current_step = nf;
                    else head->current_step = nt;
                }
                break;

        }

        while (head && (strcmp(head->current_step->name, "A") == 0 || strcmp(head->current_step->name, "R") == 0)) {
            //print_part_chain(head);
            if (strcmp(head->current_step->name, "A") == 0) {
                res += ((head->x_max - head->x_min + 1) * (head->m_max - head->m_min + 1) * (head->a_max - head->a_min + 1) * (head->s_max - head->s_min + 1));
            }
            head = head->next_part;
        }
    }

    printf("%lld\n", res);
}