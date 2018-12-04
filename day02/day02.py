#!/usr/bin/env python3

import os
import sys
from collections import Counter

# Return the product between:
#   - number of box IDs which have at least one letter appearing twice
#   - number of box IDs which have at least one letter appearing three times
def checksum(list_id):
    two = 0
    three = 0
    # for each id, count occurrence of each letter. Find if a letter has exactly
    # 2 (or 3) occurrences.
    for id in list_id:
        c = Counter(id)
        if 2 in c.values(): # there is a letter with only 2 occurrences
            two += 1
        if 3 in c.values(): # there is a letter with only 3 occurrences
            three += 1
    return two * three

# Find the two correct IDs: the ones which differ by only 1 character. Return
# the common letters of these IDs.
def common_correct_letters(list_id):
    L = len(list_id)
    for i in range(L-1):
        for j in range(i+1, L):
            s1 = list_id[i]
            s2 = list_id[j]
            distance = sum([1 for a,b in zip(s1, s2) if a != b])
            if distance == 1: # found the correct couple, can return result
                return "".join([a for a,b in zip(s1, s2) if a == b])

# Input is a list of box IDs like bpacnmelhhzpygfsjoxtvkwuor,
# biacnmelnizqygfsjoctvkwudr... One ID per line.
#
# Part 1: compute the product between the number of box IDs which have exactly
#         two of any letter and the number of IDs which have exactly tree of any
#         letter.
# Part 2: find the two box IDs which only differs by 1 char. Print the common
#         letters of these box IDs.
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
