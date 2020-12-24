import re

X = A = N = r"[0-9]+"
Rn = r"R[0-7]"
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
    "relative_direct": {"regex": fr"{A}", "size": 1, "code": "110"},
    "relative_indirect": {"regex": fr"@{A}", "size": 1, "code": "111"}
}


def get_addressing_mode(operand: str) -> str:
    for addressing_mode in addressing_modes:
        addressing_mode_regex = addressing_modes[addressing_mode].get('regex')

        if re.fullmatch(addressing_mode_regex, operand) is not None:
            return addressing_mode
    raise AttributeError  # if did not match any addressing mode

