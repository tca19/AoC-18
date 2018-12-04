#!/usr/bin/env python3

import os
import sys
from itertools import cycle

def first_duplicate(changes):
    frequency = 0
    seen_frequencies = set()

    for val in cycle(changes):
        seen_frequencies.add(frequency)
        frequency += val
        if frequency in seen_frequencies:
            return frequency

if __name__ == '__main__':
    if len(sys.argv) != 2:
        sys.exit("usage: ./day01.py INPUT_FILE")
    filename = sys.argv[1]
    if not os.path.exists(filename):
         sys.exit("error: {} does not exist.".format(filename))
    else:
        changes = list(map(int, open(filename).read().split()))
        print("PART ONE:", sum(changes))
        print("PART TWO:", first_duplicate(changes))
