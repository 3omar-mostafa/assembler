from instructions import instructions
from errorHandler import errorHandler


def instructions_identifier(line):

    segments = line['content'].split(',')
    tmp = segments[0].split()
    instruction = tmp[0].strip()
    operand1 = None
    operand2 = None
    opcode = None
    instruction_type = None

    for inst_type in instructions:
        opcode = instructions[inst_type].get(instruction)
        if opcode is not None:
            instruction_type = inst_type
            break

    if len(tmp) > 1:
        operand1 = tmp[1].strip()
        if len(segments) > 1:
            operand2 = segments[1].strip()

    if (
        instruction_type is None or
        instruction_type == 'op2' and operand2 is None or
        instruction_type == 'op1' and operand1 is None or
        (instruction_type == 'branch' or instruction_type == '0op')
        and (operand2 is not None or operand1 is not None)
    ):
        errorHandler(line['number'], line['content'])
    return instruction_type, opcode, operand1, operand2


variables_table = {}


def handle_variable(IR, line):

    segments = line['content'].split()

    if len(segments) < 3 or segments[0] != 'DEFINE' or segments[1][0].isdigit():
        errorHandler(line['number'], line['content'])

    name = segments[1]
    values = ''.join(segments[2:]).split(',')

    if '' in values:
        errorHandler(line['number'], line['content'])

    location = len(IR)
    variables_table[name] = location

    for i in values:
        IR.append(f'{int(i):016b}')

    return
