#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>
#include <ctype.h>
#include <stdint.h>
#include "aoc_utils/aoc_utils.h"

//#define IS_EXAMPLE
#ifdef IS_EXAMPLE
#define INPUT_FILE "example2.txt"
#else
#define INPUT_FILE "input.txt"
#endif

#define BUTTON_MODULE_NAME "button"
#define BROADCASTER_MODULE_NAME "broadcaster"
#define BUTTON_PUSHES 1000

enum type {FLIP_FLOP, CONJUNCTION, BROADCASTER, BUTTON};
struct module {
    size_t idx;
    char *name;
    enum type type;
    size_t destinations_count;
    struct module **destinations;
    bool on;
    size_t inputs_count;
    bool *inputs_on;
    struct module **inputs;
};
struct pulse {
    struct module *start;
    struct module *end;
    bool high;
    struct pulse *next;
};

void do_work(char **lines, int line_count, const int *chars_per_line);
struct module *find(struct module **modules, size_t modules_count, char *name);
void print_pulse(struct pulse *p);
void push_button(struct module **modules, int64_t modules_count, int64_t *low, int64_t *high);

int main(int argc, char *argv[]) {
    execute_on_input(INPUT_FILE, &do_work);
    return 0;
}

void print_pulse(struct pulse *p) {
    printf("%s -%s-> %s\n", p->start->name, p->high ? "high" : "low", p->end->name);
}

struct module *find(struct module **modules, size_t modules_count, char *name) {
    for (size_t i=0; i<modules_count; i++) {
        if (!strcmp(name, modules[i]->name)) return modules[i];
    }
    return NULL;
}

void push_button(struct module **modules, int64_t modules_count, int64_t *low, int64_t *high) {
    struct pulse *pulses = (struct pulse *) calloc(1, sizeof(struct pulse));
    pulses->start = modules[modules_count - 1];
    pulses->end = find(modules, modules_count, BROADCASTER_MODULE_NAME);
    pulses->high = false;
    pulses->next = NULL;

    struct pulse *last_pulse = pulses;

    while (pulses) {
        if (pulses->high) (*high)++;
        else (*low)++;

        //print_pulse(pulses);
        struct pulse *current = pulses;
        if (current->end->type == FLIP_FLOP && current->high) {
            pulses = current->next;
            continue;
        }

        bool pulse_to_send = true;
        if (current->end->type == FLIP_FLOP) {
            current->end->on = !current->end->on;
            pulse_to_send = current->end->on;
        }

        if (current->end->type == CONJUNCTION) {
            for (size_t i = 0; i < current->end->inputs_count; i++) {
                if (current->end->inputs[i]->idx == current->start->idx) {
                    current->end->inputs_on[i] = current->high;
                }
                pulse_to_send &= current->end->inputs_on[i];
            }
            pulse_to_send = !pulse_to_send;
        }

        if (current->end->type == BROADCASTER) {
            pulse_to_send = false;
        }

        for (size_t i = 0; i < current->end->destinations_count; i++) {
            struct pulse *new_pulse = (struct pulse *) calloc(1, sizeof(struct pulse));
            new_pulse->start = current->end;
            new_pulse->end = current->end->destinations[i];
            new_pulse->high = pulse_to_send;
            new_pulse->next = NULL;
            last_pulse->next = new_pulse;
            last_pulse = new_pulse;
        }

        pulses = pulses->next;
    }
}

void do_work(char **lines, int line_count, const int *chars_per_line) {
    struct module **modules = (struct module **)calloc(line_count + 1, sizeof(struct module *));

    for (size_t i=0; i<line_count; i++) {
       modules[i] = (struct module *)calloc(1, sizeof(struct module));
       modules[i]->idx = i;
       size_t name_size = strstr(lines[i], " ") - lines[i];
       modules[i]->name = (char *)calloc(name_size + 1, sizeof(char));
       strncpy(modules[i]->name, lines[i], name_size);
       modules[i]->name[name_size] = '\0';
       size_t destinations_count = 1;
       char *line_start = lines[i];
       while(*lines[i]) if (*lines[i]++ == ',') ++destinations_count;
       lines[i] = line_start;
       modules[i]->destinations_count = destinations_count;
       modules[i]->destinations = (struct module **)calloc(destinations_count, sizeof(struct module *));
       switch (lines[i][0]) {
           case '%':
               modules[i]->type = FLIP_FLOP;
               modules[i]->name++;
               modules[i]->on = false;
               break;
           case '&':
               modules[i]->type = CONJUNCTION;
               modules[i]->name++;
               break;
           default:
               modules[i]->type = BROADCASTER;
               modules[line_count] = (struct module *)calloc(1, sizeof(struct module));
               modules[line_count]->name = BUTTON_MODULE_NAME;
               modules[line_count]->type = BUTTON;
               modules[line_count]->destinations_count = 1;
               modules[line_count]->destinations = (struct module **)calloc(1, sizeof(struct module *));
               modules[line_count]->destinations[0] = modules[i];
               break;
       }
    }

    for (size_t i=0; i<line_count; i++) {
        strtok(lines[i], " ");
        strtok(NULL, " ");
        char *destination_name = strtok(NULL, ",");
        size_t destination_idx = 0;
        while (destination_name) {
            struct module *destination = find(modules, line_count+1, destination_name);
            if (!destination) { // only happens if a module does not have destinations
                destination = (struct module *)calloc(1, sizeof(struct module));
                destination->name = destination_name;
            }
            modules[i]->destinations[destination_idx++] = destination;
            if (destination->type == CONJUNCTION) destination->inputs_count++;
            destination_name = strtok(NULL, ",");
            if (destination_name) destination_name++;
        }
    }

    for (size_t i=0; i<line_count; i++) {
        if (modules[i]->type == CONJUNCTION) {
            modules[i]->inputs_on = (bool *)calloc(modules[i]->inputs_count, sizeof(bool));
            modules[i]->inputs = (struct module **)calloc(modules[i]->inputs_count, sizeof(struct module *));
        }
    }

    size_t *inputs_idx = (size_t *)calloc(line_count, sizeof(size_t));
    for (size_t i=0; i<line_count; i++) {
        for (size_t j=0; j<modules[i]->destinations_count; j++) {
            if (modules[i]->destinations[j]->type == CONJUNCTION) {
                size_t destination_idx = modules[i]->destinations[j]->idx;
                modules[i]->destinations[j]->inputs[inputs_idx[destination_idx]++] = modules[i];
            }
        }
    }

    int64_t high = 0; int64_t low = 0;
    for (size_t y=0; y<BUTTON_PUSHES; y++) {
        push_button(modules, line_count+1, &low, &high);
    }
    printf("%lld\n", high * low);

    free(modules);
}