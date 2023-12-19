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

struct part {
    int x;
    int m;
    int a;
    int s;
};

struct step {
    char *name;
    char condition_variable;
    char condition_operation;
    int condition_constant;
    struct step *next_if_true;
    struct step *next_if_false;
};

void do_work(char **lines, int line_count, const int *chars_per_line);
struct step *find(struct step **steps, const char *name, size_t n);

int main(int argc, char *argv[]) {
    execute_on_input(INPUT_FILE, &do_work);
    return 0;
}

struct step *next(struct step *s, struct part *p) {
    bool eval_result = true;
    switch(s->condition_variable) {
        case 'x': eval_result = (s->condition_operation == '<' && p->x < s->condition_constant) || (s->condition_operation == '>' && p->x > s->condition_constant); break;
        case 'm': eval_result = (s->condition_operation == '<' && p->m < s->condition_constant) || (s->condition_operation == '>' && p->m > s->condition_constant); break;
        case 'a': eval_result = (s->condition_operation == '<' && p->a < s->condition_constant) || (s->condition_operation == '>' && p->a > s->condition_constant); break;
        case 's': eval_result = (s->condition_operation == '<' && p->s < s->condition_constant) || (s->condition_operation == '>' && p->s > s->condition_constant); break;
    }
    return eval_result ? s->next_if_true : s->next_if_false;
}

struct step *find(struct step **steps, const char *name, size_t n) {
    for (int i=0; i<n; i++) {
        if (!strcmp(steps[i]->name, name)) return steps[i];
    }
    return NULL;
}

void do_work(char **lines, int line_count, const int *chars_per_line) {
    struct step **steps = (struct step **)malloc(sizeof(struct step *) * line_count);
    struct part **parts = (struct part **)malloc(sizeof(struct part *) * line_count);
    int step_idx = 2;
    int part_idx = 0;

    steps[0] = (struct step *)calloc(1, sizeof(struct step));
    steps[0]->name = "A";

    steps[1] = (struct step *)calloc(1, sizeof(struct step));
    steps[1]->name = "R";


    bool is_steps = true;
    for (int i=0; i<line_count; i++) {
        if (chars_per_line[i] == 0) {
            is_steps = false;
            continue;
        }

        if (is_steps) {
            char *rest = strstr(lines[i], "{");
            size_t l = rest - lines[i];
            char *name = (char *)malloc(sizeof(char) * (l + 1));
            strncpy(name, rest - l, l);
            name[l] = '\0';
            struct step *s = (struct step *)calloc(1, sizeof(struct step));
            s->name = name;
            steps[step_idx++] = s;
        } else {
            char *x = strtok(lines[i], ",") + 3;
            char *m = strtok(NULL, ",") + 2;
            char *a = strtok(NULL, ",") + 2;
            char *s = strtok(NULL, ",") + 2;
            s[strlen(s) - 1] = '\0';

            struct part *p = (struct part *)malloc(sizeof(struct part));
            p->x = atoi(x);
            p->m = atoi(m);
            p->a = atoi(a);
            p->s = atoi(s);
            parts[part_idx++] = p;
        }
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

                if (previous) {
                    previous->next_if_false = current;
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
                free(current);
            }
            transition = strtok(NULL, ",");
        }
    }

    struct step *start = find(steps, "in", step_idx);
    int res = 0;
    for (int i=0; i<part_idx; i++) {
        struct step *current = start;
        struct part *p = parts[i];
        while (strcmp(current->name, "A") != 0 && strcmp(current->name, "R") != 0) {
            current = next(current, p);
        }
        if (strcmp(current->name, "A") == 0) {
            res += p->x + p->a + p->m + p->s;
        }
    }
    printf("%d\n", res);
}