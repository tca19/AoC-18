
#!/usr/bin/env python3

import os
import sys

# Input file is a list of 4-dimensional points, one per line. Two points having
# a Manhattan distance less than 3 form a constellation. If a point has a
# Manhattan distance less than 3 to any point of a constellation, it joins this
# constellation.
#
# Part 1: find the number of distinct constellation formed by the points
# Part 2: solve all the previous problems
if __name__ == '__main__':
    if len(sys.argv) != 2:
        sys.exit("usage: ./day25.py INPUT_FILE")
    filename = sys.argv[1]
    if not os.path.exists(filename):
        sys.exit("error: {} does not exist.".format(filename))
