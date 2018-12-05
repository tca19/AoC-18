#!/usr/bin/env python3

import os
import re
import sys
import string

# All the reactions that could happen
regex = re.compile("aA|Aa|bB|Bb|cC|Cc|dD|Dd|eE|Ee|fF|Ff|gG|Gg|hH|Hh|iI|Ii|"
                   "jJ|Jj|kK|Kk|lL|Ll|mM|Mm|nN|Nn|oO|Oo|pP|Pp|qQ|Qq|rR|Rr|"
                   "sS|Ss|tT|Tt|uU|Uu|vV|Vv|wW|Ww|xX|Xx|yY|Yy|zZ|Zz")

# Remove all units that react in polymer. Repeat until no more reactions happen
def react(polymer):
    while True:
        reacted = regex.sub('', polymer)
        if reacted == polymer:
            return len(reacted)
        polymer = reacted

# Find the unit type that once removed in the polymer gives the shortest reacted
# polymer. Return the length of the shortest polymer.
def shortest_possible_polymer(polymer):
    possible_lengths = []
    for c in string.ascii_lowercase:
        residue = ''.join([l for l in polymer if l != c and l != c.upper()])
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
