#!/usr/bin/env python3

import os
import sys
import string

# Remove all units causing a reaction in polymer (see line 30)
def react(polymer):
    stack = [polymer[0]]
    for c in polymer[1:]:
        if not stack: # is empty? (faster than len(stack) == 0 or stack == [])
            stack.append(c)
        elif c.lower() == stack[-1].lower() and c != stack[-1]:
            stack.pop()
        else:
            stack.append(c)
    return len(stack)

# Find the unit type that once removed in the polymer gives the shortest reacted
# polymer. Return the length of the shortest polymer.
def shortest_possible_polymer(polymer):
    possible_lengths = []
    for c in string.ascii_lowercase:
        residue = polymer.replace(c, '').replace(c.upper(), '')
        possible_lengths.append(react(residue))
    return min(possible_lengths)

# Input file is a long string representing a polymer ("wNnJZzjXxlLrWwbBaA...").
#
# Part 1: when two consecutive same letters have different case (like Aa or bB),
#         they react and disappear. Find the length of the polymer after all
#         reactions have taken place.
# Part 2: find the unit type (a or b or c or ...) that once removed in the
#         polymer will give the shortest polymer after all reactions has
#         happened in the remaining polymer. Find the length of this shortest
#         polymer.
if __name__ == '__main__':
    if len(sys.argv) != 2:
        sys.exit("usage: ./day05.py INPUT_FILE")
    filename = sys.argv[1]
    if not os.path.exists(filename):
         sys.exit("error: {} does not exist.".format(filename))
    polymer = open(filename).read().strip()
    print("PART ONE:", react(polymer))
    print("PART TWO:", shortest_possible_polymer(polymer))
