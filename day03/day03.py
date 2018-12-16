#!/usr/bin/env python3

import os
import re
import sys

# whole piece of fabric is at least 1000 inches on each side
fabric = [ [0 for _ in range(1000)] for _ in range(1000) ]

# Extract and return info of each claim from filename.
def parse_file(filename):
    # Claims are like "#5 @ 178,10: 5x3". Use a regex to extract all numbers.
    extractor = re.compile("\d+") # assume there is no negative values
    return [[int(n) for n in extractor.findall(l)]
            for l in open(filename).read().splitlines()]

# Return the total overlapping claims area size (in square inches).
def size_overlap(claims):
    total_overlap = 0
    for id, x, y, width, height in claims:
        for i in range(x, x+width):
            for j in range(y, y+height):
                if fabric[i][j] == 1: # this square inch has already been used
                    total_overlap += 1
                fabric[i][j] += 1     # mark it as (once again) used
    return total_overlap

# Return the id of the only claim not overlapped by any other one.
def id_not_overlap(claims):
    # For each claim, verify that all its area has been wanted only once. If
    # there is a part which has been wanted at least 2 times, then it does
    # overlap with another claim.
    for id, x, y, width, height in claims:
        does_overlap = False
        for i in range(x, x+width):
            for j in range(y, y+height):
                if fabric[i][j] > 1:
                    does_overlap = True
        if not does_overlap:
            return id

# Input file is a list of claims, one per line, like "#1 @ 1,3: 4x4" having:
#   - an id (1)
#   - a starting position from left edge (1, in inches)
#   - a starting position from top edge (3, in inches)
#   - a width (4, in inches)
#   - an height (4, in inches)
# Each claim represents the area of a large square piece of fabric (of size
# 1000x1000) wanted by an elf (each elf has one claim).
#
# Part 1: some claims overlap. Find the number of square inches of fabric that
#         are within two or more claims.
# Part 2: find the ID of the claim that doesn't overlap.
if __name__ == '__main__':
    if len(sys.argv) != 2:
        sys.exit("usage: ./day03.py INPUT_FILE")
    filename = sys.argv[1]
    if not os.path.exists(filename):
         sys.exit("error: {} does not exist.".format(filename))
    claims = parse_file(filename)
    print("PART ONE:", size_overlap(claims))
    print("PART TWO:", id_not_overlap(claims))
