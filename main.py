import argparse

from IO import read_assembly_lines, memory, writeOutput, labels_table
from errorHandler import errorHandler
from instructions_identifier import instructions_identifier, handle_variable
from operands_identifier import handle_instruction
from util import findTwoscomplement

arg_parser = argparse.ArgumentParser(description='PDP-11 Like Assembler')
arg_parser.add_argument("assembly_file", help="Assembly Filename")
arg_parser.add_argument("output_file", help="Output Machine Code Filename")

args = arg_parser.parse_args()

assembly_lines = read_assembly_lines(args.assembly_file)

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
        address_size = 16 - len(opcode)
        offset_binary = format(abs(offset), f'0{address_size}b')

        if offset < 0:
            offset_binary = findTwoscomplement(offset_binary)
        memory[line['range'][0]] = opcode + offset_binary

    elif instruction_type == "jmp":
        label_address = labels_table.get(op1)
        if label_address is None:
            errorHandler(line['number'], line['content'])
        address_size = 16 - len(opcode)
        memory[line['range'][0]] = opcode + \
            format(label_address, f'0{address_size}b')

writeOutput(args.output_file)
