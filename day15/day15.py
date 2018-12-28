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
        self.power  = 3

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

        # use BFS to know the reachable cells that are in a target range. For
        # each one, find the distance and path to it
        stack = deque([(self.x-1, self.y, 1, [(self.x, self.y)]),
                       (self.x, self.y-1, 1, [(self.x, self.y)]),
                       (self.x, self.y+1, 1, [(self.x, self.y)]),
                       (self.x+1, self.y, 1, [(self.x, self.y)])])
        visited = set()
        reachable = []
        while len(stack) > 0:
            x, y, distance, path = stack.popleft()
            path += [(x,y)] # add current cell to path
            if (x, y) in visited:
                continue
            visited.add((x, y))

            # can't move further if it reaches a wall or a unit
            if grid[x][y] in "#EG":
                continue

            # if current cell is in the range of an enemy, add it to the list
            if grid[x-1][y] == enemy or grid[x][y-1] == enemy \
            or grid[x][y+1] == enemy or grid[x+1][y] == enemy:
                reachable.append((distance, x, y, path))

            # go to visit top/left/right/down: it is the sorted reading order
            stack.append((x-1, y, distance+1, path))
            stack.append((x, y-1, distance+1, path))
            stack.append((x, y+1, distance+1, path))
            stack.append((x+1, y, distance+1, path))

        # no reachable target, no move
        if not reachable:
            return

        # get closest target and the next cell in the path leading to it. The
        # reachable cells are composed of (distance, x, y, path). So min() first
        # choose the one with minimal distance. If there are ties, x and y will
        # sort them in reading order.
        closest = min(reachable)
        _, _, _, path = closest
        next_x, next_y = path[1] # path[0] is self, path[1] is next cell

        # move self to next cell, update its position in `grid`
        grid[next_x][next_y] = self.type
        grid[self.x][self.y] = "."
        self.x, self.y = next_x, next_y

    # Attack an enemy. Do nothing if no enemy are within range.
    def attack(self):
        enemy = "G" if self.type == "E" else "E"
        all_targets = [ u for u in units if u.type == enemy and u.health > 0 \
            and (  (u.x == self.x-1 and u.y == self.y) \
                or (u.x == self.x and u.y == self.y-1) \
                or (u.x == self.x and u.y == self.y+1) \
                or (u.x == self.x+1 and u.y == self.y) ) ]
        if not all_targets: # all_targets is empty
            return # no target reachable, no attack
        target = sorted(all_targets, key=lambda u: (u.health, u.x, u.y))[0]
        target.health -= self.power
        if target.health <= 0:
            grid[target.x][target.y] = "."
            del units[units.index(target)]

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
    units.sort(key=lambda u: (u.x, u.y))
    index = 0
    for row in grid:
        units_of_line = []
        for cell in row:
            print(cell, end="")
            if cell in "EG":
                units_of_line.append("{}({})".format(cell, units[index].health))
                index += 1
        print("  ", ", ".join(units_of_line))

# Simulate a round: each unit, in turn,  moves and then attacks.
def play_round():
    # sort units by their position (top to bottom, left to right)
    for u in sorted(units, key=lambda u: (u.x, u.y)):
        # if unit is dead, it can't move or attack. The unit is actually already
        # deleted from the `units` list, but this for loop iterates over a copy
        # of the `units` list (so it is not updated). This is because the order
        # of units in a round is determined by their position at the beginning
        # of the round, not their position during the round (because positions
        # can change and a unit could play mutiple times if the order changes).
        if u.health <= 0:
            continue
        u.move()
        u.attack()

# Simulate a battle: make the units fight each other in rounds until one of the
# two side dies. Return the product between the number of full rounds completed
# and the sum of the health of all units still alive.
def play_battle():
    completed_round = 0
    while True:
        play_round()
        health_G = sum([u.health for u in units if u.type == "G"])
        health_E = sum([u.health for u in units if u.type == "E"])
        if health_G == 0:
            return completed_round * health_E
        if health_E == 0:
            return completed_round * health_G
        completed_round += 1

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
    print("PART ONE:", play_battle())
