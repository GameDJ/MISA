# MISA_ASM.py v0.1
# May 2023
# MISA (My Instruction Set Architecture - Assembler)
# ⠀⠀⠀⠀⠀⠀⢀⣶⣤⣀⠀⠀⠀⡼⡑⠢⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
# ⠀⠀⠀⠀⠀⠀⢘⢉⢹⣯⣆⡰⣾⣷⣀⡄⣼⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
# ⠀⠀⠀⠀⠀⠀⠈⣧⠭⣹⢟⣽⣿⣷⡚⠿⠏⠳⠒⠢⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀
# ⠀⠀⠀⠀⠀⠀⠀⢈⠏⠈⠼⣿⣿⣏⠉⠀⠀⠀⠀⢶⠛⠢⡀⠀⠀⠀⠀⠀⠀⠀
# ⠀⠀⠀⠀⠀⠀⠀⡦⠂⠀⠊⠳⠀⠛⡢⠀⠀⠀⠀⠈⠄⠁⣻⡄⠀⠀⠀⠀⠀⠀
# ⠀⠀⠀⠀⠀⠀⡔⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠸⠄⣘⢣⠀⠀⠀⠀⠀⠀
# ⠀⠀⠀⠀⠀⢎⣀⡠⠤⢄⣀⡀⠤⠴⠶⠠⠀⠀⠀⠀⢀⠎⢸⣽⡀⠀⠀⠀⠀⠀
# ⠀⠀⠀⠀⠀⠀⠘⡤⣀⣀⣀⣤⣶⣤⠤⠂⠐⠀⠀⠀⢸⠘⠔⠝⡅⠀⠀⠀⠀⠀
# ⠀⠀⠀⠀⠀⠀⢰⢅⣽⢷⡝⡈⠀⠀⠀⢀⠀⠀⠀⠀⣟⠈⢄⡌⡵⠀⠀⠀⠀⠀
# ⠀⠀⠀⠀⠀⢀⢇⣾⣯⡞⢀⠱⡀⠀⠀⠀⠀⠀⠀⢸⠀⢔⠀⠈⠂⡆⠀⠀⠀⠀
# ⠀⠀⠀⠀⠀⡜⣻⡿⣹⠃⡌⡠⠃⠀⠀⠀⠀⠀⢠⣿⠀⠀⠈⢄⠉⢳⠀⠀⠀⠀
# ⠀⠀⠀⠀⢰⢡⣿⢷⣿⡖⠉⠀⠀⠀⠀⠀⠀⠀⠀⢿⣆⠀⢀⣀⠊⠀⠢⠀⠀⠀
# ⠀⠀⢀⢔⣡⣾⣿⣿⣿⣷⠀⠀⠀⠀⠀⠀⠀⠀⠀⠘⣻⣷⣄⡀⠀⠁⠅⣵⠀⠀
# ⠀⠀⣶⣯⠟⠛⣿⣿⣿⣿⣷⣦⣤⠀⠀⠀⠀⠀⢀⣤⣾⣿⣿⡧⡀⠠⠎⠌⡄⠀
# ⠀⠀⠜⠁⠀⠀⠸⣿⣿⣿⣿⣿⣿⣦⡀⠀⠀⢠⣿⣽⣿⣿⣿⣧⠀⠑⠄⡉⢘⡄
# ⡔⠀⠀⠀⠀⠀⠀⣿⣿⣿⣿⣿⣿⣿⣿⠀⠀⣼⣿⣿⣿⣿⣿⣿⠀⠀⠀⠘⡄⡴⠀⠀⠀⠀⠀⠀⠀⠀
# "Misa assembler!" - .jarjar binks
# "The ability to encode instructions does not make you intelligent." - Py-thon Jinn

# todo:
#   remove usages of instr
#   change order of flag bits

import sys


def checkIndirect(tokens, opNum, instrHelper):
    indirectFlag = 0
    if opNum == 2:
        indirectFlag = 1
    elif opNum == 3:
        instrHelper[2][0] = '0'
    if tokens[opNum][0] == 'i':
        instrHelper[opNum - 1][indirectFlag] = '1'  # set indirect flag for op1
        tokens[opNum] = tokens[opNum].replace('i', '').replace(':', '')  # remove i or i:
    return [tokens, instrHelper]


def checkRegister(tokens, opNum, instrHelper):
    radix = 10
    registerFlag = 2
    if opNum == 3:
        registerFlag = 1
        instrHelper[2][1] = '0'  # populate op3's register flag
    if tokens[opNum][0] == 'r':
        instrHelper[opNum - 1][registerFlag] = '1'  # set register flag for op2
        tokens[opNum] = tokens[opNum].replace('r', '')  # remove r
    if len(tokens[opNum]) > 1:
        if tokens[opNum][1] == 'x':
            radix = 16
        elif tokens[opNum][1] == 'b':
            radix = 2
    tokens[opNum] = tokens[opNum].replace("0x", '').replace("0b", '')  # remove radix
    return [tokens, instrHelper, radix]


