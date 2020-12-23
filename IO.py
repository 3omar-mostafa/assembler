def read_assembly_lines(asmFilePath):
    lines = []
    file = open(asmFilePath)
    for idx, line in enumerate(file):
        line = line.split(';')[0].strip().upper()
        if line != '':
            lines.append({'content': line, 'number': idx + 1})
    return lines
