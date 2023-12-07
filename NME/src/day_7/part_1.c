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

struct hand {
    int a;
    int b;
    int c;
    int d;
    int e;
    long long bid;
};

enum HandType {
    HIGH_CARD,
    PAIR,
    TWO_PAIR,
    THREE_OF_KIND,
    FULL_HOUSE,
    FOUR_OF_KIND,
    FIVE_OF_KIND
};

void counts(const struct hand *h, int c[5]);
enum HandType get_hand_type(const struct hand *h);
int map_card_to_num(char c);
int compare_hands(const void *x, const void *y);
int compare_ints(const void * a, const void * b);
void do_work(char **lines, int line_count, const int *chars_per_line);

int main(int argc, char *argv[]) {
    execute_on_input(INPUT_FILE, &do_work);
    return 0;
}

void counts(const struct hand *h, int *c) {
    int n[13] = {0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0};
    n[h->a]++;
    n[h->b]++;
    n[h->c]++;
    n[h->d]++;
    n[h->e]++;
    qsort(n, 13, sizeof(int), compare_ints);
    c[0] = n[0];
    c[1] = n[1];
    c[2] = n[2];
    c[3] = n[3];
    c[4] = n[4];
}


enum HandType get_hand_type(const struct hand *h) {
    int n[5] = {0, 0, 0, 0, 0};
    counts(h, n);
    if (n[0] == 5) {
        return FIVE_OF_KIND;
    }
    if (n[0] == 4) {
        return FOUR_OF_KIND;
    }
    if (n[0] == 3 && n[1] == 2) {
        return FULL_HOUSE;
    }
    if (n[0] == 3) {
        return THREE_OF_KIND;
    }
    if (n[0] == 2 && n[1] == 2) {
        return TWO_PAIR;
    }
    if (n[0] == 2) {
        return PAIR;
    }
    return HIGH_CARD;
}

int compare_ints(const void * a, const void * b) {
    return ( *(int*)b - *(int*)a );
}

int compare_hands(const void *x, const void *y) {
    struct hand *h1 = (struct hand *)x;
    struct hand *h2 = (struct hand *)y;

    enum HandType t1 = get_hand_type(h1);
    enum HandType t2 = get_hand_type(h2);
    if (t1 != t2) {
        return (int)t1 - (int)t2;
    }

    if (h1->a != h2->a) {
        return h1->a - h2->a;
    }

    if (h1->b != h2->b) {
        return h1->b - h2->b;
    }

    if (h1->c != h2->c) {
        return h1->c - h2->c;
    }

    if (h1->d != h2->d) {
        return h1->d - h2->d;
    }

    if (h1->e != h2->e) {
        return h1->e - h2->e;
    }
    return 0;
}

int map_card_to_num(char c) {
    if (c == 'A') return 12;
    if (c == 'K') return 11;
    if (c == 'Q') return 10;
    if (c == 'J') return 9;
    if (c == 'T') return 8;
    if (c == '9') return 7;
    if (c == '8') return 6;
    if (c == '7') return 5;
    if (c == '6') return 4;
    if (c == '5') return 3;
    if (c == '4') return 2;
    if (c == '3') return 1;
    if (c == '2') return 0;
    return -1;
}


void do_work(char **lines, int line_count, const int *chars_per_line) {
    struct hand *hands = (struct hand *)malloc(sizeof(struct hand) * line_count);
    for (int i=0; i<line_count; i++) {
        hands[i].a = map_card_to_num(lines[i][0]);
        hands[i].b = map_card_to_num(lines[i][1]);
        hands[i].c = map_card_to_num(lines[i][2]);
        hands[i].d = map_card_to_num(lines[i][3]);
        hands[i].e = map_card_to_num(lines[i][4]);
        hands[i].bid = atoll(lines[i]+6);
    }

    qsort(hands, line_count, sizeof(struct hand), compare_hands);

    long long res = 0;
    for (int i=0; i<line_count; i++) {
        res += (i+1) * hands[i].bid;
    }
    printf("%lld", res);
    free(hands);
}