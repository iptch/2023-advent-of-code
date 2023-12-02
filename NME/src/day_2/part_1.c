#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>
#include "aoc_utils/aoc_utils.h"

#define INPUT_FILE "input.txt"

void do_work(char **lines, int line_count, const int *chars_per_line);

int main(int argc, char *argv[]) {
    execute_on_input(INPUT_FILE, &do_work);
    return 0;
}

void do_work(char **lines, int line_count, const int *chars_per_line) {
    int res = 0;
    for (int i=0; i<line_count; i++) {
        bool valid = true;
        char copy[chars_per_line[i]+1];
        strcpy(copy, lines[i]);
        strtok(copy, ":");
        char *token = strtok(NULL, ";");
        while (token != NULL) {
            char round[strlen(token)+1];
            strcpy(round, token);
            char *end_str;
            char *color = strtok_r(round, ",", &end_str);
            while (color != NULL)
            {
                char *color_start;
                if ((color_start = strstr(color, "red"))) {
                    color_start[-1] = '\0';
                    int amount = atoi(color);
                    if (amount > 12) {
                        valid = false;
                    }
                }
                if ((color_start = strstr(color, "green"))) {
                    color_start[-1] = '\0';
                    int amount = atoi(color);
                    if (amount > 13) {
                        valid = false;
                    }
                }
                if ((color_start = strstr(color, "blue"))) {
                    color_start[-1] = '\0';
                    int amount = atoi(color);
                    if (amount > 14) {
                        valid = false;
                    }                }
                color = strtok_r(NULL, ",", &end_str);
            }
            token = strtok(NULL, ";");
        }
        if (valid) {
            res += i+1;
        }
    }
    printf("%d", res);
}