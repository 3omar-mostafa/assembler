def read_assembly_lines(asmFilePath):
    lines = []
    file = open(asmFilePath)
    for idx, line in enumerate(file):
        line = line.split(';')[0].upper()
        line = [l.strip() for l in line.split(':')]
        if(len(line) > 1):
            lines.append({'content': line[0] + ':', 'number': idx + 1})
            line = line[1]
        else:
            line = line[0]

        if line != '':
            lines.append({'content': line, 'number': idx + 1})

    return lines
