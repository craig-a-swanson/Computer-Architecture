opcodes = {
    0b0 : 'call',
    0b11 : 'iret',
    0b101 : 'jeq',
    0b1010 : 'jge',
    0b111 : 'jgt',
    0b1001 : 'jle',
    0b1000 : 'jlt',
    0b100 : 'jmp',
    0b110 : 'jne',
    0b11 : 'ld',
    0b10 : 'ldi'
}

alu_opcodes = {
    0b0 : 'add',
    0b1000 : 'and',
    0b111 : 'cmp',
    0b110 : 'dec',
    0b11 : 'div',
    0b101 : 'inc',
    0b100 : 'mod',
    0b10 : 'mul',
    0b1001 : 'not',
    0b1010 : 'or',
    0b1100 : 'shl',
    0b1101 : 'shr',
    0b1 : 'sub',
    0b1011 : 'xor'
}

def mul(self, register_a, register_b):
    return register_a * register_b