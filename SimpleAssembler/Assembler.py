import re
from re import split


testCaseFiles = {"SimpleGen": ["Ex_test_0.txt", "Ex_test_1.txt", "Ex_test_2.txt", "Ex_test_3.txt", "Ex_test_4.txt", "Ex_test_5.txt", "Ex_test_6.txt", "Ex_test_7.txt", "Ex_test_8.txt", "Ex_test_9.txt", "Ex_test_10.txt"], "errorGen": ["Ex_test_3.txt"]}

opCodes = { "R"   : "0110011",
            "lw"  : "0000011",
            "addi": "0010011",
            "jalr": "1100111",
            "sw"  : "0100011",
            "B"   : "1100011",
            "jal" : "1101111"}


registers = {"zero" : "00000",
             "ra"   : "00001",    
             "sp"   : "00010",
             "gp"   : "00011",
             "tp"   : "00100",
             "t0"   : "00101",
             "t1"   : "00110",
             "t2"   : "00111",
             "s0"   : "01000",
             "fp"   : "01000",
             "s1"   : "01001",
             "a0"   : "01010",
             "a1"   : "01011",
             "a2"   : "01100",
             "a3"   : "01101",
             "a4"   : "01110",
             "a5"   : "01111",
             "a6"   : "10000",
             "a7"   : "10001",
             "s2"   : "10010",
             "s3"   : "10011",
             "s4"   : "10100",
             "s5"   : "10101",
             "s6"   : "10110",
             "s7"   : "10111",
             "s8"   : "11000",
             "s9"   : "11001",
             "s10"  : "11010",
             "s11"  : "11011",
             "t3"   : "11100",
             "t4"   : "11101",
             "t5"   : "11110",
             "t6"   : "11111"}


funct3_R = {"add":"000",
            "sub":"000",
            "and":"111",
            "or" :"110",
            "srl":"101",
            "slt":"010"}


funct7_R = {"add":"0000000",
            "sub":"0100000",
            "and":"0000000",
            "or" :"0000000",
            "srl":"0000000",
            "slt":"0000000"}


funct3_B = {"beq":"000",
            "bne":"001",
            "blt":"100",} 


funct3_I = {"addi":"000",
            "lw"  :"010",
            "jalr":"000"}


funct3_S = {"sw":"010"}


labels = {}
instructions = []
pc = 0


def checkType(ins):
    if ins[0] in funct3_R:
        return rtype(ins)
    elif ins[0] in funct3_I:
        return itype(ins)
    elif ins[0] in funct3_S:
        return stype(ins)
    elif ins[0] in funct3_B:
        return btype(ins)
    elif ins[0] == "jal":
        return jtype(ins)
    
    else:
        raise SyntaxError("Wrong instruction type at line " + str(pc//4 + 1))
    

def decToBinary(n, x):
    d=0
    if n[0]=='-':
        d=1
        n=int(n[1:])
    else:
        n = int(n)
    S = ''
    if n==0:
        S='0'
    while n > 0:
        bit = n % 2
        S = str(bit) + S
        n //= 2
    if d==1:
        S=S.replace('1','2')
        S=S.replace('0','1')
        S=S.replace('2','0')
        f=len(S)
        S=bin(int(S,2)+1)
        S=str(S)
        if len(S)>f+2:
            S=S[3:]
        else:
            S=S[2:]
        S='0'*(f-len(S))+S
    y = '0' if d==0 else '1'
    while len(S) < x:
        S = y + S
    return S


def itype(ins):
    r = ""
    if len(ins)==3:
        ins[2]=ins[2].rstrip(')')
        x=ins[2].split('(')
        imm=x[0]
        rs=x[1]
        if ins[1] not in registers or rs not in registers:
            raise SyntaxError("Wrong register name at line " + str(pc//4 + 1))
    if len(ins)==4:
        imm=ins[3].strip()
        rs=ins[2].strip()
        if ins[1] not in registers or rs not in registers:
            raise SyntaxError("Wrong register name at line " + str(pc//4 + 1))
    r = decToBinary(imm,12)+registers[rs]+funct3_I[ins[0]]+registers[ins[1]]+opCodes[ins[0]]

    return r


def stype(ins):
    ins[2] = ins[2].rstrip(')')
    x = ins[2].split('(')
    imm = x[0]
    if ins[1] not in registers or x[1] not in registers:
        raise SyntaxError("Wrong register name at line " + str(pc//4 + 1))
    else:
        final_imm = decToBinary(imm,12)
        s = final_imm[:7] + registers[ins[1]] + registers[x[1]] + funct3_S[ins[0]] + final_imm[7:] + opCodes['sw']
    return s


def rtype(ins):
    if ins[3] not in registers or ins[2] not in registers or ins[1] not in registers:
        r = None
        raise SyntaxError("Wrong register name at line " + str(pc//4 + 1))
    else:
        r=funct7_R[ins[0]] + registers[ins[3]] + registers[ins[2]] + funct3_R[ins[0]] + registers[ins[1]] + opCodes['R']
    return r 


def btype(ins):
    y = ins[3].strip()
    if ins[1] not in registers or ins[2] not in registers:
        raise SyntaxError("Wrong register name at line " + str(pc//4 + 1))
    if y in labels:
        i = (labels[y] - pc)
    else:
        i = y
    x = decToBinary(str(i), 12)
    x = x[:-1]
    x = x[0] + x
    r = x[0] + x[2:8] + registers[ins[2]] + registers[ins[1]] + funct3_B[ins[0]] + x[-4:] + x[1] + opCodes['B']
    return r


def jtype(ins):
    y=ins[2].strip()
    if y in labels:
        i=labels[y]-pc
    else:
        i=y
    x=decToBinary(str(i),20)
    x=x[:-1]
    x=x[0]+x
    r=x[0]+x[-10:]+x[-11]+x[1:9]+registers[ins[1]]+opCodes['jal']
    return r


def checkLabel(s, label=0):
    global pc
    if label != 0:
        labels[label] = pc
    if s and not (len(s) == 1 and s[0] == ''):
        instructions.append(s)
        pc += 4


def fileRead (file_name):
    with open(file_name, 'r') as file:
        while True:
            line = file.readline().strip()
            label=0
            if not line:
                break
            s = line.split(":")
            if len(s)>1:
                label=s[0]
                s[1]=s[1].strip()
                s = re.split(pattern=r"[,. ]", string=s[1])
            else:
                s[0]=s[0].strip()
                s=re.split(pattern=r"[,. ]", string=s[0])
            checkLabel(s,label)


def fileOutput (Output):
    if instructions[-1] != ["beq", "zero", "zero", "0"]:
        raise SyntaxError("Missing virtual halt instruction at the end")
    global pc
    pc=0
    with open(Output, 'w') as file:
        for ins in instructions:
            file.write(checkType(ins) + '\n')
            pc+=4


file_name = "c:/kj/CO_Project_Allocated_jan30_2025/SimpleAssembler/input.txt"
output = "c:/kj/CO_Project_Allocated_jan30_2025/SimpleAssembler/output.txt"

fileRead(file_name)
fileOutput(output)
