#!/usr/bin/env python3

import os
import sys

# Read the file, return the initial pots state and the list of spead conditions.
def parse_input(filename):
    with open(filename) as f:
        # first line is like: initial state: #..#.#..##......###...###
        pots = f.readline().split(":")[1].strip()
        f.readline() # skip blank line
        conditions = []
        for line in f: # rest of file is composed of 1 condition per line
            line = line.strip().split(" => ")
            conditions.append([line[0], line[1]])

    return pots, conditions

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
    print(pots)
    print(len(pots))
    print(conditions)
