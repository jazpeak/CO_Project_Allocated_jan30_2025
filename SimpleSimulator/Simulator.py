import sys
import os

registers = [0] * 32    # this is creating a list of 32 integers where all elements are 0 for now
registers[2] = 380      # this is the stack pointer, so it is set to 380 for now.
memory = [0] * 32
stack=[0]*32
program=[0]*64

def bin_to_dec(binary):  
    decimal = 0
    for digit in binary:
        decimal = decimal * 2 + int(digit)
    return decimal

def dec_to_twos(d):
    f = d < 0
    d = abs(d)
    s = ''
    if f:
        s = dec_to_bin(d)
        s = bin_to_twos(s)
        s = '1' * (32 - len(s)) + s
    else:
        s = dec_to_bin(d)
        s = '0' * (32 - len(s)) + s
    return s

def dec_to_bin(dec):
    s = ''
    f = dec < 0
    dec = abs(dec)
    while dec > 0:
        s += str(dec % 2)
        dec //= 2
    s = s[::-1]
    if s == '':
        return '0'
    if f:
        s = bin_to_twos(s)
    return s

def bin_to_twos(b):
    b = b.replace('1', '2')
    b = b.replace('0', '1')
    b = b.replace('2', '0')
    f = len(b)
    b = str(bin(int(b, 2) + 1))
    if len(b) > f + 2:
        b = b[3:]
    else:
        b = b[2:]
    b = '0' * (f - len(b)) + b
    return b

def dec_to_hex(n):
    return hex(n)

def twos_to_dec(t):
    if t[0] == '1':
        t = bin_to_twos(t)
        return -1 * bin_to_dec(t)
    return bin_to_dec(t)

def hexa(d):
    h = {0:'0', 1:'1', 2:'2', 3:'3', 4:'4', 5:'5', 6:'6', 7:'7', 8:'8', 9:'9', 10:'A', 11:'B', 12:'C', 13:'D', 14:'E', 15:'F'}
    r = ''
    while d > 0:
        r = h[d % 16] + r
        d //= 16
    r = '0' * (2 - len(r)) + r
    return r

PC = 0
flag = 0
jazl = 0
totallines = 0

