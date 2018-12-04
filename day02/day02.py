#!/usr/bin/env python3

import os
import sys
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

# Input is a list of box IDs like bpacnmelhhzpygfsjoxtvkwuor,
# biacnmelnizqygfsjoctvkwudr... One ID per line.
#
# Part 1: compute the product between the number of IDs which have exactly two
#         of any letter and the number of IDs which have exactly tree of any
#         letter.
# Part 2: find the two IDs which only differs by 1 char. Print the common
#         letters of these IDs.
if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit("usage: ./day02.py INPUT_FILE")
    filename = sys.argv[1]
    if not os.path.exists(filename):
         sys.exit("error: {} does not exist.".format(filename))
    list_id = open(filename).read().splitlines()
    part_1 = checksum(list_id)
    print("PART ONE:", part_1)
    part_2 = common_correct_letters(list_id)
    print("PART TWO:", part_2)
