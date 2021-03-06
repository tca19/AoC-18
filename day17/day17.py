#!/usr/bin/env python3

import os
import re
import sys
from collections import deque

# Read `filename` (segment coordinates); return `grid` and start position
# values for x and y axis
def parse_data(filename):
    extractor  = re.compile("-?\d+")
    x_min = y_min = 10000
    x_max = y_max = 0
    vertical = []
    horizontal = []
    with open(filename) as f:
        # lines are either "x=495, y=2..7" (vertical) or "y=7, x=495..501"
        # (horizontal). The problem considers x is the column number, y the row
        for line in f:
            if line[0] == "x":
                y, x_start, x_end = list(map(int, extractor.findall(line)))
                vertical.append((y, x_start, x_end))
                x_min = min(x_min, x_start)
                x_max = max(x_max, x_end)
                y_min = min(y_min, y)
                y_max = max(y_max, y)
            elif line[0] == "y":
                x, y_start, y_end = list(map(int, extractor.findall(line)))
                horizontal.append((x, y_start, y_end))
                x_min = min(x_min, x)
                x_max = max(x_max, x)
                y_min = min(y_min, y_start)
                y_max = max(y_max, y_end)

    HEIGHT = x_max - x_min + 1
    WIDTH  = y_max - y_min + 3 # margin of 1 on each side, water can overflow
    grid   = [ ["."] * WIDTH for _ in range(HEIGHT) ]
    start  = (0, 500 - y_min + 1) # original water spring is at (0, 500)

    for y, x_start, x_end in vertical:
        for x in range(x_start, x_end+1):
            grid[x-x_min][y-y_min+1] = "#" # +1 because margin of 1 on the left
    for x, y_start, y_end in horizontal:
        for y in range(y_start, y_end+1):
            grid[x-x_min][y-y_min+1] = "#" # +1 because margin of 1 on the left
    return grid, start

# Make the water flows from `start` to the bottom, filling containers. Return
# the number of cells reached by the water.
def flow(grid, start):
    HEIGHT = len(grid)
    WIDTH  = len(grid[0])
    # `stack` is a list of points where water starts to move down (sources)
    stack = deque([start])
    while len(stack) > 0:
        x_source, y_source = stack.popleft()
        x, y = x_source, y_source # need a backup to reset the values x and y
        grid[x][y] = "|"

        # water can move down while it finds empty cells
        while x+1 < HEIGHT and grid[x+1][y] == ".":
            grid[x+1][y] = "|"
            x += 1

        # if limit is reached or it arrives where there already is moving water,
        # no more things to do, move to the next water source
        if x+1 == HEIGHT or grid[x+1][y] == "|":
            continue

        # once water reaches a bottom wall, it can fill the container. Spread
        # water on both left and right until the water overflows the container
        flows_on_one_side = False
        while not flows_on_one_side:
            # spread the water to the left. Water can spread to y-1 if there is
            # a floor ("#", "|" or "~") underneath and until it finds a wall "#"
            while grid[x][y-1] != "#" and grid[x+1][y-1] in "#|~":
                grid[x][y-1] = "|"
                y -= 1
            # if cell on the left is not a wall and there is no floor, water can
            # fall from this cell. It becomes a new water source
            if grid[x][y-1] != "#" and grid[x+1][y-1] == ".":
                stack.append((x, y-1))
                flows_on_one_side = True

            # spread the water to the right; first reset y position to be
            # aligned with the source. Water can spread to y+1 if there is a
            # floor ("#", "|" or "~") underneath and until it finds a wall "#"
            y = y_source
            while grid[x][y+1] != "#" and grid[x+1][y+1] in "#|~":
                grid[x][y+1] = "|"
                y += 1
            # if cell on the right is not a wall and there is no floor, water
            # can fall from this cell. It becomes a new water source
            if grid[x][y+1] != "#" and grid[x+1][y+1] == ".":
                stack.append((x, y+1))
                flows_on_one_side = True

            # if the water does not overflow yet, mark all water cells of
            # current level (same x) as resting ("~"). Then move up and repeat
            # the spreading operations.
            if not flows_on_one_side:
                # y is already at the right wall, move back to left wall
                while grid[x][y] != "#":
                    grid[x][y] = "~"
                    y -= 1
                x, y = x-1, y_source
                grid[x][y] = "|"

    # count the number of cells filled by moving or resting water
    moving = resting = 0
    for x in range(HEIGHT):
        for y in range(WIDTH):
            if grid[x][y] == "|" :
                moving += 1
            if grid[x][y] == "~":
                resting += 1
    return moving, resting

# Input file is a list of coordinate ranges forming horizontal/vertical lines
# (such as "x=495, y=2..7", a vertical line if y is the row and x the column).
# These lines represent clay containers, where water can be trapped. An infinite
# source of water + at (500, 0) will produce water that will fall down, filling
# the clay containers. Below is an exemple of lines, and clay containers (both
# unfilled and filled with water).
#
#                                 ......+.......             ......+.......
#                                 ............#.             ......|.....#.
#                                 .#..#.......#.             .#..#||||...#.
#      x=495, y=2..7              .#..#..#......             .#..#~~#|.....
#      y=7, x=495..501            .#..#..#......             .#..#~~#|.....
#      x=501, y=3..7              .#.....#......             .#~~~~~#|.....
#      x=498, y=2..4      ===>    .#.....#......     ===>    .#~~~~~#|.....
#      x=506, y=1..2              .#######......             .#######|.....
#      x=498, y=10..13            ..............             ........|.....
#      x=504, y=10..13            ..............             ...|||||||||..
#      y=13, x=498..504           ....#.....#...             ...|#~~~~~#|..
#                                 ....#.....#...             ...|#~~~~~#|..
#                                 ....#.....#...             ...|#~~~~~#|..
#                                 ....#######...             ...|#######|..
#
# Part 1: find the number of cells the water can reach (both | and ~)
# Part 2: find the number of cells where the water can stay (only ~)
if __name__ == '__main__':
    if len(sys.argv) != 2:
        sys.exit("usage: ./day17.py INPUT_FILE")
    filename = sys.argv[1]
    if not os.path.exists(filename):
        sys.exit("error: {} does not exist.".format(filename))
    moving, resting = flow(*parse_data(filename))
    print("PART ONE:", moving+resting)
    print("PART TWO:", resting)