def decode_instruction(instr):
    global jazl
    global flag
    global PC
    opcode = instr[-7:]
    if opcode == "0110011": #R-type
        funct7 = instr[:7]  
        rs2 = int(instr[7:12], 2)  
        rs1 = int(instr[12:17], 2)  
        x = instr[7:12]
        y = instr[12:17]
        funct3 = instr[17:20]  
        rd = int(instr[20:25], 2)  
        signedrs1 = registers[rs1]
        signedrs2 = registers[rs2]
        if funct3 == "000":  
            if funct7 == "0000000":  
                registers[rd] = registers[rs1] + registers[rs2]
            elif funct7 == "0100000":  
                registers[rd] = registers[rs1] - registers[rs2]
        
        elif funct3 == "111" and funct7 == "0000000":  
            registers[rd] = registers[rs1] & registers[rs2]
        
        elif funct3 == "110" and funct7 == "0000000":  
            registers[rd] = registers[rs1] | registers[rs2]
        
        elif funct3 == "010" and funct7 == "0000000":  
            if signedrs1 < signedrs2:
                registers[rd] = 1 
            else:
                registers[rd] = 0
        
        elif funct3 == "101" and funct7 == "0000000":  
            registers[rd] = registers[rs1] >> (registers[rs2] & 0x1F)


    if opcode == '0100011':  #sw
        rs1 = int(instr[12:17], 2)
        rs2 = int(instr[7:12], 2)
        funct3 = instr[17:20]
        imm = twos_to_dec(instr[:7] + instr[20:25])
        base_addr = registers[rs1]  

        addr = base_addr + imm  

        

        if 0x00000100 <= addr <= 0x0000017C:  # Stack Memory
            if addr % 4 == 0:
                index = (addr - 0x00000100) // 4  
                if funct3 == '010':  # sw
                    stack[index] = registers[rs2]
            else:
                print(f"Error: Misaligned address {hex(addr)} for sw in stack memory")

        elif 0x00010000 <= addr <= 0x0001007C:  # Data Memory
            if addr % 4 == 0:
                index = (addr - 0x00010000) // 4  
                if funct3 == '010':  # sw
                    memory[index] = registers[rs2]
            else:
                print(f"Error: Misaligned address {hex(addr)} for sw in data memory")
        elif 0x00000000 <= addr <= 0x000000FF: # program memory
            if addr % 4 == 0:
                index = (addr - 0x00010000) // 4  
                if funct3 == '010':  # sw
                    program[index] = registers[rs2]
            else:
                print(f"Error: Misaligned address {hex(addr)} for sw in data memory")
        
        else:
            print(f"Error: Address {hex(addr)} out of range for sw")


    if opcode == "0000011":  #LW 
        imm = twos_to_dec(instr[:12])  
        rs1 = int(instr[12:17], 2)  
        funct3 = instr[17:20]
        rd = int(instr[20:25], 2)  

        base_addr = registers[rs1]  
        addr = base_addr + imm  

        if 0x00000100 <= addr <= 0x0000017C:  
            if addr % 4 == 0:
                index = (addr - 0x00000100) // 4  
                if funct3 == '010':  
                    registers[rd] = stack[index]
            else:
                print(f"Error: Misaligned address {hex(addr)} for lw in stack memory")

        elif 0x00010000 <= addr <= 0x0001007C:  
            if addr % 4 == 0:
                index = (addr - 0x00010000) // 4  
                if funct3 == '010':  
                    registers[rd] = memory[index]
            else:
                print(f"Error: Misaligned address {hex(addr)} for lw in data memory")
        elif 0x00000000 <= addr <= 0x000000FF:
            if addr % 4 == 0:
                index = (addr - 0x00010000) // 4  
                if funct3 == '010':  
                    registers[rd] = program[index]
            else:
                print(f"Error: Misaligned address {hex(addr)} for lw in data memory")

        
        else:
            print(f"Error: Address {hex(addr)} out of range for lw")
  
    if opcode == "0010011": #addi
        imm = twos_to_dec(instr[:12])
        rs1 = int(instr[12:17], 2)
        funct3 = instr[17:20]
        rd = int(instr[20:25], 2) 
        addr = rs1 + imm
        
        if funct3 == "000":
            registers[rd] = registers[rs1] + imm

    if opcode == "1100111": #jalr
        imm = twos_to_dec(instr[:12])
        rs1 = int(instr[12:17], 2)
        funct3 = instr[17:20]
        rd = int(instr[20:25], 2)

        if funct3 == "000":
            temp=PC
            flag = 1
            PC = (registers[rs1] + imm) & ~1 
            if rd!=0:
                registers[rd] = temp + 4
    if opcode == "0010011":  
        imm = twos_to_dec(instr[:12])  
        rs1 = int(instr[12:17], 2)  
        funct3 = instr[17:20]
        rd = int(instr[20:25], 2)  

        if funct3 == "011":  
            if (registers[rs1] & 0xFFFFFFFF) < (imm & 0xFFFFFFFF): 
                registers[rd] = 1
            else:
                registers[rd] = 0
    



    if opcode == "1100011": # B-type
        funct3 = instr[17:20]
        imm = instr[0] +instr[24] + instr[1:7] + instr[20:24] + '0'  
        imm = twos_to_dec(imm)
        rs2 = int(instr[7:12], 2)
        rs1 = int(instr[12:17], 2)
        
        if funct3 == "000": 
            if registers[rs1] == registers[rs2]:
                flag = 1
                PC += imm
                if imm == 0:  
                    jazl = 1
        elif funct3 == "001":  
            if registers[rs1] != registers[rs2]:
                flag = 1
                PC += imm
        elif funct3=="100":
            if registers[rs1] < registers[rs2]:
                flag = 1
                PC += imm  #blt
        elif funct3=="110":
            if registers[rs1] & 0xFFFFFFFF < registers[rs2] & 0xFFFFFFFF:  
                flag = 1
                PC += imm #bltu
        else:   
            print("ERROR: Not a B-type function")

    if opcode == "1101111":  #JAL
        imm = instr[0] + instr[12:20] + instr[11] + instr[1:11]  
        imm = twos_to_dec(imm) << 1  
        rd = int(instr[20:25], 2)

        registers[rd] = PC + 4  
        flag = 1  
        PC = PC + imm  


    if opcode == '0010111': #u-auipc
        imm=twos_to_dec(instr[0:20])
        rd=int(instr[20:25],2)
        registers[rd]=PC+(imm << 12)
         
    if opcode == '0110111': #u-lui
        imm=twos_to_dec(instr[0:20],2)
        rd=int(instr[20:25],2)
        registers[rd]=imm << 12

    if opcode=='0110011': #r-sll
        if funct3=='001':
            rd=int(instr[20:25],2)          
            rs1=int(instr[12:17],2)         
            rs2=int(instr[7:12],2)
            registers[rd]=registers[rs1]<<(registers[rs2]%32)

        elif funct3=='100':
            rd=int(instr[20:25],2)   
            rs1=int(instr[12:17],2)  
            rs2=int(instr[7:12],2)   
            registers[rd]=registers[rs1]^registers[rs2]

    if opcode=='1100011' and instr[17:20]=='111':  #b-bgeu
        rs1=int(instr[12:17],2)  
        rs2=int(instr[7:12],2)   
        imm=instr[31]+instr[7]+instr[25:31]+instr[8:12]  
        imm=twos_to_dec(imm)<<1  
        if registers[rs1]>=registers[rs2]:
            PC+=imm
        else:
            PC+=4

    if opcode == "1100000":  # (bonus)
        rd = int(instr[20:25], 2)
        funct3 = instr[17:20]
        rs2 = int(instr[7:12], 2)
        rs1 = int(instr[12:17], 2)
        if funct3 == "000":
            registers[rd] = registers[rs1] * registers[rs2]
        if funct3 == "001":
            for i in range(32):
                registers[i] = 0
        if funct3 == "010":
            print("Halting Execution...")
            jazl = 1
        if funct3 == "011":
            registers[rd] = int(dec_to_bin(registers[rs1])[-1], 2)

