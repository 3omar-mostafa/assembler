import re

from IO import variables_table

N = r"[0-9]+"  # Immediate Value (Number)
X = A = r"([0-9]+|[A-Z][0-9A-Z]*)"  # Address or variable name
Rn = r"R[0-7]"  # Regex for Registers : R0 , R1 ... R7
# Regex for indirect Registers : (R0) , (R1) ... (R7)
Rn_indirect = fr"\({Rn}\)"

addressing_modes = {
    "register_direct": {"regex": fr"{Rn}", "size": 0, "code": "000"},
    "register_indirect": {"regex": fr"@{Rn}|{Rn_indirect}", "size": 0, "code": "001"},

    "auto_increment_direct": {"regex": fr"{Rn_indirect}\+", "size": 0, "code": "010"},
    "auto_increment_indirect": {"regex": fr"@{Rn_indirect}\+", "size": 0, "code": "011"},

    "auto_decrement_direct": {"regex": fr"-{Rn_indirect}", "size": 0, "code": "100"},
    "auto_decrement_indirect": {"regex": fr"@-{Rn_indirect}", "size": 0, "code": "101"},

    "index_direct": {"regex": fr"{X}{Rn_indirect}", "size": 1, "code": "110"},
    "index_indirect": {"regex": fr"@{X}{Rn_indirect}", "size": 1, "code": "111"},

    "immediate": {"regex": fr"#{N}", "size": 1, "code": "010"},
    "absolute": {"regex": fr"@#{A}", "size": 1, "code": "011"},
    "relative_direct": {"regex": fr"{A}", "size": 1, "code": "110"},  # X(PC)
    # @X(PC)
    "relative_indirect": {"regex": fr"@{A}", "size": 1, "code": "111"}
}


def get_addressing_mode(operand: str) -> str:
    for addressing_mode in addressing_modes:
        addressing_mode_regex = addressing_modes[addressing_mode].get('regex')

        if re.fullmatch(addressing_mode_regex, operand) is not None:
            return addressing_mode
    raise AttributeError  # if did not match any addressing mode


def get_register(operand: str) -> str:
    addressing_mode = get_addressing_mode(operand)
    if addressing_mode in ["immediate", "absolute", "relative_direct", "relative_indirect"]:
        register = "R7"
    else:
        register = re.search(Rn, operand).group()
    return register


def get_register_code(register: str) -> str:
    if register is not None:
        return format(int(register[1]), '03b')


def to_16bit_binary(value) -> str:
    value = int(value)
    if value < 0:  # Handle 2's complement
        value = (1 << 16) + value
    return format(value, '016b')


def extract_operand_next_word_value(operand: str) -> str:
    """
    Return Value in the operand other than the register (X or A or N)
    ex. @VAR1(R2) -> VAR1 , #200 -> 200 , @ABC -> ABC
    """
    value = re.split(f'#|@| |{Rn_indirect}', operand)
    return list(filter(None, value))[0]


def get_proper_next_word(program_counter: int, addressing_mode: str, value) -> int:
    value = int(value)
    if addressing_mode.find('relative') != -1:
        value -= (program_counter + 2)
    return value


def handle_instruction(program_counter: int, instruction_opcode: str, operand1: str, operand2: str):
    """
    Returns list of binary strings represents this instruction
    First Element is the instruction
    Next Elements are Data needed (Addresses of Immediate Values) [Optional]
    """

    instructions = [instruction_opcode]

    # TODO : Merge them in function
    if operand1 is not None:
        operand1 = operand1.replace(" ", "")  # Remove white spaces
        reg = get_register_code(get_register(operand1))
        addressing_mode = get_addressing_mode(operand1)
        addressing_mode_code = addressing_modes[addressing_mode].get('code')
        instructions[0] += addressing_mode_code + reg

        if addressing_modes[addressing_mode].get('size') == 1:
            value = extract_operand_next_word_value(operand1)
            if variables_table.get(value) is not None:
                value = variables_table.get(value)
            next_word = get_proper_next_word(
                program_counter, addressing_mode, value)
            instructions.append(to_16bit_binary(next_word))

    if operand2 is not None:
        operand2 = operand2.replace(" ", "")  # Remove white spaces
        reg = get_register_code(get_register(operand2))
        addressing_mode = get_addressing_mode(operand2)
        addressing_mode_code = addressing_modes[addressing_mode].get('code')
        instructions[0] += addressing_mode_code + reg

        if addressing_modes[addressing_mode].get('size') == 1:
            value = extract_operand_next_word_value(operand2)
            if variables_table.get(value) is not None:
                value = variables_table.get(value)
            next_word = get_proper_next_word(
                program_counter, addressing_mode, value)
            instructions.append(to_16bit_binary(next_word))

    return instructions
