#!/usr/bin/env python3

import os.path

if __name__ == '__main__':
    filename = "day01_changes.txt"

    if not os.path.exists(filename):
        print("ERROR. Name your input file as:", filename)
    else:
        changes = list(map(int, open(filename).read().split()))
        print("PART ONE:", sum(changes))
