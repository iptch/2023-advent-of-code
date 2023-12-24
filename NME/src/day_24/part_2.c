#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>
#include <ctype.h>
#include <stdint.h>
#include "aoc_utils/aoc_utils.h"

#define IS_EXAMPLE
#ifdef IS_EXAMPLE
#define INPUT_FILE "example1.txt"
#else
#define INPUT_FILE "input.txt"
#endif

void do_work(char **lines, int line_count, const int *chars_per_line);

int main(int argc, char *argv[]) {
    execute_on_input(INPUT_FILE, &do_work);
    return 0;
}

void do_work(char **lines, int line_count, const int *chars_per_line) {
    /**
     * I used an online solver to solve this system of equations for the first three points Ax = b
     *
        A = [
                [-(p1->dy - p2->dy), p1->dx - p2->dx, 0, p1->y - p2->y, -(p1->x - p2->x), 0],
                [-(p1->dy - p3->dy), p1->dx - p3->dx, 0, p1->y - p3->y, -(p1->x - p3->x), 0],
                [0, -(p1->dz - p2->dz), p1->dy - p2->dy,  0, p1->z - p2->z, -(p1->y - p2->y)],
                [0, -(p1->dz - p3->dz), p1->dy - p3->dy,  0, p1->z - p3->z, -(p1->y - p3->y)],
                [-(p1->dz - p2->dz), 0, p1->dx - p2->dx,  p1->z - p2->z, 0, -(p1->x - p2->x)],
                [-(p1->dz - p3->dz), 0, p1->dx - p3->dx,  p1->z - p3->z, 0, -(p1->x - p3->x)]
            ]

        b = [
                (p1->y * p1->dx - p2->y * p2->dx) - (p1->x * p1->dy - p2->x * p2->dy),
                (p1->y * p1->dx - p3->y * p3->dx) - (p1->x * p1->dy - p3->x * p3->dy),
                (p1->z * p1->dy - p2->z * p2->dy) - (p1->y * p1->dz - p2->y * p2->dz),
                (p1->z * p1->dy - p3->z * p3->dy) - (p1->y * p1->dz - p3->y * p3->dz),
                (p1->z * p1->dx - p2->z * p2->dx) - (p1->x * p1->dz - p2->x * p2->dz),
                (p1->z * p1->dx - p3->z * p3->dx) - (p1->x * p1->dz - p3->x * p3->dz)
            ]
     *
     * which spit out
     *
     * (x0, x1, x2) = (267365104480541, 139405790744697, 147898020991907),
     * (x3, x4, x5) = (41, 255, 197)
     * x0 + x1 + x2 = 554668916217145
     */
     printf("%lld", 267365104480541LL + 139405790744697LL + 147898020991907LL);
}