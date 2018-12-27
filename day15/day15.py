#!/usr/bin/env python3

import os
import sys

# Input file is a map representing Goblins (G) and Elves (E). The Goblins and
# Elves take turns fighting. During its turn, each unit first move towards the
# closest target then attack it. Each unit has 200 hit points (health) and an
# attack power of 3. The fight ends when one of the two sides has no more units.
# Below is an input example:
#
#                             #######
#                             #.G...#
#                             #...EG#
#                             #.#.#G#
#                             #..G#E#
#                             #.....#
#                             #######
#
# Part 1: find the product between the number of full rounds completed before
#         the combat ends and the sum of the hit points of all remaining units.
# Part 2: find the smallest attack power boost the elves need to win the fight
#         without any losses.
if __name__ == '__main__':
    if len(sys.argv) != 2:
        sys.exit("usage: ./day15.py INPUT_FILE")
    filename = sys.argv[1]
    if not os.path.exists(filename):
         sys.exit("error: {} does not exist.".format(filename))
