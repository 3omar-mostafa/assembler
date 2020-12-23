import sys

instructions = {
    "2op": {
        "ADD": "0000",
        "SUB": "0001",
        "ADC": "0010",
        "SBC": "0011",
        "AND": "0100",
        "OR": "0101",
        "XOR": "0110",
        "CMP": "0111",
        "MOV": "1000"
    },
    "1op": {
        "INC": "1001000000",
        "DEC": "1001000001",
        "CLR": "1001000010",
        "INV": "1001000011",
        "LSR": "1001000100",
        "ROR": "1001000101",
        "ASR": "1001000110",
        "LSL": "1001000111",
        "ROL": "1001001000"
    },
    "branch": {
        "BR": "10100000",
        "BEQ": "10100001",
        "BNE": "10100010",
        "BLO": "10100011",
        "BLS": "10100100",
        "BHI": "10100101",
        "BHS": "10100110"
    },
    "0op": {
        "HLT": "1011000000000000",
        "NOP": "1011000000000001"
    }
}

argsNum = len(sys.argv)  # TODO : Checks
asmFileName = sys.argv[1]
print(asmFileName)


def read_assembly_lines():
    temp_lines = open(asmFileName, "r").readlines()
    lines = []
    for line in temp_lines:
        line = line.upper()
        line = line.split(';')[0]
        line = line.strip()
        if line != '':
            lines.append(line)
    return lines


def decode(instruction: str, operand1: str, operand2: str):
    instruction_type = None
    opcode = None
    for inst_type in instructions:
        opcode = instructions[inst_type].get(instruction)
        if opcode is not None:
            instruction_type = inst_type
            break


assembly_lines = read_assembly_lines()

for line in assembly_lines:
    line = line.split(',')
    tmp = line[0].split()
    instruction = tmp[0].strip()
    operand1 = operand2 = ''
    if len(tmp) > 1:
        operand1 = tmp[1].strip()
        if len(line) > 1:
            operand2 = line[1].strip()
    decode(instruction, operand1, operand2)
