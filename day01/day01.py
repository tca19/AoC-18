#!/usr/bin/env python3

import os.path
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
    filename = "day01_changes.txt"

    if not os.path.exists(filename):
        print("ERROR. Name your input file as:", filename)
    else:
        changes = list(map(int, open(filename).read().split()))
        print("PART ONE:", sum(changes))
        print("PART TWO:", first_duplicate(changes))
