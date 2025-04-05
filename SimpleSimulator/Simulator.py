import sys

registers = [0] * 32
PC = 0x00000000
program_memory = [0] * 64
stack_memory = [0] * 32
registers[2]=380
data_memory = [0] * 32
instructions = []

PROGRAM_BASE = 0x00000000
STACK_BASE = 0x00000100
DATA_BASE = 0x00010000

def binary_to_signed(binary, bits):
    sign = 2 ** (bits - 1)
    complement = 2 ** bits
    if binary & sign:
        return binary - complement
    else:
        return binary
def int_to_twos_complement_32(num):
    if not (-2*31 <= num <= 2*31 - 1): raise ValueError("Out of range")
    return "0b" + (bin(num & 0xFFFFFFFF)[2:].zfill(32) if num >= 0 else bin((~abs(num) & 0xFFFFFFFF) + 1)[2:].zfill(32))

def load_data(binary_file):
    global instructions
    file = open(binary_file, 'r')
    lines = file.readlines()
    file.close()
    instructions = []
    for line in lines:
        stripped_line = line.strip()
        if stripped_line:
            instructions.append(stripped_line)
    if len(instructions) > 64:
        print("Error: Instruction Overflow")
        sys.exit(1)
    for i in range(len(instructions)):
        program_memory[i] = int(instructions[i], 2)

def instruction(instr):
    global PC, registers, stack_memory, data_memory
    opcode = int(instr[25:32], 2)
    print(instr[25:32])
    print(opcode)  # Bits 6-0 (little-endian adjusted to 31-25)
    if opcode == 0b0110011:  # R-type
        func7 = int(instr[0:7], 2)    # Bits 31-25
        rs2 = int(instr[7:12], 2)     # Bits 24-20
        rs1 = int(instr[12:17], 2)    # Bits 19-15
        funct3 = int(instr[17:20], 2) # Bits 14-12
        rd = int(instr[20:25], 2)     # Bits 11-7
        if func7 == 0 and funct3 == 0:  # add
            result = registers[rs1] + registers[rs2]
            print(f"Add: x{rs1}={registers[rs1]}, x{rs2}={registers[rs2]}, x{rd}={result}")
            registers[rd] = result
        elif func7 == 0b0100000 and funct3 == 0b000:  # sub
            registers[rd] = registers[rs1] - registers[rs2]
        elif func7 == 0 and funct3 == 0b010:  # slt
            registers[rd] = 1 if registers[rs1] < registers[rs2] else 0
        elif func7 == 0 and funct3 == 0b101:  # srl
            shift = registers[rs2] & 0x1F
            registers[rd] = registers[rs1] >> shift
        elif func7 == 0 and funct3 == 0b110:  # or
            registers[rd] = registers[rs1] | registers[rs2]
        elif func7 == 0 and funct3 == 0b111:  # and
            registers[rd] = registers[rs1] & registers[rs2]
        if rd == 0:
            registers[0] = 0
        PC += 4
    elif opcode == 0b0010011:  # I-type (addi)
        print(registers[2],'sabari')
        rd = int(instr[20:25], 2)     # Bits 11-7
        rs1 = int(instr[12:17], 2)    # Bits 19-15
        funct3 = int(instr[17:20], 2) # Bits 14-12
        imm = binary_to_signed(int(instr[0:12], 2), 12)  # Bits 31-20
        if funct3 == 0:
            print(f"Addi: x{rd} = x{rs1}({registers[rs1]}) + {imm}")
            registers[rd] = registers[rs1] + imm
            if rd == 0:
                registers[0] = 0
            PC += 4
    elif opcode == 0b1100111:  # I-type (JALR)
        funct3 = int(instr[17:20], 2)  # Bits 14-12
        rd = int(instr[20:25], 2)      # Bits 11-7
        rs1 = int(instr[12:17], 2)     # Bits 19-15
        imm = binary_to_signed(int(instr[0:12], 2), 12)  # Bits 31-20
        if funct3 == 0:  # Only funct3 = 000 for JALR
            old_PC = PC
            PC = (registers[rs1] + imm) & ~1  # LSB = 0 (even address)
            if rd != 0:  # Don’t overwrite x0
                registers[rd] = old_PC + 4
    elif opcode == 0b0000011:  # lw
        rd = int(instr[20:25], 2)
        rs1 = int(instr[12:17], 2)
        funct3 = int(instr[17:20], 2)
        imm = binary_to_signed(int(instr[0:12], 2), 12)
        if funct3 == 0b010:
            addr = registers[rs1] + imm
            if STACK_BASE <= addr < 0x0000017C:
                idx = (addr - STACK_BASE) // 4
                registers[rd] = stack_memory[idx]
            elif DATA_BASE <= addr < 0x0001007C:
                idx = (addr - DATA_BASE) // 4
                registers[rd] = data_memory[idx]
            else:
                print(f"Error: Invalid memory address {hex(addr)} at line {PC // 4}")
                sys.exit(1)
            if rd == 0:
                registers[0] = 0
            PC += 4
    elif opcode == 0b0100011:  # sw
        rs2 = int(instr[7:12], 2)
        rs1 = int(instr[12:17], 2)
        funct3 = int(instr[17:20], 2)
        imm = binary_to_signed(int(instr[0:7] + instr[20:25], 2), 12)
        if funct3 == 0b010:
            addr = registers[rs1] + imm
            if STACK_BASE <= addr < STACK_BASE + 128:
                idx = (addr - STACK_BASE) // 4
                stack_memory[idx] = registers[rs2]
            elif DATA_BASE <= addr < DATA_BASE + 128:
                idx = (addr - DATA_BASE) // 4
                data_memory[idx] = registers[rs2]
            else:
                print(f"Error: Invalid memory address {hex(addr)} at line {PC // 4}")
                sys.exit(1)
            PC += 4
    elif opcode == 0b1100011:  # beq, bne, blt
        rs1 = int(instr[12:17], 2)
        rs2 = int(instr[7:12], 2)
        funct3 = int(instr[17:20], 2)
        imm_bits = instr[0] + instr[24] + instr[1:7] + instr[20:24] + "0"
        imm = binary_to_signed(int(imm_bits, 2), 13)
        if funct3 == 0b000 and registers[rs1] == registers[rs2]:
            PC = PC + imm
        elif funct3 == 0b001 and registers[rs1] != registers[rs2]:
            PC = PC + imm
        elif funct3 == 0b100 and registers[rs1] < registers[rs2]:
            PC = PC + imm
        else:
            PC += 4
    elif opcode == 0b1101111:  # jal
        rd = int(instr[20:25], 2)
        imm_bits = instr[0] + instr[12:20] + instr[11] + instr[1:11] + "0"
        imm = binary_to_signed(int(imm_bits, 2), 21)
        registers[rd] = PC + 4
        PC = PC + imm
        if rd == 0:
            registers[0] = 0         
    else:
        print(f"Error: Unknown opcode {bin(opcode)} at line {PC // 4}")
        sys.exit(1)

