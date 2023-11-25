#ifndef INC_2023_ADVENT_OF_CODE_AOC_UTILS_H
#define INC_2023_ADVENT_OF_CODE_AOC_UTILS_H

void execute_on_input(const char *filename, void (*do_work)(char **lines, int line_count, const int *chars_per_line));
int min(int a, int b);
int max(int a, int b);

#endif //INC_2023_ADVENT_OF_CODE_AOC_UTILS_H

