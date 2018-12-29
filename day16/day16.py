#!/usr/bin/env python3

import os
import re
import sys

# Return list of Before/instruction/After and program instructions from filename
def parse_data(filename):
    extractor = re.compile("-?\d+")
    groups    = []
    program   = []
    with open(filename) as f:
        for line in f:
            if line == "\n":
                continue
            if "Before" in line:
                # when there is "Before" in a line, two more lines follow
                # containing an instruction and the values in registers After
                before = list(map(int, extractor.findall(line)))
                instruction = list(map(int, extractor.findall(f.readline())))
                after = list(map(int, extractor.findall(f.readline())))
                groups.append((before, instruction, after))
            else:
                instruction = list(map(int, extractor.findall(line)))
                program.append(instruction)

    return groups, program

# Input file has two sections:
#   * the first one is composed of groups of 3 lines like:
#          Before: [3, 2, 1, 1]
#          9 2 1 2
#          After:  [3, 2, 2, 1]
#     They represent the state of 4 registers Before and After an instruction
#     (the middle line) has been run.
#   * the second one is a list of instructions like:
#          10 3 3 3
#          10 0 0 2
#          9 0 0 1
#
# Each instruction has: <op_code> <input_A> <input_B> <output_C>. They do
# different things according to their op_code (some add value A and B and put it
# in register C, others compute the OR between values of registers A and B and
# put result in register C...).
#
# Part 1: with the first section of input, find the number of groups that have
#         at least 3 different op_code that could transform Before into After.
# Part 2: find the op_code of each instruction and the value of register 0 after
#         executing all the instructions of second section of input.
if __name__ == '__main__':
    if len(sys.argv) != 2:
        sys.exit("usage: ./day16.py INPUT_FILE")
    filename = sys.argv[1]
    if not os.path.exists(filename):
         sys.exit("error: {} does not exist.".format(filename))
    groups, program = parse_data(filename)
    print(program)
