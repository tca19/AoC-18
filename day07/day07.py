#!/usr/bin/env python3

import os
import sys
from collections import defaultdict

# Read filename, return a dict that maps a task to all the task requiring it.
def parse(filename):
    tree = defaultdict(set)
    for line in open(filename).read().splitlines():
        line = line.strip().split()
        # line is like "Step T must be finished before step C can begin."
        # so the important information are line[1] and line[-3].
        tree[line[1]].add(line[-3])
    return tree

# Input file is a list of steps and requirements about which steps must be
# finished before others can begin. Lines are like:
# "Step T must be finished before step C can begin."
#
# Part 1: find the order in which the steps should be completed.
# Part 2: each step has a different duration and some workers are able to
#         perform tasks simultaneously. Find the time required to perform all
#         the steps considering that only 5 workers are available.
if __name__ == '__main__':
    if len(sys.argv) != 2:
        sys.exit("usage: ./day07.py INPUT_FILE")
    filename = sys.argv[1]
    if not os.path.exists(filename):
         sys.exit("error: {} does not exist.".format(filename))
    tree = parse(filename)
