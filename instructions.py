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
        "INV": "1001000010",
        "LSR": "1001000011",
        "ROR": "1001000100",
        "ASR": "1001000101",
        "LSL": "1001000110",
        "ROL": "1001000111",
        "CLR": "1001001000"
    },
    "branch": {
        "BR": "10100000",
        "BEQ": "10100001",
        "BNE": "10100010",
        "BLO": "10100011",
        "BLS": "10100100",
        "BHI": "10100101",
        "BHS": "10100110",
    },

    "0op": {
        "HLT": "1011000000000000",
        "NOP": "1011100000000000",
        "RTS": "1101000000000000",
        "IRET": "1111000000000000"
    },
    "jmp":
    {
        "JSR": "1100",
    }

}

INTERRUPT = {
    "op": "1110",
    "name": "INTERRUPT"
}
