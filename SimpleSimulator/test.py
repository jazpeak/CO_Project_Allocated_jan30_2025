rs1=0
imm=8
'''
addi t3,zero,8
jalr t0,t3,8
'''
if opcode == "0000011": #  i - type lw
    imm=twos_to_dec(instr[:12])   # arul to do
    rs1=int(instr[12:17],2)
    funct3=instr[17:20]                                   #~Jazl
    rd=int(instr[20:25],2)
    rs1=10000-int(dec_to_hex(rs1)[2:])
    addr=rs1+imm
    print("addsvaw",registers[rs1],rs1,addr,imm,addr)

    if funct3=='010':
        print("aefawf",addr)
        
        registers[rd]=memory[addr]
        
