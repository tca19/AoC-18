#!/usr/bin/env python3

import os
import sys
from itertools import cycle

def first_duplicate(frequency_changes):
    frequency = 0
    seen_frequencies = set()

    for val in cycle(frequency_changes):
        seen_frequencies.add(frequency)
        frequency += val
        if frequency in seen_frequencies:
            return frequency

# Input file is a list of frequency changes like +3, -2, -7, +10... one per
# line.
#
# Part 1: find the final frequency after applying each change (start at 0).
# Part 2: repeat the changes indefinetely. What is the first frequency to be
#         duplicated?
if __name__ == '__main__':
    if len(sys.argv) != 2:
        sys.exit("usage: ./day01.py INPUT_FILE")
    filename = sys.argv[1]
    if not os.path.exists(filename):
         sys.exit("error: {} does not exist.".format(filename))
    frequency_changes = list(map(int, open(filename).read().splitlines()))
    print("PART ONE:", sum(frequency_changes))
    print("PART TWO:", first_duplicate(frequency_changes))
