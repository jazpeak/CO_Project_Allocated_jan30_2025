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
            #print(S)

    y = '0' if d==0 else '1'
    while len(S) < x:
        S = y + S
    return S   


i=1024
x=decToBinary(str(i),12)
x=x[:-1]
x=x[0]+x
print(x)
print(f"imm[12]: {x[0]}, imm[10:5]: {x[1:7]}, imm[4:1]: {x[7:11]}, imm[11]: {x[11]}")
