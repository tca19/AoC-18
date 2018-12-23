#!/usr/bin/env python3

import os
import sys

class Cart:
    def __init__(self, x, y, dir):
        self.x = x
        self.y = y
        self.dir = dir
        self.choice = 0 # 0 for left, 1 for straight, 2 for right

    # move the cart in the direction `dir`. Find the new direction for next move
    def move(self, grid):
        # move towards the right
        if self.dir == "E":
            self.y += 1
            if grid[self.x][self.y] == "\\":
                self.dir = "S"
            elif grid[self.x][self.y] == "/":
                self.dir = "N"
            elif grid[self.x][self.y] == "+":
                # coming from left: turning left = North; going straight = East
                # and turning right => South
                self.dir = "NES"[self.choice]
                self.choice = (self.choice + 1) % 3

        # move towards the left
        elif self.dir == "W":
            self.y -= 1
            if grid[self.x][self.y] == "\\":
                self.dir = "N"
            elif grid[self.x][self.y] == "/":
                self.dir = "S"
            elif grid[self.x][self.y] == "+":
                # coming from right: turning left = South; going straight = West
                # and turning right => North
                self.dir = "SWN"[self.choice]
                self.choice = (self.choice + 1) % 3

        # move towards the top
        elif self.dir == "N":
            self.x -= 1
            if grid[self.x][self.y] == "\\":
                self.dir = "W"
            elif grid[self.x][self.y] == "/":
                self.dir = "E"
            elif grid[self.x][self.y] == "+":
                # coming from bottom: turning left = West; going straight =
                # North and turning right => East
                self.dir = "WNE"[self.choice]
                self.choice = (self.choice + 1) % 3

        # move towards the bottom
        elif self.dir == "S":
            self.x += 1
            if grid[self.x][self.y] == "\\":
                self.dir = "E"
            elif grid[self.x][self.y] == "/":
                self.dir = "W"
            elif grid[self.x][self.y] == "+":
                # coming from top: turning left = East; going straight = South
                # and turning right => West
                self.dir = "ESW"[self.choice]
                self.choice = (self.choice + 1) % 3

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
