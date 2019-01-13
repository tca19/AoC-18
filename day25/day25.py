#!/usr/bin/env python3

import os
import sys
from collections import defaultdict

# Return the Manhattan distance between the 4-dimensional points x and y
def distance(x, y):
    return abs(x[0]-y[0]) + abs(x[1]-y[1]) + abs(x[2]-y[2]) + abs(x[3]-y[3])

# Return if there is at least a point in L with a distance less than 3 to x
def inside_constellation(x, L):
    for point in L:
        if distance(point, x) <= 3:
            return True
    return False

# Return the number of distincts constellations formed by points
def n_constellations(points):
    # create an undirected graph where vertices are the points and two vertices
    # are connected by an edge if the distance between the points is less than 3
    edges = defaultdict(set)
    for i in range(len(points)):
        for j in range(i+1, len(points)):
            if distance(points[i], points[j]) <= 3:
                edges[i].add(j)
                edges[j].add(i)
    # number of distincts constellations = number of connected components
    n_connected = 0
    seen = set()
    for i in range(len(points)):
        if i in seen:
            continue
        n_connected += 1
        # go through all the neighbors of i, mark them as seen
        stack = [i]
        while stack:
            node = stack.pop()
            if node in seen:
                continue
            seen.add(node)
            for neighbor in edges[node]:
                stack.append(neighbor)
    return n_connected

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
