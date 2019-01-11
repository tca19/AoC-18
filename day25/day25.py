#!/usr/bin/env python3

import os
import sys

# Return the Manhattan distance with 4-dimensional points x and y
def distance(x, y):
    return abs(x[0]-y[0]) + abs(x[1]-y[1]) + abs(x[2]-y[2]) + abs(x[3]-y[3])

# Return if there is at least a point in L with a distance less than 3 to x
def inside_constellation(x, L):
    for p in L:
        if distance(p, x) <= 3:
            return True
    return False

# Return the number of distincts constellations formed by points
def n_constellations(points):
    constellations = {}
    id = 0
    for p in points:
        possible_constellation = []
        for i, L in constellations.items():
            if inside_constellation(p, L):
                possible_constellation.append(i)
        if len(possible_constellation) == 0:
            constellations[id] = [p]
            id += 1
        elif len(possible_constellation) == 1:
            constellations[possible_constellation[0]].append(p)
        else:
            all_points = []
            for i in possible_constellation:
                all_points += constellations[i]
                del constellations[i]
            constellations[id] = all_points
            id += 1
    return len(constellations)

# Input file is a list of 4-dimensional points, one per line. Two points having
# a Manhattan distance less than 3 form a constellation. If a point has a
# Manhattan distance less than 3 to any point of a constellation, it joins this
# constellation.
#
# Part 1: find the number of distinct constellation formed by the points
# Part 2: solve all the previous problems
if __name__ == '__main__':
    if len(sys.argv) != 2:
        sys.exit("usage: ./day25.py INPUT_FILE")
    filename = sys.argv[1]
    if not os.path.exists(filename):
        sys.exit("error: {} does not exist.".format(filename))
    points = [list(map(int, line.split(","))) for line in open(filename)]
    print("PART ONE:", n_constellations(points))
