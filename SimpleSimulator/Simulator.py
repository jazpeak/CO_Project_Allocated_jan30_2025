registers = [0] * 32    # thiss is creaitng a list of 32 integers where all elements are 0 for now
memory=[0]*32
def binary_to_decimal(binary):  # this function converts binary to decimal to store in registers as we cannot perform addition on the strings
    decimal = 0
    for digit in binary:
        decimal = decimal*2 + int(digit)
    return decimal
def decode_instruction(instr):

    opcode = instr[25:]

    if opcode == "0110011": # checks r - type
        funct7 = instr[:7]  
        x=rs2
        y=rs1
        rs2 = int(instr[7:12], 2)  
        rs1 = int(instr[12:17], 2)  
        funct3 = instr[17:20]  # funct3
        rd = int(instr[20:25], 2)  # storage register
        signedrs2=-int(x[1:],2) if x[0]==1 else int(x[1:],2)
        signedrs1=-int(y[1:],2) if y[0]==1 else int(y[1:],2)


        if funct3 == "000":  
            if funct7 == "0000000":  
                registers[rd] = registers[rs1] + registers[rs2]
            elif funct7 == "0100000":  
                registers[rd] = registers[rs1] - registers[rs2]
        
        elif funct3 == "111" and funct7 == "0000000":                   #~Jazl or Soumil
            registers[rd] = registers[rs1] & registers[rs2]
        
        elif funct3 == "110" and funct7 == "0000000":  
            registers[rd] = registers[rs1] | registers[rs2]
        
        elif funct3 == "010" and funct7 == "0000000":  
            if signedrs1 < signedrs2:
                registers[rd] = 1 
            else:
                registers[rd] = 0
        
        elif funct3 == "001" and funct7 == "0000000":  
            registers[rd] = registers[rs1] >> (int(x[-5:],2))


    if opcode == '0100011': #stype sw
        rs1=int(instr[12:17],2)
        rs2=int(instr[7:12],2)
        funct3=instr[17:20]
        imm=twos_to_dec(instr[:7]+instr[20:25])
        addr=registers[rs1]+imm
        
        if funct3=='010':
            memory[addr]=rs2

    #memory is completely wrong change
            



    if opcode == "0000011": #  i - type lw
        imm=twos_to_dec(instr[:12])   # arul to do
        rs1=int(instr[12:17],2)
        funct3=instr[17:20]                                   #~Jazl
        rd=int(instr[20:25],2)
        addr=registers[rs1]+imm

        if funct3=='010':
            registers[rd]=memory[addr]  #sign extend or nah? need to c . update: will do later when output perhaps. stil thinking.
        
    if opcode == "0010011": #  i - type addi
        imm=twos_to_dec(instr[:12])   # arul to do
        rs1=int(instr[12:17],2)
        funct3=instr[17:20]
        rd=int(instr[20:25],2)                                #~ Jazl
        addr=registers[rs1]+imm

        if funct3=="000":
            registers[rd]=registers[rs1]+imm

    if opcode == "1100111": #  i - type jalr
        imm=twos_to_dec(instr[:12])   # arul to do
        rs1=int(instr[12:17],2)
        funct3=instr[17:20]
        rd=int(instr[20:25],2)                                # ~Jazl
        addr=registers[rs1]+imm

        if funct3=="000":
            registers[rd]=PC+4
            PC=registers[6]+imm
            if PC%2==1:
                PC-=1   # making lsb 1

    if opcode == "1100011": #b-type
        funct3=instr[17:20]
        imm=instr[0]+instr[-8]+instr[1:7]+instr[20:25]        #~Jazl
        imm=twos_to_dec(imm)                                  # for arul to change according to wat he makes
        rs2=instr[7:12]
        rs1=instr[12:17]
        if funct3=="000":
            if rs1==rs2:
                PC+=imm
        elif funct3=="001":
            if rs1!=rs2:
                PC+=imm
        else:
            "ERROR: Not a b type function"
    

    
    if opcode == "1101111": # checks j - type
        imm=instr[0]+instr[12:20]+instr[11]+instr[1:11]                 # ~Jazl
        imm=twos_to_dec(imm)                                        # for arul to change as required
        rd=int(instr[20:25],2)                                      # store pc+4 in rd, and PC is increased by immediate, and binary(PC) last digit is made to 0 but subtracting 1
        registers[rd]=PC+4
        PC=PC+imm
        if PC%2==1:
            PC-=1
    
    

PC=0
totallines=0
def setup(file_name):
    global totallines               #setup function(pc counter etc, add whatever you need to setup) ~ Jazl
    fil = open(file_name, "r")
    fl = fil.readlines()
    totallines=len(fl)
    for i in range(totallines):
        fl[i]=fl[i].strip()
    fil.close()
setup("D:\CO_Project_Allocated_jan30_2025\CO_Project_Allocated_jan30_2025\SimpleSimulator\simple_2.txt")