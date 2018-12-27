#!/usr/bin/env python3

import os
import sys
from collections import deque

grid = []
units = []

class Unit:
    def __init__(self, type, x, y):
        self.type   = type
        self.x      = x
        self.y      = y
        self.health = 200
        self.attack = 3

    # Move the unit towards a target, only if not already in a target range.
    def move(self):
        enemy = "G" if self.type == "E" else "E"

        # the entire map is surrounded by walls, so no need to test if positions
        # x-1 or x+1 are valid.
        if grid[self.x-1][self.y] == enemy \
        or grid[self.x+1][self.y] == enemy \
        or grid[self.x][self.y-1] == enemy \
        or grid[self.x][self.y+1] == enemy:
            return # already in range, no need to move

        # use bfs to know each reachable target with distance and path to it
        stack = deque([(self.x-1, self.y, 1, [(self.x, self.y)]),
                       (self.x, self.y-1, 1, [(self.x, self.y)]),
                       (self.x, self.y+1, 1, [(self.x, self.y)]),
                       (self.x+1, self.y, 1, [(self.x, self.y)])])
        visited = set()
        reachable = []
        while len(stack) > 0:
            x, y, distance, path = stack.popleft()
            if (x, y) in visited:
                continue
            visited.add((x, y))
            if grid[x][y] == enemy:
                reachable.append((distance, x, y, path))
            elif grid[x][y] in "#EG":
                continue # can't move further if it reaches a wall or a unit

            # go to top, left, right, down: it corresponds to the sorted order
            stack.append((x-1, y, distance+1, path + [(x,y)]))
            stack.append((x, y-1, distance+1, path + [(x,y)]))
            stack.append((x, y+1, distance+1, path + [(x,y)]))
            stack.append((x+1, y, distance+1, path + [(x,y)]))

        # get closest target and the next cell in the path leading to it
        closest = min(reachable) # distance is first field so min is the closest
        _, _, _, path = closest
        next_x, next_y = path[1] # path[0] is self, path[1] is next cell

        # move self to next cell, update its position in `grid`
        grid[next_x][next_y] = self.type
        grid[self.x][self.y] = "."
        self.x, self.y = next_x, next_y

# Read the content of filename to get the unit positions and the map. Fill the
# global variables `grid` (2D list) and `units` (list of Unit instances).
def read_map(filename):
    with open(filename) as f:
        for i, line in enumerate(f):
            grid.append(list(line.strip())) # use list because str is immutable
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
    units[0].move()
    print_map()
