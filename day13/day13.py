#!/usr/bin/env python3

import os
import sys

class Cart:
    def __init__(self, x, y, dir):
        self.x = x
        self.y = y
        self.dir = dir

# Read the rail tracks paths and carts position from filename. Return the tracks
# as a 2D grid and the list of carts.
def read_tracks_and_carts(filename):
    data  = open(filename).read().splitlines()
    L     = max(len(line) for line in data)
    carts = []
    grid = []
    for i, line in enumerate(data):
        s = "" # strings are immutable, create a new one to modify line
        for j, c in enumerate(line):
            if c == ">": # direction = East
                carts.append(Cart(i, j, "E"))
                s += "-"
            elif c == "<": # direction = West
                carts.append(Cart(i, j, "W"))
                s += "-"
            elif c == "^": # direction = North
                carts.append(Cart(i, j, "N"))
                s += "|"
            elif c == "v": # direction = South
                carts.append(Cart(i, j, "S"))
                s += "|"
            else:
                s += c
        grid.append(s)
    return grid, carts

# Input file is a representation of rail tracks and carts. Tracks are either
# "-", "|", "/", "\" or "+". Carts are either ">", "<", "^" or "v", indicating
# their position and current direction. Below is an example of rail tracks.
#
#                            /->-\
#                            |   |  /----\
#                            | /-+--+-\  |
#                            | | |  | v  |
#                            \-+-/  \-+--/
#                              \------/
#
# Part 1: find the position of the first collision between two carts.
# Part 2: find the position of the last cart after all the others have crashed.
if __name__ == '__main__':
    if len(sys.argv) != 2:
        sys.exit("usage: ./day13.py INPUT_FILE")
    filename = sys.argv[1]
    if not os.path.exists(filename):
         sys.exit("error: {} does not exist.".format(filename))
    grid, carts = read_tracks_and_carts(filename)
    print("\n".join(grid))
    for x in carts:
        print(x.x, x.y, x.dir)
