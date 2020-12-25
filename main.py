import sys

from IO import read_assembly_lines
from instructions_identifier import *
from operands_identifier import *

argsNum = len(sys.argv)  # TODO : Checks
# asmFilePath = sys.argv[1]
asmFilePath = 'main.asm'
print(asmFilePath)

assembly_lines = read_assembly_lines(asmFilePath)

IR = []

for line in assembly_lines:
    if line['content'].startswith('DEFINE'):
        handle_variable(IR, line)
        continue
    if line['content'].endswith(':'):
        handle_label(IR, line)
        continue

for line in assembly_lines:
    if line['content'].startswith('DEFINE'):
        continue
    if line['content'].endswith(':'):
        continue

    instruction_type, opcode, op1, op2 = instructions_identifier(line)

    if instruction_type == "1op" or instruction_type == "2op":
        program_counter = len(IR)
        instruction = handle_instruction(program_counter, opcode, op1, op2)
        IR += instruction
        print(line, instruction)
