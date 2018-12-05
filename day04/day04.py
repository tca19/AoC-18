#!/usr/bin/env python3

import os
import sys
from collections import defaultdict

# Each guard has an array of 60 values. Each value is the number of times they
# were asleep during this minute (00:00 -> 00:59 is 60 minutes so 60 values)
guards_sleep = defaultdict(lambda: [0 for _ in range(60)])

# Read the data to get the moments where each guard fell asleep. Increment by 1
# the occurrence of each concerned minutes in `guards_sleep`.
def init_guards_sleep(data):
    # data is not sorted in chronological order but since every lines start with
    # the date in "%Y-%M-%D %H-%M" format, lexicographic order is the same as
    # chronological order.
    data.sort()
    for line in data:
        if "Guard" in line: # get the id of the current guard (see line 47)
            id_guard = int(line.split()[3][1:])
        if "falls" in line: # get starting minute of sleeping interval
            start = int(line.split()[1][3:5])
        if "wakes" in line: # get ending minute = know the interval to increment
            end = int(line.split()[1][3:5])
            for i in range(start, end):
                guards_sleep[id_guard][i] += 1

# Return the product between:
#   - the id of the guard who slept the most
#   - the minute when this guard was most frequently asleep
def strategy_one():
    total_sleep = [(sum(sleep), id) for id,sleep in guards_sleep.items()]
    id_guard = max(total_sleep)[1]
    sleepiest_minute = guards_sleep[id_guard].index(max(guards_sleep[id_guard]))
    return id_guard * sleepiest_minute

# Return the product between:
#   - the id of the guard who is most frequently asleep on the same minute
#   - the minute when this guard was most frequently asleep
def strategy_two():
    most_frequent = [(max(sleep), id) for id,sleep in guards_sleep.items()]
    id_guard = max(most_frequent)[1]
    sleepiest_minute = guards_sleep[id_guard].index(max(guards_sleep[id_guard]))
    return id_guard * sleepiest_minute

# Input file is composed of 3 types of lines:
#   - shift info:        [1518-11-01 00:00] Guard #10 begins shift
#   - sleep info:        [1518-11-01 00:05] falls asleep
#   - waking up info:    [1518-11-01 00:25] wakes up
# The lines describe the sleep activity of some guards. Lines are NOT in
# chronological order. The times mentioned are all between 00:00 and 00:59.
#
# Part 1: find the guard that has the most minutes asleep and the minute
#         this guard spends most asleep.
# Part 2: find the guard which is most frequently asleep on the same minute and
#         the minute this guard spends most asleep.q
if __name__ == '__main__':
    if len(sys.argv) != 2:
        sys.exit("usage: ./day04.py INPUT_FILE")
    filename = sys.argv[1]
    if not os.path.exists(filename):
         sys.exit("error: {} does not exist.".format(filename))
    data = open(filename).read().splitlines()
    init_guards_sleep(data)
    print("PART ONE:", strategy_one())
    print("PART TWO:", strategy_two())
