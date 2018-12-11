#!/usr/bin/env python3

import os
import sys

SERIAL_NUMBER = 8979

# Return the top-left coordinates of the 3x3 square with the largest power.
def coordinates_max_power(grid):
    max_power   = -10**9
    best_square = (-1, -1)
    for x in range(1, 299):
        for y in range(1, 299):
            s = grid[x-1][y-1] + grid[x][y-1] + grid[x+1][y-1] +\
                grid[x-1][y]   + grid[x][y]   + grid[x+1][y]   +\
                grid[x-1][y-1] + grid[x][y+1] + grid[x+1][y+1]
            if s > max_power:
                max_power = s
                best_square = (x, y)

    return "{},{}".format(*best_square)

# A 300x300 grid represents the power level of fuel cells. Each cell has a value
# that depends on its x,y coordinates and the serial number (the file input).
#
# Part 1: find the top-left coordinates of the 3 x 3 square that has the largest
#         total power (sum of the fuel power of its 9 cells).
# Part 2: find the top-left coordinates and the size k of the k x k square that
#         has the largest total power (sum of the fuel power of all its cells).
if __name__ == '__main__':
    if len(sys.argv) > 2:
        sys.exit("usage: ./day11.py [INPUT_FILE]")
    if len(sys.argv) == 2:
        filename = sys.argv[1]
        if not os.path.exists(filename):
            sys.exit("error: {} does not exist.".format(filename))
        SERIAL_NUMBER = int(open(filename).read())

    # init cells with fuel power formula
    grid = [ [ ((((X+10)*Y + SERIAL_NUMBER) * (X+10)) // 100) % 10 - 5 \
               for Y in range(1, 301) ] for X in range(1, 301) ]
    print("PART ONE:", coordinates_max_power(grid))