def addLeadingZeros(string, totalPlaces, side = 'left'):
    totalPlaces -= len(string)
    while totalPlaces > 0:
        if side == 'left':
            string = "0" + string
        elif side == 'right':
            string = string + '0'
        totalPlaces -= 1
    return string


labels = {}
start_address = 0

# Parse Labels
line_counter = 0
asm = open(sys.argv[1], 'r')
# with open(sys.argv[1], 'r') as asm:
for line in asm:
    # skip comments
    if line[0] == '#':
        continue
    elif line[0] == '.':
        # Record label name with the line it leads to
        labels[line.replace('.', '').replace('\n', '')] = line_counter
        continue
    else:
        line_counter += 1

name = sys.argv[1].split('.')[0]
# with sys.argv[1].split('.')[0] as name:
binary_file = open(name + ".bin", "wb")
binary_file.close()
# with open(name + ".bin", "wb") as binary_file:
#     binary_file.close()
file_name = name + ".bin"


def writebin(data):
    binary_file = open(file_name, "ab")
    # with open(file_name, "ab") as binary_file:
    binary_file.write(int(data, 2).to_bytes(4, byteorder='big'))


# this version will try consolidating the token reading

opcodes = {"ADR": 0, "LOD": 1, "STR": 2, "ADD": 3, "SUB": 4, "INP": 5, "OUT": 6, "BEQ": 7, "BGT": 8, "BLT": 9,
           "SLL": 10, "SRL": 11, "SRA": 12, "MUL": 13, "END": 15}

# Assemblers assemble!!!
asm = open(sys.argv[1], 'r')
# with open(sys.argv[1], 'r') as asm:
line_counter = 0
for line in asm:
    instr = []
    bin_string = "00"
    radix = 10
    # instrH stores helper bits for instr
    # instr[0]: op1 indirect
    # instr[1]: op2 expanded, indirect, register
    # instr[2]: indirect, register
    instrH = [['0'], ['0', '0', '0'], ['', '']]
    # skip labels
    if line[0] == '.':
        continue
    # skip comments
    elif line[0] == '#':
        continue
    else:
        line = line.replace(',', ' ')
        line = line.replace('  ', ' ')
        line = line.replace('\n', '')
        print(line)
        if line.find('#'):  # cut off inline comments
            line = line.split('#')[0]
        tok = line.split(' ')
        # print(tok)
        # first check for ADR which is special
        # note that it does not increment the line counter
        if tok[0] == 'ADR':
            [tok, instrH, radix] = checkRegister(tok, 1, instrH)
            writebin(addLeadingZeros(bin(int(tok[1], radix))[2:], 32))
            continue
        # encode opcode
        tok[0] = bin(opcodes[tok[0]])[2:]
        instr.append(tok[0])
        bin_string += addLeadingZeros(tok[0], 4)
        # print(tok)
        if len(tok) > 1:
            # operand 1 (tok[1])
            [tok, instrH] = checkIndirect(tok, 1, instrH)
            tok[1] = tok[1].replace('r', '')  # remove r
            tok[1] = bin(int(tok[1])).split('b')[1]
            instr.append(tok[1])
            # Encode op1
            bin_string += instrH[0][0]
            bin_string += addLeadingZeros(tok[1], 4)
            # print(tok)
            # 2 or more operands
            if len(tok) > 2:
                # op2
                [tok, instrH] = checkIndirect(tok, 2, instrH)
                [tok, instrH, radix] = checkRegister(tok, 2, instrH)
                tok[2] = bin(int(tok[2], radix)).split('b')[1]
                instr.append(tok[2])  # add register's value
                # print(tok)
                if len(tok) == 3:  # if just 2 operands
                    instrH[1][0] = '1'  # set op2 expanded flag
                # Encode op2
                for x in instrH[1]:  # add op2's flags
                    bin_string += x
                if len(tok) == 3:  # if just 2 operands
                    bin_string += addLeadingZeros(tok[2], 18)  # add expanded op2
                # 3 operands
                if len(tok) == 4:
                    bin_string += addLeadingZeros(tok[2], 8)  # add normal op2
                    if 7 <= int(tok[0], 2) <= 9:  # if branching instruction
                        # encode label's line counter
                        bin_string += addLeadingZeros(bin(labels[tok[3]])[2:], 10)
                    else:
                        # op3
                        [tok, instrH] = checkIndirect(tok, 3, instrH)
                        [tok, instrH, radix] = checkRegister(tok, 3, instrH)
                        tok[3] = bin(int(tok[3], radix)).split('b')[1]
                        # print(tok)
                        instr.append(tok[3])  # add register's value
                        for x in instrH[2]:  # add op3's flags
                            bin_string += x
                        bin_string += addLeadingZeros(tok[3], 8)  # add op3

        # fill in trailing zeros for lesser-operand instructions
        bin_string = addLeadingZeros(bin_string, 32, 'right')
        print(bin_string)
        writebin(bin_string)  # write the binary to the file
        line_counter += 1

print("Assembly complete")
