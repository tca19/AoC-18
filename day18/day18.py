#!/usr/bin/env python3

import os
import sys

# Input file represents a grid (50 acres by 50 acres) where each square can be
# either open ground ("."), trees ("|") or a lumberyard ("#"). At each minute,
# each square can change according to its environment: open ground can become
# trees, trees can become lumberyards and lumberyards can become open ground.
#
# Part 1: find the product between the number of trees and lumberyards in the
#         grid after 10 minutes.
# Part 2: find the product between the number of trees and lumberyards in the
#         grid after 1000000000 minutes.
if __name__ == '__main__':
    if len(sys.argv) != 2:
        sys.exit("usage: ./day18.py INPUT_FILE")
    filename = sys.argv[1]
    if not os.path.exists(filename):
         sys.exit("error: {} does not exist.".format(filename))
