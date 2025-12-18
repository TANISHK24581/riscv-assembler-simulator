import sys

input_file = sys.argv[1]

output_file = sys.argv[2]



L=[]
def sign_extend(val, bits):
    if (val >> (bits - 1)) & 1:
        val -= 1 << bits
    return val

def unsigned(x):
    return x & 0xffffffff

def signed(x):
    if x & 0x80000000:
        return x - 0x100000000
    return x

def to_32bit_binary(value):
    if value >= 0:
        return "0b"+format(value, '032b')  
    else:
        return "0b"+format((1 << 32) + value, '032b')



# Decoding functions
def decode_R_type(instr):
    funct7 = int(instr[0:7], 2)
    rs2 = int(instr[7:12], 2)
    rs1 = int(instr[12:17], 2)
    funct3 = int(instr[17:20], 2)
    rd = int(instr[20:25], 2)
    opcode = instr[25:32]
    return {'funct7': funct7, 'rs2': rs2, 'rs1': rs1, 'funct3': funct3, 'rd': rd, 'opcode': opcode}
def decode_I_type(instr):
    imm_bin = instr[0:12]
    rs1 = int(instr[12:17], 2)
    funct3 = int(instr[17:20], 2)
    rd = int(instr[20:25], 2)
    opcode = instr[25:32]
    imm = sign_extend(int(imm_bin, 2), 12)
    return {'imm': imm, 'rs1': rs1, 'funct3': funct3, 'rd': rd, 'opcode': opcode}

def decode_S_type(instr):
    imm_bin = instr[0:7] + instr[20:25]
    rs2 = int(instr[7:12], 2)
    rs1 = int(instr[12:17], 2)
    opcode = instr[25:32]
    imm = sign_extend(int(imm_bin, 2), 12)
    return {'imm': imm, 'rs1': rs1, 'rs2': rs2, 'opcode': opcode}

def decode_B_type(instr):
    imm_12 = instr[0]
    imm_10_5 = instr[1:7]
    rs2 = int(instr[7:12], 2)
    rs1 = int(instr[12:17], 2)
    funct3 = int(instr[17:20], 2)
    imm_4_1 = instr[20:24]
    imm_11 = instr[24]
    opcode = instr[25:32]
    imm_bin = imm_12 + imm_11 + imm_10_5 + imm_4_1
    imm = sign_extend(int(imm_bin, 2), 12)
    offset = imm << 1
    return {'offset': offset, 'rs1': rs1, 'rs2': rs2, 'funct3': funct3, 'opcode': opcode}

def decode_J_type(instr):
    rd = int(instr[20:25], 2)
    imm_bin = instr[0] + instr[12:20] + instr[11] + instr[1:11]
    imm = sign_extend(int(imm_bin, 2), 21)
    offset = imm << 1
    return {'rd': rd, 'offset': offset, 'opcode': instr[25:32]}

# Global memory model (addresses -> 32-bit word)
memory = {}

