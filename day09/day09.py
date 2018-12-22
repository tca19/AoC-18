#!/usr/bin/env python3

import os
import sys
from collections import deque

# Return the score of the wininng player of the marble game. Use a deque object
# (double ended queue) to represent the circle where the marbles are inserted.
def winning_score(n_players, n_marbles):
    scores = [0] * n_players
    circle = deque([0]) # insert position will always be 0, only rotate deque
    for m in range(1, n_marbles+1):
        if m%23 == 0:
            scores[(m-1) % n_players] += m
            circle.rotate(-7) # move back 7 position = rotate to the left
            scores[(m-1) % n_players] += circle.popleft()
            circle.rotate(1) # move 1 pos to the right to insert AFTER new one
        else:
            circle.rotate(1) # move 1 pos to the right to insert AFTER current
            circle.appendleft(m)
    return max(scores)

# Input file is the number of players and the value of the last marble. The
# players play the marble game. The game consists of inserting in turn the
# marbles (starting with the marble with value 1, then the marble with value 2,
# then 3...) at a specific position into a circle (a list) initialized with the
# marble numbered 0. The insertion position is moved by one unit each turn. When
# the value of the inserted marble is a multiple of 23, its value is added to
# the current player score and the marble which is 7 units behind the insertion
# position is removed and also added to its score. The game ends when the last
# marble is inserted. The winner is the player with the highest score.
#
# Part 1: find the score of the winning elf.
# Part 2: find the score of the winning elf if there are 100x more marbles.
if __name__ == '__main__':
    if len(sys.argv) != 2:
        sys.exit("usage: ./day09.py INPUT_FILE")
    filename = sys.argv[1]
    if not os.path.exists(filename):
         sys.exit("error: {} does not exist.".format(filename))
    # line of input file is like: "X players; last marble is worth Y points"
    line = open(filename).read().split()
    n_players = int(line[0])
    n_marbles = int(line[-2])
    print("PART ONE:", winning_score(n_players, n_marbles))
    print("PART TWO:", winning_score(n_players, n_marbles*100))
