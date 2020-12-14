"""CPU functionality."""

import sys
import operations

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256
        self.reg = [0] * 8
        self.pc = 0
        self.num_operands = 0
        self.fl = 0b0

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

    def alu(self, op, reg_a, reg_b=None):
        """ALU operations."""

        alu_operation = operations.alu_opcodes[op]

        if self.num_operands > 1:
            getattr(self, alu_operation)(reg_a, reg_b)
        else:
            getattr(self, alu_operation)(reg_a)

        # else:
        #     raise Exception("Unsupported ALU operation")
    
    def pcs(self, op, register_a=None, register_b=None):

        pc_setter_operation = operations.direct_codes[op]

        if self.num_operands > 1:
            getattr(self, pc_setter_operation)(register_a, register_b)
        elif self.num_operands == 1:
            getattr(self, pc_setter_operation)(register_a)
        else:
            getattr(self, pc_setter_operation)()

    def add(self, register_a, register_b):
        self.reg[register_a] += self.reg[register_b]

    def call(self, register_a):
        subroutine_address = self.reg[register_a]
         
        # push the next PC location
        # get the location of the stack pointer
        # decrement it by one and store the new PC location
        self.reg[7] -= 0x1
        self.ram[self.reg[7]] = self.pc + self.num_operands + 1
        self.pc = subroutine_address

    def cmp(self, register_a, register_b):
        if self.reg[register_a] < self.reg[register_b]:
            self.fl = 0b100
        elif self.reg[register_a] > self.reg[register_b]:
            self.fl = 0b10
        else:
            self.fl = 0b1

    def hlt(self):
        exit()
    
    def jmp(self, register):
        address = self.reg[register]
        self.pc = address
    
    def jeq(self, register):
        if self.fl == 0b1:
            self.jmp(register)
        else:
            self.pc += 2

    def jne(self, register):
        if self.fl != 0b1:
            self.jmp(register)
        else:
            self.pc += 2

    def mul(self, register_a, register_b):
        self.reg[register_a] *= self.reg[register_b]

    def ldi(self, register, immediate):
        self.reg[register] = immediate
    
    def pop(self,register):
        value = self.ram[self.reg[7]]
        self.reg[register] = value
        address = self.reg[7]
        new_address = address + 0x1
        self.reg[7] = new_address
    
    def prn(self, register):
        binary_string = str(self.reg[register])
        print(binary_string)
    
    def push(self, register):
        self.reg[7] -= 0x1
        value = self.reg[register]
        self.ram[self.reg[7]] = value
    
    def ram_read(self, address_to_read):
        # return value stored at address_to_read
        return self.ram[address_to_read]

    def ram_write(self, value_to_write, address_to_write):
        # store value_to_write at address_to_write
        self.ram[address_to_write] = value_to_write
        return
    
    def ret(self):
        self.pc = self.ram[self.reg[7]]
        address = self.reg[7]
        new_address = address + 0x1
        self.reg[7] = new_address


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
        running = True
        test_num = 0

        while running:
            # self.trace()
            instruction = self.ram[self.pc]
            self.num_operands = instruction >> 6
            opertion_code = instruction & 0b00001111
            test_num += 1

            #HLT
            if instruction == 0b00000001:
                self.hlt()

            if self.num_operands > 0:
                operand_a = self.ram[self.pc + 1]
            if self.num_operands > 1:
                operand_b = self.ram[self.pc + 2]

            # ALU Mask
            alu = (instruction >> 5) & 0b001

            # Direct Code Mask
            pc_setters = (instruction >> 4) & 0b0001

            if alu:
                self.alu(opertion_code, operand_a, operand_b)

            elif pc_setters:
                if self.num_operands > 1:
                    self.pcs(opertion_code, operand_a, operand_b)
                elif self.num_operands == 1:
                    self.pcs(opertion_code, operand_a)
                else:
                    self.pcs(opertion_code)
                continue

            else:
                operation = operations.opcodes[opertion_code]
                if self.num_operands > 1:
                    getattr(self, operation)(operand_a, operand_b)
                else:
                    getattr(self, operation)(operand_a)
            
            self.pc += (1 + self.num_operands)