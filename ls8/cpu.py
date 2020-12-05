"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256
        self.reg = [0] * 8
        self.pc = 0

        self.reg[7] = 0xf4

    def load(self):
        """Load a program into memory."""
        try:
            if len(sys.argv) < 2:
                print(f'Error from {sys.argv[0]}: missing filename argument')
                print(f'Usage: python3 {sys.argv[0]} <somefilename>')
                sys.exit(1)


            # add a counter that adds to memory at that index
            address = 0

            with open(sys.argv[1]) as f:
                for line in f:
                        split_line = line.split("#")[0]
                        stripped_split_line = split_line.strip()

                        if stripped_split_line != "":
                            command = int(stripped_split_line, 2)
                            
                            # load command into memory
                            self.ram[address] = command

                            address += 1

        except FileNotFoundError:
            print(f'Error from {sys.argv[0]}: {sys.argv[1]} not found')
            print("(Did you double check the file name?)")
            exit()

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        #elif op == "SUB": etc
        else:
            raise Exception("Unsupported ALU operation")

    def hlt(self):
        exit()

    def ldi(self, register, immediate):
        self.reg[register] = immediate
        return
    
    def prn(self, register):
        binary_string = str(self.reg[register])
        # int_value = (int(binary_string, 2))
        # print(int_value)
        print(binary_string)
        return
    
    def ram_read(self, address_to_read):
        # return value stored at address_to_read
        return self.ram[address_to_read]

    def ram_write(self, value_to_write, address_to_write):
        # store value_to_write at address_to_write
        self.ram[address_to_write] = value_to_write
        return

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            #self.fl,
            #self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def run(self):
        """Run the CPU."""
        ir = 0 # a copy of the currently executing instruction
        operand_a = 0
        operand_b = 0
        # read the address in pc and store the result in ir.
        # using ram_read(), read PC+1 and PC+2 from RAM into
        # the variable operand_a and operand_b
        # then depending on the value of opcode, perform action.

        running = True

        while running:
            # self.trace()
            instruction = self.ram[self.pc]

            if instruction == 0b00000001:
                self.hlt()

            elif instruction == 0b10000010:
                ir = instruction
                operand_a = self.ram[self.pc + 1]
                operand_b = self.ram[self.pc + 2]
                self.ldi(operand_a, operand_b)
                self.pc += 3
            
            elif instruction == 0b01000111:
                ir = instruction
                operand_a = self.ram[self.pc + 1]
                self.prn(operand_a)
                self.pc +=2


# NOTE
# 10100000 >> 6  # results in the left two digits, 10
# 160 >> 6 # equals 2
# number_of_operands = command >> 6
# pc += (1 + number_of_operands)
#                                   v
# to get a digit in the middle: 0b11100000
#first shift right by five
# then do masking with &
# 0b11100000 >> 5
# 0b111 & 001 = 001   so we know our digit is a one.