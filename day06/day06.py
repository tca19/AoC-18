#!/usr/bin/env python3

import os
import sys

# Input file is a list of point coordinates (x, y), one per line, representing
# places in an infinite grid.
#
# Part 1: find the size of the largest area of points having the same closest
#         place (infinite area do not count).
# Part 2: find the size of the area of points having a total Manhattan distance
#         to places less than 10000 (the total distance is the sum of Manhattan
#         distance to all places coordinates).
if __name__ == '__main__':
    if len(sys.argv) != 2:
        sys.exit("usage: ./day06.py INPUT_FILE")
    filename = sys.argv[1]
    if not os.path.exists(filename):
         sys.exit("error: {} does not exist.".format(filename))
    places = [list(map(int, line.split(',')))
              for line in open(filename).read().splitlines()]
