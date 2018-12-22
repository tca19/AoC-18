#!/usr/bin/env python3

import os
import sys

# Class representing a node in a doubly linked list.
class Node:
    def __init__(self, val):
        self.prev = None
        self.next = None
        self.val  = val

# Insert a new node with value `val` AFTER node `n`. Return the new node.
def insert(n, val): # n <-> m becomes n <-> new <-> m
    new = Node(val)
    new.prev    = n
    new.next    = n.next
    n.next.prev = new
    n.next      = new
    return new

# Move back by `offset` positions from `current` node in the list.
def move_back(current, offset):
    for _ in range(offset):
        current = current.prev
    return current

# Return the score of the wininng player of the marble game. Use a doubly linked
# list to represent the circle where the marbles are inserted.
def winning_score(n_players, n_marbles):
    scores = [0] * n_players
    current_player = 0
    current_node = Node(0)
    current_node.next = current_node
    current_node.prev = current_node
    for m in range(1, n_marbles+1):
        if m%23 == 0:
            scores[current_player] += m
            current_node = move_back(current_node, 7)
            scores[current_player] += current_node.val
            current_node.prev.next = current_node.next # remove current node
            current_node.next.prev = current_node.prev
            current_node = current_node.next
        else:
            current_node = insert(current_node.next, m)
        current_player = (current_player + 1) % n_players
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
