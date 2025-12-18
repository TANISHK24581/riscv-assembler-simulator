import sys

input_file = sys.argv[1]

output_file = sys.argv[2]



registers={
    'x0': '00000', 'x1': '00001', 'x2': '00010', 'x3': '00011',
    'x4': '00100', 'x5': '00101', 'x6': '00110', 'x7': '00111',
    'x8': '01000', 'x9': '01001', 'x10': '01010', 'x11': '01011',
    'x12': '01100', 'x13': '01101', 'x14': '01110', 'x15': '01111',
    'x16': '10000', 'x17': '10001', 'x18': '10010', 'x19': '10011',
    'x20': '10100', 'x21': '10101', 'x22': '10110', 'x23': '10111',
    'x24': '11000', 'x25': '11001', 'x26': '11010', 'x27': '11011',
    'x28': '11100', 'x29': '11101', 'x30': '11110', 'x31': '11111',
    'zero': '00000',
    'ra': '00001',
    'sp': '00010',
    'gp': '00011',
    'tp': '00100',
    't0': '00101',
    't1': '00110',
    't2': '00111',
    'fp': '01000',
    's0': '01000',
    's1': '01001',
    'a0': '01010',
    'a1': '01011',
    'a2': '01100',
    'a3': '01101',
    'a4': '01110',
    'a5': '01111',
    'a6': '10000',
    'a7': '10001',
    's2': '10010',
    's3': '10011',
    's4': '10100',
    's5': '10101',
    's6': '10110',
    's7': '10111',
    's8': '11000',
    's9': '11001',
    's10': '11010',
    's11': '11011',
    't3': '11100',
    't4': '11101',
    't5': '11110',
    't6': '11111',}

d={}

abc= [
    'add', 
    'sub', 
    'slt', 
    'srl', 
    'or', 
    'and', 
    'addi', 
    'lw', 
    'jalr', 
    'sw', 
    'beq', 
    'bne', 
    'blt', 
    'jal'
]

def test11():
    global d
    l=[]
    
    f=open(input_file,"r")
    c=0
    for i in f:
        j=i.lower()
        c=c+1
        y=j.split(" ")
        z=''
        if y[0] not in abc:
            for i in y[0]:
                if i!=":":
                    z=z+i
                else:
                    break
            d[z]=[c]
            q=j.find(":")
            y=j[q+1::]
            l.append(y)
        else:
            l.append(j)

    f.close()

    f=open("input1.txt","w")
    for i in l:
        
        
        f.write(i)
    f.close()
    
        
test11()




def twoscomplement(n, bits):
    if n < 0:
        n = (1 << bits) + n  # Two's complement calculation for negative numbers
    return bin(n)[2:].zfill(bits) 






def Rtype(opcode, funct7, rs2, rs1, funct3, rd):      #RTYPE INSTRUCTIONS 
    return f"{funct7}{registers[rs2]}{registers[rs1]}{funct3}{registers[rd]}{opcode}"



def Itype(opcode, imm, rs1, funct3, rd):               #ITYPE INSTRUCTIONS   
    z=twoscomplement(imm,12)

   


    return f"{z}{registers[rs1]}{funct3}{registers[rd]}{opcode}"


def Stype(opcode, imm, rs2, rs1, funct3):              #STYPE INSTRUCTIONS 
    imm_7_5 = format((imm >> 5) & 0x7F, '07b')
    imm_4_0 = format(imm & 0x1F, '05b')     




  
    return f"{imm_7_5}{registers[rs2]}{registers[rs1]}{funct3}{imm_4_0}{opcode}"

def Btype(opcode, imm, rs2, rs1, funct3):              #STYPE INSTRUCTIONS
    imm_12 = format((imm >> 12) & 0x1, '01b')
    imm_10_5 = format((imm >> 5) & 0x3F, '06b')
    imm_4_1 = format((imm >> 1) & 0xF, '04b')
    imm_11 = format((imm >> 11) & 0x1, '01b')
    return f"{imm_12}{imm_10_5}{registers[rs2]}{registers[rs1]}{funct3}{imm_4_1}{imm_11}{opcode}"



def to_twoscomplement(value, bits):
    
    if value < 0:
        value = (1 << bits) + value  
    return format(value & ((1 << bits) - 1), f'0{bits}b') 
def Jtype(opcode, imm, rd):


    
   
    imm_20 = to_twoscomplement((imm >> 20) & 0x1, 1)      # 1 bit for imm[20]
    imm_10_1 = to_twoscomplement((imm >> 1) & 0x3FF, 10)   # 10 bits for imm[10:1]
    imm_11 = to_twoscomplement((imm >> 11) & 0x1, 1)       # 1 bit for imm[11]
    imm_19_12 = to_twoscomplement((imm >> 12) & 0xFF, 8)   # 8 bits for imm[19:12]
    
 
    return f"{imm_20}{imm_10_1}{imm_11}{imm_19_12}{registers[rd]}{opcode}"






