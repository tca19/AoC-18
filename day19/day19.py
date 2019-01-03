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

# Run the program instructions until the instruction pointer points outside the
# instructions list. Use the `bounded_register` as the instruction pointer.
# Return the value of register 0 at the end of the program.
def run_program(instructions, bounded_register):
    registers = [0] * 6
    ip = 0 # instruction pointer
    while ip < len(instructions):
        registers[bounded_register] = ip
        name, A, B, C = instructions[ip].split()
        A, B, C = int(A), int(B), int(C)
        registers = OPCODES[name](registers, A, B, C)
        ip = registers[bounded_register]
        ip += 1
    return registers[0]

# Input file is composed of assembly instructions such as "mulr 2 5 3" (one per
# line) which simulate a program.
# Each instruction has: <op_code> <input_A> <input_B> <output_C>. They do
# different things according to their op_code (some add value A and B and put it
# in register C, others compute the OR between values of registers A and B and
# put result in register C...).
# The program also has 6 registers (initialized to 0).
#
# The order of the instructions execution is not deterministic, but is
# determined by an instruction pointer (the index of the instruction to run)
# which is bounded to a register. So when the value of that register is
# modified, so is the order. The first line of the input file indicates to which
# register the instruction pointer is bounded (line is like "#ip 4").
#
# Part 1: find the value in register 0 after the program execution.
# Part 2: find the value in register 0 after the program execution if register 0
#         starts with the value 1.
if __name__ == '__main__':
    if len(sys.argv) != 2:
        sys.exit("usage: ./day19.py INPUT_FILE")
    filename = sys.argv[1]
    if not os.path.exists(filename):
        sys.exit("error: {} does not exist.".format(filename))
    instructions = open(filename).read().splitlines()
    bounded_registers = int(instructions[0].split()[1])
    instructions = instructions[1:]
    print("PART ONE:", run_program(instructions, bounded_registers))
