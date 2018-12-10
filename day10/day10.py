#!/usr/bin/env python3

import os
import re
import sys

# Return the coordinates of the bounding box that includes all points.
def bounding_box(points):
    xmin = xmax = points[0][0]
    ymin = ymax = points[0][1]
    for p in points[1:]:
        xmin = min(xmin, p[0])
        xmax = max(xmax, p[0])
        ymin = min(ymin, p[1])
        ymax = max(ymax, p[1])
    return xmin, xmax, ymin, ymax

# Return the message as ascii art and the number of iterations needed to get it.
def find_message(points, vx, vy):
    iteration = 0

    # simulate the movements of the points. Stop once the bounding box of the
    # points has a height smaller than 15 (suppose that the size of the letters
    # is less than 15).
    xmin, xmax, ymin, ymax = bounding_box(points)
    while (ymax - ymin) >= 15:
        # update the position of each point
        for i in range(len(points)):
            points[i][0] += vx[i]
            points[i][1] += vy[i]
        iteration += 1
        xmin, xmax, ymin, ymax = bounding_box(points)

    # build ascii message, with '#' for points. The size of the message is the
    # same as the bounding box.
    grid = [ [' ' for _ in range(xmin, xmax+1)] for _ in range(ymin, ymax+1) ]
    for x, y in points:
        grid[y-ymin][x-xmin] = '#'

    message = ["".join(row) for row in grid]
    return '\n'.join(message), iteration

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
    message, iteration = find_message(points, vx, vy)
    print("PART ONE:\n" + message)