def assembler1(l,c):
    l=l.replace(","," ")
    l=l.replace(":"," ")
    parts = l.split()
    instruction = parts[0]
    
    label={}
    
    #R-type instructions----add, sub, slt, srl, or, and

    
    if instruction == 'add':

        
        rd, rs1, rs2 = parts[1], parts[2], parts[3]
        
                                             
                                             
        return Rtype('0110011', '0000000', rs2, rs1, '000', rd)  # ADD
    elif instruction == 'sub':
        rd, rs1, rs2 = parts[1], parts[2], parts[3]
        return Rtype('0110011', '0100000', rs2, rs1, '000', rd)  # SUB
    elif instruction == 'slt':
        rd, rs1, rs2 = parts[1], parts[2], parts[3]
        return Rtype('0110011', '0000000', rs2, rs1, '010', rd)  # SLT
    elif instruction == 'srl':
        rd, rs1, rs2 = parts[1], parts[2], parts[3]
        return Rtype('0110011', '0000000', rs2, rs1, '101', rd)  # SRL
    elif instruction == 'or':
        rd, rs1, rs2 = parts[1], parts[2], parts[3]
        return Rtype('0110011', '0000000', rs2, rs1, '110', rd)  # OR
    elif instruction == 'and':
        rd, rs1, rs2 = parts[1], parts[2], parts[3]
        return Rtype('0110011', '0000000', rs2, rs1, '111', rd)  # AND


    
    # I-type instructions----addi, lw, jalr

    
    elif instruction == 'addi':
        
        rd, rs1, imm = parts[1], parts[2], int(parts[3])
        return Itype('0010011', imm, rs1, '000', rd)  # ADDI
    elif instruction == 'lw':  
        rd=parts[1]
        imm=''
        for i in parts[2]:
            if i!="(":
                imm=imm+i
            else:
                break
        rs1=parts[2][-3:-1:1]
        imm=int(imm)
        
        

        
        return Itype('0000011', imm, rs1, '010', rd)  # LW
    elif instruction == 'jalr':
        rd, rs1, imm = parts[1], parts[2], int(parts[3])
        return Itype('1100111', imm, rs1, '000', rd)  # JALR



    
    # S-type instructions--- sw

    elif instruction == 'sw':
        rs2=parts[1]
        imm=''
        for i in parts[2]:
            if i!="(":
                imm=imm+i
            else:
                break
        rs1=parts[2][-3:-1:1]
        imm=int(imm)
        
       
        return Stype('0100011', imm, rs2, rs1, '010')  # SW


    
    # B-type instructions---beq, bne, blt


    
    elif instruction == 'beq':

        if parts[3] in d:
            
            for i in d[parts[3]]:
                y=i
            imm=4*(y-c)                                              #IMM VALUE FOR LABEL
            
            rs1, rs2, imm = parts[1], parts[2], imm
        else:
            rs1, rs2, imm = parts[1], parts[2], int(parts[3])

        
        
        return Btype('1100011', imm, rs2, rs1, '000')  # BEQ
    elif instruction == 'bne':
        if parts[3] in d:
            for i in d[parts[3]]:
                y=i
            imm=4*(y-c)
            rs1, rs2, imm = parts[1], parts[2], imm
        else:
            rs1, rs2, imm = parts[1], parts[2], int(parts[3])
        return Btype('1100011', imm, rs2, rs1, '001')  # BNE
    elif instruction == 'blt':
        if parts[3] in d:
            for i in d[parts[3]]:
                y=i
            imm=4*(y-c)
            rs1, rs2, imm = parts[1], parts[2], imm

        else:
            rs1, rs2, imm = parts[1], parts[2], int(parts[3])
        return Btype('1100011', imm, rs2, rs1, '100')  # BLT
    
    # J-type instructions---jal
    elif instruction == 'jal':

        if parts[2] in d:
            for i in d[parts[2]]:
                y=i
            imm=4*(y-c)
            rd, imm = parts[1], int(imm)
        else:
            rd, imm = parts[1], int(parts[2])
        return Jtype('1101111', imm, rd)  # JAL

   
        


def assembler2(f):
    binarycode=[]
    c=0

    try:
        with open(f, 'r') as file:
            
            for i in file:
                c=c+1
                
                
                binarycode.append(assembler1(i.lower(),c))
    except FileNotFoundError:
        print(f"FILE'{f}' NOT FOUND")
        return []

    
    
    return binarycode


def write(binarycode,f):
    try:
        with open(f, 'w') as file:
            for i in binarycode:
                file.write(i + '\n')
    except :
        print(f"ERROR WRITING TO THE {f}")

# Main execution
inputt="input1.txt"
outputt='output.txt'

binarycode = assembler2(inputt)


# Write the binary program to output.txt
if binarycode:
    write(binarycode,output_file)
    print(f"ASSEMBLY DONE INTO .")
else:
    print("ASSEMBLY NOT DONE.")
    


    


    
