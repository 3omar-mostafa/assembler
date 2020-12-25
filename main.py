from os import write
import sys
from IO import read_assembly_lines, variables_table, labels_table, memory, writeOutput
from instructions_identifier import instructions_identifier, handle_variable

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


print(variables_table)
print(labels_table)
writeOutput()