def store_registers(out_file):
    file = open(out_file, 'a')
    line = f"0b{PC:032b}"
    for reg in registers:
        line += " "+int_to_twos_complement_32(reg)
    file.write(line.strip() + "\n")
    file.close()

def save_memory(out_file):
    file = open(out_file, 'a')
    for i in range(32):
        addr = DATA_BASE + i * 4
        value = data_memory[i]
        file.write(f"0x{addr:08X}:0b{value:032b}\n")
    file.close()

def simulator_execution(input_file, output_file):
    global registers, PC, program_memory, stack_memory, data_memory, instructions
    registers = [0] * 32
    registers[2]=380
    PC = 0x00000000
    program_memory = [0] * 64
    stack_memory = [0] * 32
    data_memory = [0] * 32
    load_data(input_file)
    with open(output_file, 'w') as file:
        pass



    
    halted = False
    while True:
        if PC < 0 or PC // 4 >= len(instructions):
            print("Error: Program counter out of bounds or missing halt instruction")
            sys.exit(1)
        instr = instructions[PC // 4]
        print(f"PC: 0b{PC:032b}, Executing: {instr}")

        if instr == "00000000000000000000000001100011":
            store_registers(output_file)
            save_memory(output_file)
            halted = True
            break
        print(instr)
        instruction(instr)
        store_registers(output_file)
    if not halted:
        print("Error: Missing Virtual Halt instruction")
        sys.exit(1)

if len(sys.argv) != 3:
    print("Usage: python 1.py <binary_file> <output_file>")
    sys.exit(1)
input_file = sys.argv[1]
output_file = sys.argv[2]    
simulator_execution(input_file, output_file)