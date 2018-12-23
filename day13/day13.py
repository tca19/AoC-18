#!/usr/bin/env python3

import os
import sys

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
