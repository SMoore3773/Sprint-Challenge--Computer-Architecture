"""CPU functionality."""

import sys

HLT = 0b00000001
LDI = 0b10000010
PRN = 0b01000111
MUL = 0b10100010
PUSH = 0b01000101
POP = 0b01000110
CALL = 0b01010000
RET = 0b00010001
CMP = 0b10100111
JMP = 0b01010100
JEQ = 0b01010101
JNE = 0b01010110


class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.registers = [0] * 8
        self.registers[7] = 0xF4
        self.pc = 0
        self.ram = [0] * 256
        self.halted = False
        self.sp = self.registers[7]
        self.fl = 0

    def ram_read(self, address):
        return self.ram[address]

    def ram_write(self, value, address):
        self.ram[address] = value

    def load(self, filename):
        """Load a program into memory."""

        address = 0

        # For now, we've just hardcoded a program:

        # program = [
        #     # From print8.ls8
        #     0b10000010,  # LDI R0,8
        #     0b00000000,
        #     0b00001000,
        #     0b01000111,  # PRN R0
        #     0b00000000,
        #     0b00000001,  # HLT
        # ]

        # for instruction in program:
        #     self.ram[address] = instruction
        #     address += 1

        with open(filename) as my_file:
            # parse and get instruction
            for line in my_file:
                # try to get isntruction/ operand in the line
                comment_split = line.split("#")
                possibe_binary_number = comment_split[0]
                try:
                    x = int(possibe_binary_number, 2)
                    self.ram_write(x, address)
                    address += 1
                except:
                    # silent fail of try block
                    continue

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        elif op == MUL:
            self.registers[reg_a] *= self.registers[reg_b]
            self.pc += 3
        
        elif op == CMP:
            if self.registers[reg_a] == self.registers[reg_b]:
                self.fl = self.fl
            elif self.registers[reg_a] > self.registers[reg_b]:
                self.fl = self.fl
            elif self.registers[reg_a] < self.registers[reg_b]:
                self.fl = self.fl

        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            # self.fl,
            # self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def run(self):
        """Run the CPU."""
        while not self.halted:
            instr_to_execute = self.ram_read(self.pc)
            operand_a = self.ram_read(self.pc + 1)
            operand_b = self.ram_read(self.pc + 2)
            self.execute_instr(instr_to_execute, operand_a, operand_b)

    def execute_instr(self, instruction, operand_a, operand_b):
        if instruction == HLT:
            self.halted = True
            self.pc += 1

        elif instruction == PRN:
            print(self.registers[operand_a])
            self.pc += 2

        elif instruction == LDI:
            self.registers[operand_a] = operand_b
            self.pc += 3

        elif instruction == MUL:
            # self.registers[operand_a] = self.registers[operand_a] * self.registers[operand_b]
            self.registers[operand_a] *= self.registers[operand_b]
            self.pc += 3

        elif instruction == PUSH:
            # decrement stack pointer
            self.sp -= 1
            # store the operand in the stack
            self.ram_write(self.registers[operand_a], self.sp)
            # self.ram[self.sp] = self.registers[operand_a]
            self.pc += 2

        elif instruction == POP:
            self.registers[operand_a] = self.ram_read(self.sp)
            # self.registers[operand_a] = self.ram[self.sp]
            self.sp += 1
            self.pc += 2

        elif instruction == CALL:
            self.sp -= 1
            self.ram_write(operand_b, self.sp)
            self.pc = operand_a

        elif instruction == RET:
            self.pc = self.sp
            self.sp += 1

        elif instruction == CMP:
            pass

        elif instruction == JMP:
            pass

        elif instruction == JEQ:
            pass

        elif instruction == JNE:
            pass

        else:
            print("invalid instruction")
            self.halted = True
