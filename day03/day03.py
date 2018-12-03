#!/usr/bin/env python3

import os.path

grid = [ [0 for _ in range(1000)] for _ in range(1000) ]

def parse_file(filename):
    data = []
    with open(filename) as f:
        for line in f:
            id, _, pos, size = line.split()
            x, y = pos[:-1].split(',')
            width, height = size.split('x')
            x      = int(x)
            y      = int(y)
            width  = int(width)
            height = int(height)
            data.append((id, x, y, width, height))
    return data

def size_overlap(lines):
    total_overlap = 0
    for line in lines:
        id, x, y, width, height = line
        for i in range(x, x+width):
            for j in range(y, y+height):
                if grid[i][j] == 1:
                    total_overlap += 1
                grid[i][j] += 1
    return total_overlap

def id_not_overlap(lines):
    for line in lines:
        id, x, y, width, height = line
        does_overlap = False
        for i in range(x, x+width):
            for j in range(y, y+height):
                if grid[i][j] > 1:
                    does_overlap = True
        if not does_overlap:
            return id[1:]

if __name__ == '__main__':
    filename = "day03_claims.txt"
    if not os.path.exists(filename):
        print("ERROR. Name your input file as:", filename)
    else:
        lines = parse_file(filename)
        part_1 = size_overlap(lines)
        print("PART ONE:", part_1)
        part_2 = id_not_overlap(lines)
        print("PART TWO:", part_2)