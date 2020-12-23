import sys
from IO import read_assembly_lines
from instructions_identifier import instructions_identifier, handle_variable

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

    instruction_type, opcode, op1, op2 = instructions_identifier(line)
