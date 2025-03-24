registers = [0] * 32    # thiss is creaitng a list of 32 integers where all elements are 0 for now

def binary_to_decimal(binary):  # this function converts binary to decimal to store in registers as we cannot perform addition on the strings
    decimal = 0
    for digit in binary:
        decimal = decimal*2 + int(digit)
    return decimal

def decode_instruction(instr):

    opcode = instr[25:]

    if opcode == "0110011": # checks r - type
        funct7 = instr[:7]  # First 7 bits
        rs2 = int(instr[7:12], 2)  # sregister 2 , can also use above function to convert to int
        rs1 = int(instr[12:17], 2)  # sregister 1 , can also use above function to convert to int
        funct3 = instr[17:20]  # funct3
        rd = int(instr[20:25], 2)  # storage register
        opcode = "0110011"

        if funct3 == "000":  # checks for add or subtract as funct3 is same for them both
            if funct7 == "0000000":  # addding
                registers[rd] = registers[rs1] + registers[rs2]
            elif funct7 == "0100000":  # subtraacting
                registers[rd] = registers[rs1] - registers[rs2]
        
        elif funct3 == "111" and funct7 == "0000000":  # and
            registers[rd] = registers[rs1] & registers[rs2]
        
        elif funct3 == "110" and funct7 == "0000000":  # or
            registers[rd] = registers[rs1] | registers[rs2]
        
        elif funct3 == "010" and funct7 == "0000000":  # slt Set Less Than
            if registers[rs1] < registers[rs2]:
                registers[rd] = 1 
            else:
                registers[rd] = 0
        
        elif funct3 == "001" and funct7 == "0000000":  # srl shift right logical
            registers[rd] = registers[rs1] >> (registers[rs2] & 0x1F)


    
    if opcode == "0000011": # checks i - type lw
        for                 # for loop to store values of registrsss bla bla..
    
    if opcode == "0010011": # checks i - type addi
        for                 # for loop to store values of registrsss bla bla..
    
    if opcode == "1100111": # checks i - type jallrdwwd
        for                 # for loop to store values of registrsss bla bla..

    if opcode == "1100011": # checks b - type
        for                 # for loop to store values of registrsss bla bla..
    
    if opcode == "1101111": # checks j - type
        for                 # for loop to store values of registrsss bla bla..
    


#The input file will be in binary format. we will take line by line from function below and put it in decode_instruction function
def run(file_name):
    fil = open(file_name, "r")
    fl = fil.readlines()
    for line in fl:
        decode_instruction(line.strip())
    
    fil.close()