def fileInput(file_name):
    global totallines
    with open(file_name, "r") as fil:  
        fl = [line.strip() for line in fil.readlines()]  
        totallines = len(fl)
    return fl

def fileOutput(trace_file):
    os.makedirs(os.path.dirname(trace_file) or '.', exist_ok=True)

    s = '0b' + dec_to_twos(PC) + ' ' + ' '.join('0b' + dec_to_twos(reg) for reg in registers)
    with open(trace_file, 'a') as fh:
        fh.write(s + '\n')

def write_memory_to_trace(trace_file):
    c = 0
    with open(trace_file, 'a') as fh:
        for i in range(32):
            s = f"0x000100{hexa(c)}:0b{dec_to_twos(memory[i])}"
            fh.write(s + '\n')
            c += 4

def run():
    global PC
    global jazl
    global flag
    with open(trace_file_path, 'w') as fh:
        fh.write('')
    MAX_ITERATIONS = 1000  
    iteration_count = 0

    while jazl == 0: 
        if(iteration_count==MAX_ITERATIONS):
            break    
        decode_instruction(il[(PC // 4)])
        if flag == 0:
            PC += 4
        else:
            flag = 0
        fileOutput(trace_file_path)
        iteration_count += 1
    
    write_memory_to_trace(trace_file_path)

if len(sys.argv) != 4:  
    sys.exit(1)

input_file_path = sys.argv[1]
trace_file_path = sys.argv[2] 

if not os.path.isfile(input_file_path):
    print(f"Error: Input file '{input_file_path}' not found.")
    sys.exit(1)

try:
    il = fileInput(input_file_path)
    run()
    print(f"Assembly code processed successfully. Output written to {trace_file_path}")
except FileNotFoundError:
    print(f"Error: Input file '{input_file_path}' not found.")
except Exception as e:
    print(f"An unexpected error occurred: {e}")