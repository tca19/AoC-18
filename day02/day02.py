#!/usr/bin/env python3

import os.path
from collections import Counter

def checksum(list_id):
    two = 0
    three = 0
    for id in list_id:
        c = Counter(id)
        if 2 in c.values():
            two += 1
        if 3 in c.values():
            three += 1
    return two * three

if __name__ == '__main__':
    filename = "day02_boxIDs.txt"
    if not os.path.exists(filename):
        print("ERROR. Name your input file as:", filename)
    else:
        IDs = open(filename).read().splitlines()
        part_1 = checksum(IDs)
        print("PART ONE:", part_1)
