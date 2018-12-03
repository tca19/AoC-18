#!/usr/bin/env python3

import os.path

grid = [ [0 for _ in range(1000)] for _ in range(1000) ]

def size_overlap(lines):
    total_overlap = 0
    for line in lines:
        _, _, pos, size = line.split()
        x, y = pos[:-1].split(',')
        width, height = size.split('x')
        x      = int(x)
        y      = int(y)
        width  = int(width)
        height = int(height)
        for i in range(x, x+width):
            for j in range(y, y+height):
                if grid[i][j] == 1:
                    total_overlap += 1
                grid[i][j] += 1

    return total_overlap

if __name__ == '__main__':
    filename = "day03_claims.txt"
    if not os.path.exists(filename):
        print("ERROR. Name your input file as:", filename)
    else:
        lines = open(filename).read().splitlines()
        part_1 = size_overlap(lines)
        print("PART ONE:", part_1)
