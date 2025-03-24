def decode_instruction(instr):

    opcode = instr[7:]

    if opcode == "0110011": # checks r - type
                         # for loop to store values of registrsss bla bla..
    
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
    


#The input file will be in binary format. we extract line by line from function below and put it in decode_instruction function
def run(file_name):
    fil = open(file_name, "r")
    fl = fil.readlines()
    for line in fl:
        decode_instruction(line.strip())
    
    fil.close()