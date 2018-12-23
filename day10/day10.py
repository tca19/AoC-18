#!/usr/bin/env python3

import os
import re
import sys

# Return the number of seconds needed for the points to form a message.
def seconds_to_converge(points, vy):
    # Assume the final message has a height smaller than 15. It means that the
    # distance between the points with the largest/smallest y will have a
    # distance less than 15.
    # Let's D be the distance between those two points at the beginning and v
    # the speed at which these points move closer to each other. Then the time t
    # to converge verifies: D - t*v <= 15 therefore t >= (D-15)/v.
    y_and_v = [ (p[1], v) for p,v in zip(points, vy) ]
    y_and_v.sort() # first item has smallest y, last item has largest y
    D = y_and_v[-1][0] - y_and_v[0][0]
    v = y_and_v[0][1] - y_and_v[-1][1]

    return int((D-15) / v) + 1 # t has to be greater, and must be an int

# Return the coordinates of the bounding box which includes all points.
def bounding_box(points):
    xmin = xmax = points[0][0]
    ymin = ymax = points[0][1]
    for p in points[1:]:
        xmin = min(xmin, p[0])
        xmax = max(xmax, p[0])
        ymin = min(ymin, p[1])
        ymax = max(ymax, p[1])
    return xmin, xmax, ymin, ymax

# Return the ascii art message displayed after a certain number of iterations.
def find_message(points, vx, vy, iterations):
    # move the points like a certain number of iteration happened
    for i in range(len(points)):
        points[i][0] += vx[i] * iterations
        points[i][1] += vy[i] * iterations

    # build ascii message, with '#' for points. The size of the message is the
    # same as the bounding box.
    xmin, xmax, ymin, ymax = bounding_box(points)
    grid = [ [' ' for _ in range(xmin, xmax+1)] for _ in range(ymin, ymax+1) ]
    for x, y in points:
        grid[y-ymin][x-xmin] = '#'

    message = ["".join(row) for row in grid]
    return '\n'.join(message)

# Input file is a list of points with their X,Y coordinates and vX,vY
# velocities. The points are placed throughout the space and move at each second
# according to their velocity. At one moment, the points will be aligned in the
# space and will form a message.
#
# Part 1: find the message displayed by the points.
# Part 2: find out how many seconds it takes for the message to appear.
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
    iterations = seconds_to_converge(points, vy)
    message = find_message(points, vx, vy, iterations)
    print("PART ONE:\n" + message)
    print("PART TWO:", iterations)
