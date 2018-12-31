#!/usr/bin/env python3

import os
import re
import sys
from collections import defaultdict

def addr(register, A, B, C):
    new_register = list(register)
    new_register[C] = register[A] + register[B]
    return new_register

def addi(register, A, B, C):
    new_register = list(register)
    new_register[C] = register[A] + B
    return new_register

def mulr(register, A, B, C):
    new_register = list(register)
    new_register[C] = register[A] * register[B]
    return new_register

def muli(register, A, B, C):
    new_register = list(register)
    new_register[C] = register[A] * B
    return new_register

def banr(register, A, B, C):
    new_register = list(register)
    new_register[C] = register[A] & register[B]
    return new_register

def bani(register, A, B, C):
    new_register = list(register)
    new_register[C] = register[A] & B
    return new_register

def borr(register, A, B, C):
    new_register = list(register)
    new_register[C] = register[A] | register[B]
    return new_register

def bori(register, A, B, C):
    new_register = list(register)
    new_register[C] = register[A] | B
    return new_register

def setr(register, A, B, C):
    new_register = list(register)
    new_register[C] = register[A]
    return new_register

def seti(register, A, B, C):
    new_register = list(register)
    new_register[C] = A
    return new_register

def gtir(register, A, B, C):
    new_register = list(register)
    new_register[C] = 1 if A > register[B] else 0
    return new_register

def gtri(register, A, B, C):
    new_register = list(register)
    new_register[C] = 1 if register[A] > B else 0
    return new_register

def gtrr(register, A, B, C):
    new_register = list(register)
    new_register[C] = 1 if register[A] > register[B] else 0
    return new_register

def eqir(register, A, B, C):
    new_register = list(register)
    new_register[C] = 1 if A == register[B] else 0
    return new_register

def eqri(register, A, B, C):
    new_register = list(register)
    new_register[C] = 1 if register[A] == B else 0
    return new_register

def eqrr(register, A, B, C):
    new_register = list(register)
    new_register[C] = 1 if register[A] == register[B] else 0
    return new_register

OPCODES = {"addr": addr, "addi": addi, "mulr": mulr, "muli": muli,
           "banr": banr, "bani": bani, "borr": borr, "bori": bori,
           "setr": setr, "seti": seti, "gtir": gtir, "gtri": gtri,
           "gtrr": gtrr, "eqir": eqir, "eqri": eqri, "eqrr": eqrr}

# Return list of (Before,instruction,After) and program execution instructions
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

# Return the list of opcodes that can transform registers `before` into `after`.
def possible_opcodes(before, instruction, after):
    possible = []
    for opcode, f in OPCODES.items():
        # `instruction` has 4 values (opcode ID, A, B and C)
        opcode_id, A, B, C = instruction
        if f(before, A, B, C) == after:
            possible.append(opcode)
    return possible

# Return the number of groups where the intruction can behave at least like `n`
# different opcode.
def similar_different_opcodes(groups, n=3):
    opcodes_per_group = [possible_opcodes(before, instruction, after)
                         for before, instruction, after in groups]
    return len([1 for ops in opcodes_per_group if len(ops) >= n])

# Return a dict that maps each opcode_id to an operation name.
def find_opcode_mapping(groups):
    # for each opcode (0 to 15), find the list of operations that are possible
    choices = defaultdict(set)
    for before, instruction, after in groups:
        opcode_id, _, _, _ = instruction
        choices[opcode_id].update(possible_opcodes(before, instruction, after))
    mapping = {}
    while len(mapping) < 16: # because 16 possible opcode, run until it's filled
        # find ids which only have 1 possible operation. Put them in the mapping
        # and remove these operations from the choice of other ids
        for id, L in choices.items():
            if len(L) == 1:
                op_name = L.pop()
                # OPCODES associate a str to a function
                mapping[id] = OPCODES[op_name]
                for k, v in choices.items():
                    if op_name in v:
                        v.remove(op_name)
    return mapping

# Run the program instruction, return the value in register 0 after execution.
def run_program(groups, program):
    mapping = find_opcode_mapping(groups)
    registers = [0] * 4
    # `program` is already splitted line by line
    for opcode_id, A, B, C in program:
        # mapping associates an id to a function
        registers = mapping[opcode_id](registers, A, B, C)
    return registers[0]

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
    print("PART ONE:", similar_different_opcodes(groups))
    print("PART TWO:", run_program(groups, program))
