#!/usr/bin/env python3

import os
import sys

# Return the structure of the tree as a dict (metadata and child for each node)
def parse(data):
    # each node starts with 2 information: number of child, number of metadata.
    n_child = next(data) # data is an iterator, get the first 2 values
    n_meta  = next(data)
    # the following data represent the child of this node. They follow the same
    # structure so call recursively the parse function. Since the `data`
    # argument is an iterator, each next() call will modify it so the next call
    # will operate on a modified (i.e. reduced) version of `data`.
    child = [parse(data) for n in range(n_child)]
    # the following info is the list of metadata of this node.
    metadata = [next(data) for m in range(n_meta)]
    return {"child": child, "metadata": metadata}

# Return the sum of metadata of all nodes (including child of node)
def sum_metadatas(node):
    return sum(node["metadata"]) + sum(sum_metadatas(c) for c in node["child"])

# Return the value of node.
def node_value(node):
    # if node has no child, return the sum of its metadata.
    if not node["child"]:
        return sum(node["metadata"])
    # otherwise, consider the metadata as child indexes and return the sum
    # of values of child referenced by the metadata entries. If the index is not
    # valid, skip it. A metadata entry of 1 corresponds to the first child (so
    # use index-1).
    return sum(node_value(node["child"][i-1]) for i in node["metadata"]
               if i-1 in range(len(node["child"])))

# Input file is a list of integers, all on one line. They represent a tree
# structure, composed of nodes. Each node has a list of metadata and a list of
# childs (which can be empty). For each node, its information are grouped as:
# <number_of child> <number_of_metadata> [list of child nodes] [metadata].
# Each node in the [list of child nodes] follows the same structure.
#
# Part 1: find the sum of all metadata in the tree.
# Part 2: find the value of the root node. The value of a node is either the sum
#         of its metadata if it has no child, or the sum of the values of its
#         child nodes whose indexes are those of the metadata otherwise.
if __name__ == '__main__':
    if len(sys.argv) != 2:
        sys.exit("usage: ./day08.py INPUT_FILE")
    filename = sys.argv[1]
    if not os.path.exists(filename):
         sys.exit("error: {} does not exist.".format(filename))
    data = list(map(int, open(filename).read().split()))
    tree = parse(iter(data))
    print("PART ONE:", sum_metadatas(tree))
    print("PART TWO:", node_value(tree))
