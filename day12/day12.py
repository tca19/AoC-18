#!/usr/bin/env python3

import os
import sys

from collections import defaultdict

# Read the file, return the initial state and the list of spread conditions.
def parse_input(filename):
    with open(filename) as f:
        # first line is like: initial state: #..#.#..##......###...###
        pots = f.readline().split(":")[1].strip()
        f.readline() # skip blank line
        conditions = defaultdict(lambda: ".") # use a dict for fast lookup
        for line in f: # rest of file is composed of 1 condition per line
            line = line.strip().split(" => ")
            conditions[line[0]] = line[1]
    return pots, conditions

# Update the plant positions in pots given the conditions. Return the new pots.
def update(pots, conditions):
    new_pots = ["." for _ in range(len(pots))] # strings are immutable, use list
    for pos in range(2, len(pots)-2):
        new_pots[pos] = conditions[pots[pos-2:pos+3]]
    return "".join(new_pots)

# Return the sum of indexes having a plant (a plant is a '#' in `pots`)
def sum_plants(pots, extension_size):
    s = 0
    # `pots` has been extended on both left and right, but index 0 is still at
    # the position of the first original pot. So if original pots has a length
    # of L and the extension size is K, indexes are:
    # -K  -K+1 .... 0 1 ...L-1 L .... L+K-1
    for i in range(len(pots)):
        if pots[i] == '#':
            s += i - extension_size
    return s

# Return the sum of indexes having a plant after N spread generations.
def sum_after_generations(pots, conditions, N):
    EXTENSION = 1000 # add extended empty space around pots
    pots = "." * EXTENSION + pots + "." * EXTENSION
    seen_patterns = dict()
    for iter in range(N):
        pots = update(pots, conditions)
        pots_stripped = pots.strip(".") # remove empty space on both side
        if pots_stripped in seen_patterns:
            prev_iter, prev_val = seen_patterns[pots_stripped]
            diff_val = sum_plants(pots, EXTENSION) - prev_val
            diff_iter = iter - prev_iter

            # this means that the sum has increased by `diff_val` in `diff_iter`
            # generations. Skip a lot of `diff_iter` generations and add the
            # `diff_val` value instead of simulating the plant spreading. Only
            # simulate the last remaining generations.
            left_iter = N - iter
            total = prev_val + diff_val * (left_iter // diff_iter)
            if (left_iter % diff_iter > 0):
                for _ in range(left_iter % diff_iter):
                    pots = update(pots, conditions)
                total += sum_plants(pots, EXTENSION)
            return total
        else:
            seen_patterns[pots_stripped] = (iter, sum_plants(pots, EXTENSION))
    return sum_plants(pots, EXTENSION)

# Input file is the initial state of the pots representing where the plants are
# placed (like "#..#.#..##......###...###", a '#' is a plant) and the list of
# conditions for plant spreading (like "..#.. => #").
#
# Part 1: find the sum of indexes where there is a plant after 20 generations.
# Part 2: find the sum of indexes where there is a plant after 50 billion
#         generations.
if __name__ == '__main__':
    if len(sys.argv) != 2:
        sys.exit("usage: ./day12.py INPUT_FILE")
    filename = sys.argv[1]
    if not os.path.exists(filename):
         sys.exit("error: {} does not exist.".format(filename))
    pots, conditions = parse_input(filename)
    print("PART ONE:", sum_after_generations(pots, conditions, 20))
    print("PART TWO:", sum_after_generations(pots, conditions, 50000000000))
