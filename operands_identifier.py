import re

X = A = N = r"[0-9]+"
Rn = r"R[0-7]"  # Regex for Registers : R0 , R1 ... R7
Rn_indirect = fr"\({Rn}\)"  # Regex for indirect Registers : (R0) , (R1) ... (R7)

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
    "relative_direct": {"regex": fr"{A}", "size": 1, "code": "110"},
    "relative_indirect": {"regex": fr"@{A}", "size": 1, "code": "111"}
}


# TODO : Replace Variable Name with its address

def get_addressing_mode(operand: str) -> str:
    for addressing_mode in addressing_modes:
        addressing_mode_regex = addressing_modes[addressing_mode].get('regex')

        if re.fullmatch(addressing_mode_regex, operand) is not None:
            return addressing_mode
    # raise AttributeError  # if did not match any addressing mode


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


def handle_instruction(address: int, instruction_opcode: str, operand1: str, operand2: str):
    """
    Returns list of binary strings represents this instruction
    First Element is the instruction
    Next Elements are Data needed (Addresses of Immediate Values) [Optional]
    """
    instruction = instruction_opcode

    reg1 = reg2 = None
    reg1_addressing_mode = reg2_addressing_mode = None

    if operand1 is not None:
        reg1 = get_register_code(get_register(operand1))
        reg1_addressing_mode = get_addressing_mode(operand1)
        reg1_mode_code = addressing_modes[reg1_addressing_mode].get('code')
        instruction += reg1_mode_code + reg1

    if operand2 is not None:
        reg2 = get_register_code(get_register(operand2))
        reg2_addressing_mode = get_addressing_mode(operand2)
        reg2_mode_code = addressing_modes[reg2_addressing_mode].get('code')
        instruction += reg2_mode_code + reg2

    return [instruction]
