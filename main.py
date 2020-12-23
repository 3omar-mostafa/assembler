import sys
from IO import read_assembly_lines
from instructions_identifier import instructions_identifier

argsNum = len(sys.argv)  # TODO : Checks
asmFilePath = sys.argv[1]
# asmFilePath = 'main.asm'
print(asmFilePath)

assembly_lines = read_assembly_lines(asmFilePath)


for line in assembly_lines:
    instruction_type, opcode, op1, op2 = instructions_identifier(line)
