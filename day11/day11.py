#!/usr/bin/env python3

import os
import sys

SERIAL_NUMBER = 8979

# A 300x300 grid represents the power level of fuel cells. Each cell has a value
# that depends on its x,y coordinates and the serial number (the file input).
#
# Part 1: find the top-left coordinates of the 3 x 3 square that has the largest
#         total power (sum of the fuel power of its 9 cells).
# Part 2: find the top-left coordinattes and the size k of the k x k square that
#         has the largest total power (sum of the fuel power of all its cells).
if __name__ == '__main__':
    if len(sys.argv) > 2:
        sys.exit("usage: ./day11.py [INPUT_FILE]")
    if len(sys.argv) == 2:
        filename = sys.argv[1]
        if not os.path.exists(filename):
            sys.exit("error: {} does not exist.".format(filename))
        SERIAL_NUMBER = int(open(filename).read())
