#!/usr/bin/env python3

import os
import sys

# Read filename to get coordinates of places, return max/min of x and y
def parse(filename):
    places = [list(map(int, line.split(',')))
              for line in open(filename).read().splitlines()]
    minx, maxx = places[0]
    miny, maxy = places[0]
    for x, y in places[1:]:
        if x < minx:
            minx = x
        if x > maxx:
            maxx = x
        if y < miny:
            miny = y
        if y > maxy:
            maxy = y
    return places, minx, maxx, miny, maxy

# Return the index of the place in `places` which is the closest to point (x,y).
# Return None if there is a tie (2 or more places has the same distance).
def index_closest_place(x, y, places):
    min_d = 10**9
    closest_place = None
    has_tie = False
    for index, (px, py) in enumerate(places):
        d = abs(px - x) + abs(py - y)
        if d < min_d:
            min_d = d
            closest_place = index
            has_tie = False
        elif d == min_d:
            has_tie = True
    if not has_tie:
        return closest_place

# Return the size of the finite area with the largest number of cells having the
# same closest place.
def largest_area_same_closest(places, minx, maxx, miny, maxy):
    # Places are scattered all around an infinite grid. Each cell of this grid
    # has 1 (or more) closest places (using the Manhattan distance). When a
    # group of adjacent cells have the same closest place, they form an area.
    # Since the grid is infinite, some area are also infinite (especially the
    # ones in the corners). To know which area are finite, we first consider the
    # entire grid bounded by (minx, miny) and (maxx, maxy), and then slightly
    # expand this grid. Areas with a finite size will have the same size,
    # whereas the inifinite areas will have a bigger size (because the grid is
    # bigger).  This function returns the largest area size which has a size
    # independent of the size of the grid.

    # 1 area per place because points can only has 1 closest area
    areas = [0 for _ in places]
    for x in range(minx, maxx+1):
        for y in range(miny, maxy+1):
            idx = index_closest_place(x, y, places)
            if idx is not None:
                areas[idx] += 1

    # when a point outside the grid belongs to an area, it means this area is
    # infinite, so mark its size as -1 so it can't be the largest one.
    for x in range(minx-1, maxx+2):            # top edge
        idx = index_closest_place(x, miny-1, places)
        if idx is not None:
            areas[idx] = -1
    for x in range(minx-1, maxx+2):            # bottom edge
        idx = index_closest_place(x, maxy+2, places)
        if idx is not None:
            areas[idx] = -1
    for y in range(miny-1, maxy+2):            # left edge
        idx = index_closest_place(minx-1, y, places)
        if idx is not None:
            areas[idx] = -1
    for y in range(miny-1, maxy+2):            # right edge
        idx = index_closest_place(maxx+2, y, places)
        if idx is not None:
            areas[idx] = -1

    return max(areas)

# Return the number of cells having a total distance to all places less than
# `N`. Total distance is the sum of all the Manhattan distance to each place.
def ncells_close_to_all(places, minx, maxx, miny, maxy, N):
    ncells = 0
    for x in range(minx, maxx+1):
        for y in range(miny, maxy+1):
            total_distance = 0
            for px, py in places:
                total_distance += abs(px-x) + abs(py-y)
            if total_distance < N:
                ncells += 1
    return ncells

# Input file is a list of point coordinates (x, y), one per line, representing
# places in an infinite grid.
#
# Part 1: find the size of the largest area of points having the same closest
#         place (infinite area do not count).
# Part 2: find the size of the area of points having a total Manhattan distance
#         to places less than 10000 (the total distance is the sum of Manhattan
#         distance to all places coordinates).
if __name__ == '__main__':
    if len(sys.argv) != 2:
        sys.exit("usage: ./day06.py INPUT_FILE")
    filename = sys.argv[1]
    if not os.path.exists(filename):
         sys.exit("error: {} does not exist.".format(filename))
    places, minx, maxx, miny, maxy = parse(filename)
    print("PART ONE:", largest_area_same_closest(places, minx, maxx, miny, maxy))
    print("PART TWO:", ncells_close_to_all(places, minx, maxx, miny, maxy, 10000))
