from errorHandler import errorHandler
from instructions import INTERRUPT, instructions
import re


def compute_words(line):
    words = 1
    tmp = line.split()
    if tmp[0].startswith("DEFINE"):
        words -= 1

    if len(tmp) > 1 and not tmp[0].startswith(('B', "JSR")):
        tmp = ''.join(tmp[1:]).split(',')
        for op in tmp:
            if op.startswith('#') or op[0].isdigit() or len(op) == 1:
                words += 1
            else:
                container = op
                if container.startswith('@'):
                    container = container.split('@')
                    if len(container) < 2:
                        continue
                    container = ''.join(container[1:])
                if container.endswith('+') or container.startswith('-'):
                    str = re.search(r'\(.*?\)', container).group()
                    l = len(str)
                    if l > 2:
                        container = str[1:l - 1]
                if(not (len(container) == 2 and container[0] == 'R' and container[1].isdigit())):
                    words += 1
    return words


variables_table = {}
labels_table = {}
memory = []


def read_assembly_lines(asmFilePath):
    current_memory_location = 1
    memory_size = 1
    lines = []
    file = open(asmFilePath)
    for idx, line in enumerate(file):
        line = line.split(';')[0].upper()
        line = [l.strip() for l in line.split(':')]

        if(len(line) > 1):
            label = line[0]
            labels_table[label] = current_memory_location
            line = line[1]
        else:
            line = line[0]

        if line != '':

            if line.startswith('.='):
                current_memory_location = int(line.split('.=')[1])
                continue

            first_memory_location = current_memory_location
            current_memory_location += compute_words(line)
            memory_size = max(memory_size, current_memory_location)
            lines.append({'content': line, 'number': idx + 1,
                          'range': (first_memory_location, current_memory_location)})

            if line.startswith('DEFINE'):
                var_name = line.split()
                if len(var_name) < 2:
                    errorHandler(line['number'], line['content'])
                var_name = var_name[1].split(',')[0]
                variables_table[var_name] = first_memory_location

    for i in range(memory_size):
        memory.append("0" * 16)

    int_label = labels_table.get(INTERRUPT['name'])

    if int_label is None:
        memory[0] = instructions["0op"]["IRET"]
    else:
        address_size = 16 - len(INTERRUPT['op'])
        memory[0] = INTERRUPT['op'] + format(int_label, f'0{address_size}b')

    return lines


def writeOutput(filename="out.txt"):

    mem = ["0" * 16] * 2048
    mem[:len(memory)-1] = memory[1:]
    mem[-1] = memory[0]

    with open(filename, 'w') as filehandle:
        filehandle.write('// memory data file (do not edit the following line - required for mem load use)\n// instance=/cpu/spr_alu_ram_modules/u1/ram\n// format=mti addressradix=d dataradix=b version=1.0 wordsperline=1 noaddress\n')
        for listitem in mem:
            filehandle.write('%s\n' % listitem)
