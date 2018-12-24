#!/usr/bin/env python3

import os
import sys

N_RECIPES = 503761

# Return the scores of the m recipes created after N recipes have been made.
def scores_after(N, m):
    scores = "37"
    pos_elf1 = 0
    pos_elf2 = 1
    while len(scores) < N+m:
        r1 = int(scores[pos_elf1])
        r2 = int(scores[pos_elf2])
        scores += str(r1 + r2)
        pos_elf1 += r1 + 1
        if pos_elf1 >= len(scores):
            pos_elf1 %= len(scores)
        pos_elf2 += r2 + 1
        if pos_elf2 >= len(scores):
            pos_elf2 %= len(scores)
    return scores[-m:]

# Two elves are making recipes. Starting with only two recipes which have the
# scores of 3 and 7, they create new recipes based on the already existing ones.
# Each new recipe has a score which is appended to the current list of scores.
# The input is a number (an integer) of recipes to make.
#
# Part 1: find the scores of the ten recipes made after the certain number of
#         recipes have been done.
# Part 2: create new recipes until there are contiguous scores forming the
#         input number. Find the index of the first contiguous value.
if __name__ == '__main__':
    if len(sys.argv) > 2:
        sys.exit("usage: ./day14.py [INPUT_FILE]")
    if len(sys.argv) == 2:
        filename = sys.argv[1]
        if not os.path.exists(filename):
            sys.exit("error: {} does not exist.".format(filename))
        N_RECIPES = int(open(filename).read())
    print("PART ONE:", scores_after(N_RECIPES, 10))
