#!/usr/bin/env python3

import os
import re
import sys

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

# Input file is a long string representing a polymer ("wNnJZzjXxlLrWwbBaA...").
#
# Part 1: when two consecutive same letters have different case (like Aa or bB),
#         they react and disappear. Find the length of the polymer after all
#         reactions have taken place.
if __name__ == '__main__':
    if len(sys.argv) != 2:
        sys.exit("usage: ./day05.py INPUT_FILE")
    filename = sys.argv[1]
    if not os.path.exists(filename):
         sys.exit("error: {} does not exist.".format(filename))
    polymer = open(filename).read().strip()
    print("PART ONE:", react(polymer))
