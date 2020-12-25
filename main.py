from errorHandler import errorHandler
from os import write
import sys
from IO import read_assembly_lines, memory, writeOutput, labels_table
from instructions_identifier import instructions_identifier, handle_variable
from operands_identifier import *
from util import findTwoscomplement

argsNum = len(sys.argv)  # TODO : Checks
# asmFilePath = sys.argv[1]
asmFilePath = 'main.asm'
print(asmFilePath)

assembly_lines = read_assembly_lines(asmFilePath)


for line in assembly_lines:

    if line['content'].startswith('DEFINE'):
        handle_variable(line)
        continue

    instruction_type, opcode, op1, op2 = instructions_identifier(line)

    if instruction_type == "1op" or instruction_type == "2op":
        memory_location = line['range']
        instruction = handle_instruction(memory_location[0], opcode, op1, op2)
        if len(instruction) > memory_location[1] - memory_location[0]:
            errorHandler(line['number'], line['content'])
        memory[memory_location[0]:memory_location[1]] = instruction

    elif instruction_type == "0op":
        memory[line['range'][0]] = opcode

    elif instruction_type == "branch":
        label_address = labels_table.get(op1)
        if label_address is None:
            errorHandler(line['number'], line['content'])
        offset = label_address - line['range'][1]
        offset_binary = f'{abs(offset):08b}'

        if offset < 0:
            offset_binary = findTwoscomplement(offset_binary)
        memory[line['range'][0]] = opcode + offset_binary

    elif instruction_type == "jmp":
        label_address = labels_table.get(op1)
        if label_address is None:
            errorHandler(line['number'], line['content'])
        memory[line['range'][0]] = opcode + f'{label_address:011b}'
writeOutput()
