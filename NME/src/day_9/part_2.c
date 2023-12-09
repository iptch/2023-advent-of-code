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

void do_work(char **lines, int line_count, const int *chars_per_line);
bool generate_subsequence(const int *in, int* out, size_t n);

int main(int argc, char *argv[]) {
    execute_on_input(INPUT_FILE, &do_work);
    return 0;
}

bool generate_subsequence(const int *in, int* out, size_t n) {
    bool all_zeroes = true;
    for (int i=1; i<n; i++) {
        int a = in[i] - in[i-1];
        out[i-1] = a;
        if (a != 0) {
            all_zeroes = false;
        }
    }
    return all_zeroes;
}


void do_work(char **lines, int line_count, const int *chars_per_line) {
    long long res = 0;

    for (int i=0; i<line_count; i++) {
        int num_nums = 1;
        for (int j=0; j<chars_per_line[i]; j++) {
            if (lines[i][j] == ' ') {
                num_nums++;
            }
        }

        int *nums = (int *)malloc(sizeof(int) * num_nums);
        char *ptr = strtok(lines[i], " ");
        int j = 0;
        while (ptr) {
            nums[j++] = atoi(ptr);
            ptr = strtok(NULL, " ");
        }

        bool all_zeroes = false;
        int level = 1;
        long long next = nums[0];
        while (!all_zeroes) {
            int *new_nums = (int *)malloc(sizeof(int) * (num_nums - level));
            all_zeroes = generate_subsequence(nums, new_nums, num_nums - level + 1);
            if (level % 2 == 0) {
                next += new_nums[0];
            } else {
                next -= new_nums[0];
            }
            free(nums);
            nums = new_nums;
            level++;
        }
        free(nums);
        res += next;
    }

    printf("%lld\n", res);
}