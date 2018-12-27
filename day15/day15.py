#!/usr/bin/env python3

import os
import sys

grid = []
units = []

class Unit:
    def __init__(self, type, x, y):
        self.type   = type
        self.x      = x
        self.y      = y
        self.health = 200
        self.attack = 3

# Read the content of filename to get the unit positions and the map. Fill the
# global variables `grid` (2D list) and `units` (list of Unit instances).
def read_map(filename):
    with open(filename) as f:
        for i, line in enumerate(f):
            grid.append(line.strip())
            for j, c in enumerate(line):
                if c in "EG":
                    units.append(Unit(c, i, j))

# Print the grid. For each line, displays the existing units and their health.
def print_map():
    # assume that units are sorted by position (top to bottom, left to right)
    index = 0
    for row in grid:
        units_of_line = []
        for cell in row:
            print(cell, end="")
            if cell in "EG":
                units_of_line.append("{}({})".format(cell, units[index].health))
                index += 1
        print("  ", ", ".join(units_of_line))

# Input file is a map representing Goblins (G) and Elves (E). The Goblins and
# Elves take turns fighting. During its turn, each unit first move towards the
# closest target then attack it. Each unit has 200 hit points (health) and an
# attack power of 3. The fight ends when one of the two sides has no more units.
# Below is an input example:
#
#                             #######
#                             #.G...#
#                             #...EG#
#                             #.#.#G#
#                             #..G#E#
#                             #.....#
#                             #######
#
# Part 1: find the product between the number of full rounds completed before
#         the combat ends and the sum of the hit points of all remaining units.
# Part 2: find the smallest attack power boost the elves need to win the fight
#         without any losses.
if __name__ == '__main__':
    if len(sys.argv) != 2:
        sys.exit("usage: ./day15.py INPUT_FILE")
    filename = sys.argv[1]
    if not os.path.exists(filename):
         sys.exit("error: {} does not exist.".format(filename))
    read_map(filename)
    print_map()
