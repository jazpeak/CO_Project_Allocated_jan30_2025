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
            "jal":"000"}


funct3_S = {"sw":"010"}


labels = {}
instructions = []
pc = 0


def checkType(ins):
    ins = instructions[0]
    if ins in funct3_R:
        return rtype(ins)
    elif ins in funct3_I:
        return itype(ins)
    elif ins in funct3_S:
        return stype(ins)
    elif ins in funct3_B:
        return btype(ins)
    elif ins == "jal":
        return jtype(ins)
    

def decToBinary(n,x):
    n=int(n)
    S=''
    while n > 0:
        bit = n % 2
        S=str(bit)+S
        n //= 2
    y=S[0]
    while len(S)<x:
        S=y+S
    return S


def itype(ins):
    if len(ins)==3:
        ins[2].rstrip(')')
        x=ins[2].split('(')
        imm=x[0]
        rs=x[1]
    r= decToBinary(imm,12)+registers[rs]+registers[x[1]]+funct3_I[ins[0]]+registers[ins[1]]+opCodes[ins[0]]
    return r


def stype(ins):
    ins[2].rstrip(')')
    x = ins[2].split('(')
    imm = x[0]
    final_imm = decToBinary(imm,12)
    s = final_imm[11:4:-1] + registers[ins[1]] + registers[x[1]] + funct3_S[ins[0]] + final_imm[4::-1] + opCodes['sw']
    return s


def rtype(ins):
    r=funct3_R[ins[0]] + registers[ins[1]] + registers[ins[2]] + funct3_R[ins[3]] + registers[ins[4]] + opCodes['R']
    return r 


def btype(ins):
    x=decToBinary[ins[3],12]
    r=x[0]+x[2:8]+registers[ins[2]]+registers[ins[1]]+funct3_B[ins[0]]+ x[-4:]+x[1]+opCodes['B']
    return r


def jtype(ins):
    x=decToBinary(ins[2],20)
    r=x[0]+x[-10:]+x[-11]+x[1:9]+registers[ins[1]]+opCodes['jal']
    return r


def checkLabel(s):
    global pc
    if s[0].endswith(":"):
                label = s[0][:-1]
                labels[label] = pc
    else:
        instructions.append(s)
        pc += 4


def checkType(ins):
    ins = instructions[0]
    if ins in funct3_R:
        return rtype(ins)
    elif ins in funct3_I:
        return itype(ins)
    elif ins in funct3_S:
        return stype(ins)
    elif ins in funct3_B:
        return btype(ins)
    elif ins == "jal":
        return jtype(ins)


def fileRead (file_name):
    with open(file_name, 'r') as file:
        while True:
            line = file.readline()
            if not line:
                break
            s = re.split(pattern=r"[:,.() ]", string=line)
            checkLabel(s)


def fileOutput (file_name):
    with open(file_name, 'w') as file:
        for ins in instructions:
            file.write(checkType(ins) + '\n')

    



