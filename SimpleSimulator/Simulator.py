registers = [0] * 32    # thiss is creaitng a list of 32 integers where all elements are 0 for now
memory=[0]*32

def bin_to_dec(binary):  
    decimal = 0
    for digit in binary:
        decimal = decimal*2 + int(digit)
    return decimal

def dec_to_twos(d):
    f=d<0
    d=abs(d)
    s=''
    if f:
        s=dec_to_bin(d)
        s=bin_to_twos(s)
        s='1'*(32-len(s))+s
    else:
        s=dec_to_bin(d)
        s='0'*(32-len(s))+s
        return s

def dec_to_bin(dec):
    s=''
    f= dec<0
    dec=abs(dec)
    while dec>0:
        s+=str(dec%2)
        dec//=2
    s=s[::-1]
    if s=='':
        return '0'

    if f:
        s=bin_to_twos(s)
    return(s)

def bin_to_twos(b):
    b=b.replace('1','2')
    b=b.replace('0','1')
    b=b.replace('2','0')
    f=len(b)
    b=str(bin(int(b,2)+1))
    if len(b)>f+2:
        b=b[3:]
    else:
        b=b[2:]
    b='0'*(f-len(b))+b
    return b

def twos_to_dec(t):
    if t[0]=='1':
        t=bin_to_twos(t)
        return -1*bin_to_dec(t)
    return bin_to_dec(t)

def decode_instruction(instr):
    global flag
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


    if opcode == '0100011':  # S-type sw
        rs1 = int(instr[12:17], 2)
        rs2 = int(instr[7:12], 2)
        funct3 = instr[17:20]
        imm = twos_to_dec(instr[:7] + instr[20:25])  # Combine immediate parts
        addr = registers[rs1] + imm  # Calculate memory address

        if funct3 == '010':  # Store word (sw)
            memory[addr] = registers[rs2]  # Store the value from rs2 into memory


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
            flag=1
            PC=registers[6]+imm
            if PC%2==1:
                PC-=1   # making lsb 1

    if opcode == "1100011": #b-type
        funct3=instr[17:20]
        imm=instr[0]+instr[-8]+instr[1:7]+instr[20:25]        #~Jazl
        imm=twos_to_dec(imm)                                  # for arul to change according to wat he makes
        rs2=instr[7:12]
        rs1=instr[12:17]
        flag=1
        if funct3=="000":
            if rs1==rs2:
                PC+=imm
                if imm==0:
                    PC=0
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
        flag=1
        PC=PC+imm
        if PC%2==1:
            PC-=1
    
    
def printoutput():
    s=''
    s+='0b'+dec_to_twos(PC)
    s+=' '
    rs1='00000'
    while rs1!='11111':
        s+='0b'+dec_to_twos(registers[rs1])
        s+=' '
        rs1=dec_to_bin(bin_to_dec(rs1)+1)
    s+='0b'+dec_to_twos(registers[rs1])
    fh=open("output.txt",'a')
    fh.write(s+'/n')
    fh.close()
    
def memorywrite():
    fh=open('output.txt','a')
    c=0
    for i in memory:
        s="0x000010{}:{}".format(hexa(c),'0b'+dec_to_twos(i))
        fh.write(s+'\n')
        fh.close()
        c+=4
    

def hexa(d):
    h={0:'0',1:'1', 2:'2', 3:'3', 4:'4', 5:'5', 6:'6', 7:'7', 8:'8', 9:'9', 10:'A', 11:'B', 12:'C', 13:'D', 14:'E', 15:'F'}
    r=''
    while d>0:
        r=h[d%16]+r
        d//=16
    r='0'*(2-len(r))
    return r
PC=0
flag=0
totallines=0
def setup(file_name):
    global totallines               #setup function(pc counter etc, add whatever you need to setup) ~ Jazl
    fil = open(file_name, "r")
    fl = fil.readlines()
    totallines=len(fl)
    for i in range(totallines):
        fl[i]=fl[i].strip()
    fil.close()

def run(il):
    global PC
    global flag
    while (PC!=0):
        if flag==0:
            PC+=4
        else:
            flag=0
        decode_instruction(il[PC%4])
        printoutput()
    memorywrite()


setup("D:\CO_Project_Allocated_jan30_2025\CO_Project_Allocated_jan30_2025\SimpleSimulator\simple_2.txt")