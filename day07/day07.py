#!/usr/bin/env python3

import os
import sys
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

# Return the order in which the tasks should be completed.
def completion_order(following, preceding):
    # find the roots (= the tasks which can start without requiring other tasks)
    all_tasks = set()
    for k, v in following.items():
        all_tasks.add(k)
        all_tasks.update(v)
    roots = all_tasks - set.union(*following.values())
    steps_order = ""
    done = set()
    available = roots
    while len(done) < len(all_tasks):
        cur_task = sorted(list(available), reverse=True).pop()
        steps_order += cur_task
        done.add(cur_task)
        available.remove(cur_task)
        # remove cur_task from the task that needed it
        for required in preceding.values():
            if cur_task in required:
                required.remove(cur_task)
        # for all the task following cur_task, put the ones not done and which
        # don't need any other requirements into the available stack
        for next in following[cur_task]:
            if next not in done and len(preceding[next]) == 0:
                available.add(next)
    return steps_order

# Return the time needed to complete all steps if mutiple workers are available.
def completion_time(following, preceding):
    # stack is the list of steps which can start without requiring other steps
    done, stack = set(), set(following.keys()) - set.union(*following.values())
    n_workers   = 5
    doing       = [None for _ in range(n_workers)] # what the worker #i is doing
    time_left   = [0 for _ in range(n_workers)]    # time to complete its task
    total_time  = 0
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
        done.add(doing[pos])
        total_time += d

        # suppose `d` seconds have happened (so running tasks have progressed)
        for i in range(n_workers):
            if time_left[i] > 0:
                time_left[i] -= d

        # task is done, remove it from the requirements of its following tasks.
        # if it was the last requirement, add the following task to stack.
        for next in following[doing[pos]]:
            preceding[next].remove(doing[pos])
            if len(preceding[next]) == 0:
                stack.append(next)

        # mark task as done
        doing[pos] = None
        time_left[pos] = 0

    return total_time

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
    print("PART ONE:", completion_order(following, preceding))
    following, preceding = parse(filename)
    print("PART TWO:", completion_time(following, preceding))
