#!/usr/bin/env python3

import os
import sys
from copy import deepcopy

SERIAL_NUMBER = 8979

# Return the top-left coordinates and the size of the square with the largest
# total power (the sum of fuel power of all its cells). If square_size is given,
# only look at squares of size square_size x square_size.
def coordinates_max_power(grid, square_size=None):
    # build the summed-area table `s_grid` of `grid`
    L = len(grid)
    s_grid = deepcopy(grid) # nested lists, need deepcopy to have a full copy
    for x in range(1, L):
        s_grid[x][0] += s_grid[x-1][0] # cumulative sum of first column
        s_grid[0][x] += s_grid[0][x-1] # cumulative sum of first row
    for x in range(1, L):
        for y in range(1, L):
            # each cell is the sum of all the values above and on the left
            s_grid[x][y] += s_grid[x][y-1] + s_grid[x-1][y] - s_grid[x-1][y-1]

    max_power   = -10**9
    best_square = (-1, -1)
    best_size   = -1
    sizes       = [square_size] if square_size else range(1, L+1)
    for size in sizes:
        for x in range(1, 300-size):
            for y in range(1, 300-size):
                # top-left is (x, y); bottom-right is (x + size-1, y + size-1)
                s = s_grid[x + size-1][y + size-1] \
                  - s_grid[x-1][y + size-1]        \
                  - s_grid[x + size-1][y-1]        \
                  + s_grid[x-1][y-1]
                if s > max_power:
                    max_power   = s
                    best_square = (x+1, y+1) # problem says grid is 1-indexed
                    best_size   = size

    if square_size:
        return "{},{}".format(*best_square)
    else:
        return "{},{},{}".format(*best_square, best_size)

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
    print("PART ONE:", coordinates_max_power(grid, 3))
    print("PART TWO:", coordinates_max_power(grid))