def execute_instruction(instr_bin, registers, pc):
    opcode = instr_bin[25:32]
    new_pc = pc + 4

    # R-type: add, sub, slt, srl, or, and
    if opcode == "0110011":
        decoded = decode_R_type(instr_bin)
        rs1_val = registers[decoded['rs1']]
        rs2_val = registers[decoded['rs2']]
        if decoded['funct3'] == 0:
            if decoded['funct7'] == 0:  # add
                result = rs1_val + rs2_val
            elif decoded['funct7'] == 32:  # sub
                result = rs1_val - rs2_val
            else:
                result = registers[decoded['rd']]
        elif decoded['funct3'] == 2 and decoded['funct7'] == 0:  # slt (signed less-than)
            result = 1 if signed(rs1_val) < signed(rs2_val) else 0
        elif decoded['funct3'] == 5 and decoded['funct7'] == 0:  # srl (shift right logical)
            shamt = rs2_val & 0x1f
            result = rs1_val >> shamt
        elif decoded['funct3'] == 6 and decoded['funct7'] == 0:  # or
            result = rs1_val | rs2_val
        elif decoded['funct3'] == 7 and decoded['funct7'] == 0:  # and
            result = rs1_val & rs2_val
        else:
            result = registers[decoded['rd']]
        result = unsigned(result)
        if decoded['rd'] != 0:
            registers[decoded['rd']] = result


    # I-type: addi, lw, jalr
    elif opcode == "0010011":  # addi
        decoded = decode_I_type(instr_bin)
        rs1_val = registers[decoded['rs1']]
        if decoded['funct3'] == 0:  # addi
            result = rs1_val + decoded['imm']
        else:
            result = registers[decoded['rd']]
        result = unsigned(result)
        if decoded['rd'] != 0:
            registers[decoded['rd']] = result

    elif opcode == "0000011":  # lw
        decoded = decode_I_type(instr_bin)
        if decoded['funct3'] == 2:
            addr = unsigned(registers[decoded['rs1']] + decoded['imm'])
            val = memory.get(addr, 0)
            if decoded['rd'] != 0:
                registers[decoded['rd']] = unsigned(val)
        else:
            pass  # unsupported I-type

    elif opcode == "1100111":  # jalr
        decoded = decode_I_type(instr_bin)
        rs1_val = registers[decoded['rs1']]
        target = unsigned(rs1_val + decoded['imm']) & 0xfffffffe  # clear LSB
        if decoded['rd'] != 0:
            registers[decoded['rd']] = unsigned(pc + 4)
        new_pc = target

    
    # S-type: sw
    elif opcode == "0100011":  # sw
        decoded = decode_S_type(instr_bin)
        addr = unsigned(registers[decoded['rs1']] + decoded['imm'])
        memory[addr] = unsigned(registers[decoded['rs2']])
        # No register write-back for sw

    # B-type: beq, bne
    elif opcode == "1100011":
        decoded = decode_B_type(instr_bin)
        rs1_val = registers[decoded['rs1']]
        rs2_val = registers[decoded['rs2']]
        if decoded['funct3'] == 0:  # beq
            if rs1_val == rs2_val:
                new_pc = pc + decoded['offset']
        elif decoded['funct3'] == 1:  # bne
            if rs1_val != rs2_val:
                new_pc = pc + decoded['offset']

    # J-type: jal
    elif opcode == "1101111":  # jal
        decoded = decode_J_type(instr_bin)
        if decoded['rd'] != 0:
            registers[decoded['rd']] = unsigned(pc + 4)
        new_pc = pc + decoded['offset']

    else:
        # Unsupported opcode: just advance
        new_pc = pc + 4

    registers[0] = 0  # x0 always remains 0
    return registers, new_pc



def print_state(pc, registers, output_file='outputttt.txt'):
    global L
    # Format registers as 32-bit binary strings
    reg_str = " ".join(str(to_32bit_binary(reg)) for reg in registers)
    
    # Create the output string
    output = f"{to_32bit_binary(pc)} {reg_str}\n"
    L.append(output)
    
    
    
l1=[]

def print_memory_trace(data_memory, start_addr=0x00010000, end_addr=0x0001007C):
    for addr in range(start_addr, end_addr + 1, 4):
        value = data_memory.get(addr, 0)
        # Format address with leading zeros to 8 digits
        formatted_addr = f"0x{addr:08X}"
        # Format value as 32-bit binary with '0b' prefix
        binary_str = f"0b{value & 0xFFFFFFFF:032b}"
        l1.append(f"{formatted_addr}:{binary_str}\n")
    

    
    
        
 
def main():
    global L
    global l1
    instructions=[]
    # Initialize registers (x0..x31): x0 remains 0, sp(x2) set to 380.
    registers = [0] * 32
    registers[2] = 380
    pc = 0
    f=open(input_file, "r")
    for i in f:
        instructions.append(i)
    f.close()

   
        

    

    # Running simulation until PC goes out of bounds or halt condition (PC does not change)
    while True:
        idx = pc // 4
        if idx < 0 or idx >= len(instructions):
            break
        current_pc = pc
        instr = instructions[idx]
        registers, pc = execute_instruction(instr, registers, pc)
        print_state(pc, registers)
        if pc == current_pc:  # halt condition (e.g. infinite loop)
            break
    with open(output_file, 'w') as file:
        for i in L:
            file.write(i)
            

    print_memory_trace(memory)
    with open(output_file, 'a') as file:
        for i in l1:
            file.write(i)
            

main()
