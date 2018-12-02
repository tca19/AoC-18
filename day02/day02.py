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

def common_correct_letters(list_id):
    for i in range(len(list_id)-1):
        for j in range(i+1, len(list_id)):
            s1 = list_id[i]
            s2 = list_id[j]
            distance = sum([1 for a,b in zip(s1, s2) if a != b])
            if distance == 1:
                return "".join([a for a,b in zip(s1, s2) if a == b])

if __name__ == '__main__':
    filename = "day02_boxIDs.txt"
    if not os.path.exists(filename):
        print("ERROR. Name your input file as:", filename)
    else:
        list_id = open(filename).read().splitlines()
        part_1 = checksum(list_id)
        print("PART ONE:", part_1)
        part_2 = common_correct_letters(list_id)
        print("PART TWO:", part_2)
