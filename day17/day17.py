#!/usr/bin/env python3

import os
import re
import sys

SIZE = 2000 # assume maximum x and y will be 2000
grid = [ ["." for _ in range(SIZE)] for _ in range(SIZE) ]
x_min = y_min = SIZE
x_max = y_max = 0

# Read `filename` (segment coordinates); add lines in `grid`; find min/max
def parse_data(filename):
    extractor  = re.compile("-?\d+")
    global x_min, x_max, y_min, y_max
    with open(filename) as f:
        # lines are either "x=495, y=2..7" (vertical) or "y=7, x=495..501"
        # (horizontal). The problem considers x is the column number, y the row
        for line in f:
            if line[0] == "x":
                y, x_start, x_end = list(map(int, extractor.findall(line)))
                for x in range(x_start, x_end+1):
                    grid[x][y] = "#"
                x_min = min(x_min, x_start)
                x_max = max(x_max, x_end)
                y_min = min(y_min, y)
                y_max = max(y_max, y)
            elif line[0] == "y":
                x, y_start, y_end = list(map(int, extractor.findall(line)))
                for y in range(y_start, y_end+1):
                    grid[x][y] = "#"
                x_min = min(x_min, x)
                x_max = max(x_max, x)
                y_min = min(y_min, y_start)
                y_max = max(y_max, y_end)

# Input file is a list of coordinate ranges forming horizontal/vertical lines
# (such as "x=495, y=2..7", a vertical line if y is the row and x the column).
# These lines represent clay containers, where water can be trapped. An infinite
# source of water at (500, 0) will produce water that will fall down, filling
# the clay containers. Below is an exemple of lines, and clay container (both
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
    parse_data(filename)
    print_grid()
