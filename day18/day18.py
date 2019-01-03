#!/usr/bin/env python3

import os
import sys

# Update the grid according to rules stated in the problem, return the new grid
def update(grid):
    HEIGHT = len(grid)
    WIDTH  = len(grid[0])
    new_grid = [["."] * WIDTH for _ in range(HEIGHT)]
    for x in range(1, HEIGHT-1):    # start at 1, end at -1 = because of margin
        for y in range(1, WIDTH-1):
            # count the occurrence of each symbol on the 8 adjacent cells
            count = {".": 0, "|": 0, "#": 0}
            count[grid[x-1][y-1]] += 1
            count[grid[x-1][y  ]] += 1
            count[grid[x-1][y+1]] += 1
            count[grid[x  ][y-1]] += 1
            count[grid[x  ][y+1]] += 1
            count[grid[x+1][y-1]] += 1
            count[grid[x+1][y  ]] += 1
            count[grid[x+1][y+1]] += 1

            # see if cell type can be modified by rules. Otherwise leave it as
            # it is
            if grid[x][y] == "." and count["|"] >= 3:
                new_grid[x][y] = "|"
            elif grid[x][y] == "|" and count["#"] >= 3:
                new_grid[x][y] = "#"
            elif grid[x][y] == "#" and (count["#"] < 1 or count["|"] < 1):
                new_grid[x][y] = "."
            else:
                new_grid[x][y] = grid[x][y]
    return new_grid

# Return the string version of grid (concatenation of all cells)
def to_string(grid):
    return "".join(["".join(line) for line in grid])

# Return the resource value of grid (n_trees * n_lumberyards) after N iterations
def resource_value(grid, N=0):
    # keep an history of previous grid states, to find possible cycles
    saved = {to_string(grid): 0}

    # make the grid updates itself
    iter = 0
    while iter < N:
        grid = update(grid)
        iter += 1
        if to_string(grid) in saved: # we have a cycle, skip many steps
            cycle_length = iter - saved[to_string(grid)]
            iter += ((N-iter) // cycle_length) * cycle_length
        else:
            saved[to_string(grid)] = iter

    # compute the resource value of grid
    n_trees = n_lumberyards = 0
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if grid[i][j] == "|":
                n_trees += 1
            if grid[i][j] == "#":
                n_lumberyards += 1
    return n_trees * n_lumberyards

# Input file represents a grid (50 acres by 50 acres) where each square can be
# either open ground ("."), trees ("|") or a lumberyard ("#"). At each minute,
# each square can change according to its environment: open ground can become
# trees, trees can become lumberyards and lumberyards can become open ground.
#
# Part 1: find the product between the number of trees and lumberyards in the
#         grid after 10 minutes.
# Part 2: find the product between the number of trees and lumberyards in the
#         grid after 1000000000 minutes.
if __name__ == '__main__':
    if len(sys.argv) != 2:
        sys.exit("usage: ./day18.py INPUT_FILE")
    filename = sys.argv[1]
    if not os.path.exists(filename):
        sys.exit("error: {} does not exist.".format(filename))
    # add a margin of 1 cell "." all around the grid (easier to take the
    # adjacent elements for the cells on the edges)
    grid = [["."] + list(l) + ["."] for l in open(filename).read().splitlines()]
    grid = [["."] * len(grid[0])] + grid + [["."] * len(grid[0])]
    print("PART ONE:", resource_value(grid, 10))
    print("PART TWO:", resource_value(grid, 1000000000))
