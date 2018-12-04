#!/usr/bin/env python3

import os
import sys
from collections import defaultdict

# Input file is composed of 3 types of lines:
#   - shift info:        [1518-11-01 00:00] Guard #10 begins shift
#   - sleep info:        [1518-11-01 00:05] falls asleep
#   - waking up info:    [1518-11-01 00:25] wakes up
# The lines describe the sleep activity of some guards. Lines are not in
# chronological order. The times mentioned are all between 00:00 and 00:59.
#
# Part 1: find the guard that has the most minutes asleep and the minute when
#         this guard spends most asleep.
# Part 2: find the guard which is most frequently asleep on the same minute.
if __name__ == '__main__':
    if len(sys.argv) != 2:
        sys.exit("usage: ./day04.py INPUT_FILE")
    filename = sys.argv[1]
    if not os.path.exists(filename):
         sys.exit("error: {} does not exist.".format(filename))
    data = open(filename).read().splitlines()
    print(data)
