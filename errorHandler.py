import sys


def errorHandler(line_number, line_content):
    sys.exit(f'ERROR AT LINE {line_number}: {line_content} \n ABORT...!')
