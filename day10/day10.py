#!/usr/bin/env python3

import os
import re
import sys

# Input file is a list of points with their X,Y coordinates and vX,vY
# velocities. The points are placed throughout the space and move at each second
# according to their velocity. At one moment, the points will be aligned in the
# space and will form a message.
#
# Part 1: find the message displayed by the points.
# Part 2: find out the second the message appears.
if __name__ == '__main__':
    if len(sys.argv) != 2:
        sys.exit("usage: ./day10.py INPUT_FILE")
    filename = sys.argv[1]
    if not os.path.exists(filename):
         sys.exit("error: {} does not exist.".format(filename))
    # each line is like: position=<-41933,  10711> velocity=< 4, -1>
    data = [re.findall("-?\d+", l) for l in open(filename).read().splitlines()]
    points = [ [int(l[0]), int(l[1])] for l in data ]
    vx, vy = [ int(l[2]) for l in data ], [ int(l[3]) for l in data ]
