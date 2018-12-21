#!/usr/bin/env python3

import os
import sys
from copy import deepcopy
from collections import defaultdict

# Read filename, return 2 dicts: one to know the following steps of a step, the
# other one to know the preceding steps (= the requirements) of a step.
def parse(filename):
    following = defaultdict(set)
    preceding = defaultdict(set)
    for line in open(filename).read().splitlines():
        line = line.strip().split()
        # line is like "Step T must be finished before step C can begin."
        # so the important information are line[1] and line[-3].
        following[line[1]].add(line[-3])
        preceding[line[-3]].add(line[1])
    return following, preceding

# Return the order and execution time of all tasks (n_workers are available)
def completion_order_and_time(following, preceding, n_workers=1):
    preceding = deepcopy(preceding) # copy to not alter original one
    # stack is the list of steps which can start without requiring other steps
    stack      = set(following.keys()) - set.union(*following.values())
    order      = ""
    doing      = [None] * n_workers # what the worker #i is doing
    time_left  = [0] * n_workers    # time the worker #i needs to complete task
    total_time = 0
    while len(stack) > 0 or sum(time_left) > 0:
        # start as much as possible available tasks
        stack = sorted(stack, reverse=True)
        for i in range(n_workers):
            if not stack: # test if stack is empty. If yes, no more tasks to add
                break
            if doing[i] is None: # worker #i is free, give him a task
                task = stack.pop()
                doing[i]     = task
                time_left[i] = ord(task) - 4 # ord(task) - ord("A") + 1 + 60

        # find the next completed task (and the time required to complete it)
        d, pos = min((T,idx) for idx,T in enumerate(time_left) if T > 0)
        order += doing[pos]
        total_time += d

        # `d` seconds have elapsed (so running tasks have progressed)
        for i in range(n_workers):
            if time_left[i] > 0:
                time_left[i] -= d

        # task is done, remove it from the requirements of its following tasks.
        # if this was the last requirement, add the following task to stack.
        for next in following[doing[pos]]:
            preceding[next].remove(doing[pos])
            if len(preceding[next]) == 0:
                stack.append(next)

        # mark task as done
        doing[pos] = None
        time_left[pos] = 0

    return order, total_time

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
    following, preceding = parse(filename)
    print("PART ONE:", completion_order_and_time(following, preceding)[0])
    print("PART TWO:", completion_order_and_time(following, preceding, 5)[1])
