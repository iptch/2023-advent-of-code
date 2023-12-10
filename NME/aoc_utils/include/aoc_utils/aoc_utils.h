#ifndef INC_2023_ADVENT_OF_CODE_AOC_UTILS_H
#define INC_2023_ADVENT_OF_CODE_AOC_UTILS_H

struct queue {
    void *item;
    struct queue *next;
};

void execute_on_input(const char *filename, void (*do_work)(char **lines, int line_count, const int *chars_per_line));
int min(int a, int b);
int max(int a, int b);
long long minll(long long a, long long b);
long long maxll(long long a, long long b);
struct queue *queue_init(void *item);
void queue_add(struct queue *q, void *item);
struct queue *queue_pop(struct queue *q, void **item_ptr);

#endif //INC_2023_ADVENT_OF_CODE_AOC_UTILS_H

