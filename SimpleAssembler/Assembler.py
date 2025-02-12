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


registers = {"x0" : "00000",
             "x1" : "00001",    
             "x2" : "00010",
             "x3" : "00011",
             "x4" : "00100",
             "x5" : "00101",
             "x6" : "00110",
             "x7" : "00111",
             "x8" : "01000",
             "x9" : "01001",
             "x10": "01010",
             "x11": "01011",
             "x12": "01100",
             "x13": "01101",
             "x14": "01110",
             "x15": "01111",
             "x16": "10000",
             "x17": "10001",
             "x18": "10010",
             "x19": "10011",
             "x20": "10100",
             "x21": "10101",
             "x22": "10110",
             "x23": "10111",
             "x24": "11000",
             "x25": "11001",
             "x26": "11010",
             "x27": "11011",
             "x28": "11100",
             "x29": "11101",
             "x30": "11110",
             "x31": "11111"}


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


def checkLabel(s):
    global pc
    if s[0].endswith(":"):
                label = s[0][:-1]
                labels[label] = pc
    else:
        instructions.append(s)
        pc += 4

<<<<<<< HEAD
def rtype(ins):
    r=funct3_R[ins[0]] + registers[ins[1]] + registers[ins[2]] + funct3_R[ins[3]] + registers[ins[4]] + opCodes['R']
    return r 

=======
    
>>>>>>> 8fb5822ec29d4ce098acd62cbf094f3ca5962bb1
def fileRead (file_name):
    with open(file_name, 'r') as file:
        while True:
            line = file.readline()
            if not line:
                break
            s = re.split(pattern=r"[:,. ]", string=line)
            checkLabel(s)
    



