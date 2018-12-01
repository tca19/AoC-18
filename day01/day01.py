#!/usr/bin/env python3

import os.path

def first_duplicate(changes):
    frequency, i = 0, 0
    seen_frequencies = set()

    while True:
        seen_frequencies.add(frequency)
        frequency += changes[i % len(changes)]
        if frequency in seen_frequencies:
            return frequency
        i += 1

if __name__ == '__main__':
    filename = "day01_changes.txt"

    if not os.path.exists(filename):
        print("ERROR. Name your input file as:", filename)
    else:
        changes = list(map(int, open(filename).read().split()))
        print("PART ONE:", sum(changes))
        print("PART TWO:", first_duplicate(changes))
