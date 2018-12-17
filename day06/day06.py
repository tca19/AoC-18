#!/usr/bin/env python3

import os
import sys

# Return the index of the place in `places` which is the closest to point (x,y).
# Return None if there is a tie (2 or more places has the same distance)
def index_closest_place(x, y, places):
    min_d = 10**9
    closest_place = []
    for index, (px, py) in enumerate(places):
        d = abs(px - x) + abs(py - y)
        if d < min_d:
            min_d = d
            closest_place = [index]
        elif d == min_d:
            closest_place.append(index)
    return closest_place[0] if len(closest_place) == 1 else None

# Return the size of the finite area with the largest number of cells having the
# same closest place.
def largest_area_same_closest(places):
    # Places are scattered all around an infinite grid. Each cell of this grid
    # has 1 (or more) closest places (using the Manhattan distance). When a
    # group of adjacent cells have the same closest place, they form an area.
    # Since the grid is infinite, some area are also infinite (especially the
    # ones in the corners). To know which area are finite, we first consider a
    # basic grid, and then slightly expand this grid. Area with a finite size
    # will have the same size, whereas the inifinite area will have a bigger
    # size (because the grid is bigger). This function returns the largest area
    # size which has a size independent of the size of the grid.
    minx = min([x for x,y in places])
    maxx = max([x for x,y in places])
    miny = min([y for x,y in places])
    maxy = max([y for x,y in places])

    area_basic_grid = [0 for _ in places]
    for x in range(minx, maxx+1):
        for y in range(miny, maxy+1):
            idx = index_closest_place(x, y, places)
            if idx is not None:
                area_basic_grid[idx] += 1

    area_expanded_grid = [0 for _ in places]
    s = 10
    for x in range(minx - s, maxx+1 + s):
        for y in range(miny - s, maxy+1 + s):
            idx = index_closest_place(x, y, places)
            if idx is not None:
                area_expanded_grid[idx] += 1

    finite_area = [a for a,b in zip(area_basic_grid, area_expanded_grid) if a == b]
    return max(finite_area)

# Return the number of cells having a total distance to all places less than
# `N`. Total distance is the sum of all the Manhattan distance to each place.
def ncells_close_to_all(places, N):
    minx = min([x for x,y in places])
    maxx = max([x for x,y in places])
    miny = min([y for x,y in places])
    maxy = max([y for x,y in places])

    ncells = 0
    for x in range(minx, maxx+1):
        for y in range(miny, maxy+1):
            distances = [abs(px - x) + abs(py - y) for px,py in places]
            if sum(distances) < N:
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
    places = [list(map(int, line.split(',')))
              for line in open(filename).read().splitlines()]
    print("PART ONE:", largest_area__same_closest(places))
    print("PART TWO:", ncells_close_to_all(places, 10000))
