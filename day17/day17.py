#!/usr/bin/env python3

import os
import sys

# Input file is a list of coordinate ranges forming horizontal/vertical lines
# (such as "x=495, y=2..7", a vertical line if y is the row and x the column).
# These lines represent clay recipients, where water can be trapped. An infinite
# source of water at (500, 0) will produce water that will fall down, filling
# the clay recipients. Below is an exemple of lines, and clay recipients (both
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
