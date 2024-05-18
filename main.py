# main.py v0.1
# May 2023
# MISA (My Instruction Set Architecture)
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
# "Misa bombad emulator!" - .jarjar binks

# todo:
#   implement other instructions

import sys
import struct

# REGISTERS AND MAIN MEMORY MUST BE STORED AS BINARY STRING eg '10101001'
r = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

# main memory will be an array of 0x10000 words (16 bits each)
main_memory = ['0000000000000000'] * 0x1000
pc = 0

def decodeFile(file):
    global pc
    instruction_start_offset = 0

    # Write the instructions from the file into main memory
    ir = file.read(4)
    ir = bin(struct.unpack('>I', ir)[0])[2:].zfill(32)
    if ir[:6] == '000000':  # first line is ADR
        instruction_start_offset = int(ir, 2)
        ir = file.read(4)
    while ir:
        # print(ir)
        if type(ir) is bytes:
            # convert instruction from 4 bytes of hex to 32 bits of binary
            ir = bin(struct.unpack('>I', ir)[0])[2:].zfill(32)
        # print(ir)
        # print(pc)
        # write instruction to memory
        main_memory[int(instruction_start_offset / 16) + pc] = ir
        pc += 1
        ir = file.read(4)
    file.close()
    # print("file closed")
    program_size = pc + 1
    pc = 0
    # Decode instructions
    while pc < program_size:
        # printRegisters()
        ir = main_memory[int(instruction_start_offset / 16) + pc]
        opcode = ''
        op1 = ['', '']  # value, indirect
        op2 = ['', '', '', '']  # value, indirect, register, expanded
        op3 = ['', '', '']  # value, indirect, register
        # convert instruction from 4 bytes of hex to 32 bits of binary
        #print(ir)
        ir = ir[2:]  # should probably change this so that opcodes are actually 6 bits lol
        # split the opcode off
        opcode = ir[:4]
        ir = ir[4:]
        if ir == '':
            executeInstruction(opcode, op1, op2, op3)
            pc += 1
            continue
        # parse op1
        op1[1] = ir[0]  # parse indirect
        ir = ir[1:]
        op1[0] = ir[:4]
        ir = ir[4:]
        if ir == '':
            executeInstruction(opcode, op1, op2, op3)
            pc += 1
            continue
        # parse op2
        op2[3] = ir[0]  # parse expanded
        ir = ir[1:]
        op2[1] = ir[0]  # parse indirect
        ir = ir[1:]
        op2[2] = ir[0]  # parse register
        ir = ir[1:]
        if op2[3] == '1':  # expanded op2
            op2[0] = ir
            executeInstruction(opcode, op1, op2, op3)
            pc += 1
            continue
        else:  # normal op2
            op2[0] = ir[:8]  # parse data
            ir = ir[8:]
            # parse op3
            op3[1] = ir[0]  # parse indirect
            ir = ir[1:]
            op3[2] = ir[0]  # parse register
            ir = ir[1:]
            op3[0] = ir  # data should be the rest of ir

        executeInstruction(opcode, op1, op2, op3)
        pc += 1


# note: if unsure, mbr should be an integer
def executeInstruction(opcode, op1, op2, op3):
    global pc
    # print("opcode: " + opcode + ", op1: " + str(op1) + ", op2: " + str(op2) + ", op3: " + str(op3))
    if int(opcode, 2) == 0:  # ADR  UNTESTED!!
        # This doesn't actually do anything right now since instructions aren't being loaded onto main memory, oopsie
        instruction_start_offset = op1[0]
    elif int(opcode, 2) == 1:  # LOD  UNTESTED!!
        if op1[1] == '0':  # direct
            r[int(op1[0], 2)] = getValue(op1)
        else:  # indirect
            main_memory[r[int(op1[0], 2)]] = getValue(op1)
    elif int(opcode, 2) == 2:  # STR  UNTESTED!!
        if op2[2] == '1':  # store into register
            if op2[1] == '0':  # direct
                r[int(op2[0], 2)] = r[int(op1[0], 2)]
            else:  # indirect
                main_memory[r[int(op2[0], 2)]] = r[int(op1[0], 2)]
        else:  # store at destination
            if op2[1] == '0':  # direct
                main_memory[getValue(op2)] = r[int(op1[0], 2)]
            else:  # indirect
                # maybe dont do this lol
                main_memory[int(main_memory[getValue(op2)], 2)] = r[int(op1[0], 2)]
    elif int(opcode, 2) == 3:  # ADD
        if op3[0] == '':  # if no op3
            mbr = int(getValue(op1), 2)
            mbr += int(getValue(op2), 2)
        else:
            mbr = int(getValue(op2), 2)
            mbr += int(getValue(op3), 2)
        r[int(op1[0], 2)] = mbr
        # printRegisters()
    elif int(opcode, 2) == 4:  # SUB
        if op3[0] == '':  # if no op3
            mbr = int(getValue(op1), 2)
            mbr -= int(getValue(op2), 2)
        else:
            mbr = int(getValue(op2), 2)
            mbr -= int(getValue(op3), 2)
        r[int(op1[0], 2)] = mbr
        # printRegisters()
    elif int(opcode, 2) == 5:  # INP
        mbr = input("INPUT: ")
        mbr = int(mbr)
        r[int(op1[0], 2)] = mbr
    elif int(opcode, 2) == 6:  # OUT
        print(
            "OUTPUT: " + str(int(getValue(op1), 2)) + " = " + str(hex(int(getValue(op1), 2))) + " = 0b" + getValue(op1))
    elif int(opcode, 2) == 7:  # BEQ  untested
        if int(getValue(op1), 2) == int(getValue(op2), 2):
            pc = int(getValue(op3), 2) - 1  # gotta be -1 since it increments right afterward
    elif int(opcode, 2) == 8:  # BGT
        if int(getValue(op1), 2) > int(getValue(op2), 2):
            pc = int(getValue(op3), 2) - 1  # gotta be -1 since it increments right afterward
    elif int(opcode, 2) == 9:  # BLT  untested
        if int(getValue(op1), 2) < int(getValue(op2), 2):
            pc = int(getValue(op3), 2) - 1  # gotta be -1 since it increments right afterward
    elif int(opcode, 2) == 10:  # SLL UNTESTED!!
        mbr = getValue(op1)[1:]
        for i in range(int(getValue(op2), 2)):
            mbr = mbr[1:]
            mbr = mbr + '0'
        r[int(op1[0], 2)] = mbr
    elif int(opcode, 2) == 11:  # SRL UNTESTED!!
        mbr = getValue(op1)[1:]
        for i in range(int(getValue(op2), 2)):
            mbr = '0' + mbr
            mbr = mbr[:16]
        r[int(op1[0], 2)] = mbr
    # I haven't really put much consideration into negatives/two's complement/etc but here's this anyway I guess
    elif int(opcode, 2) == 12:  # SRA UNTESTED!!
        mbr = getValue(op1)[1:]
        for i in range(int(getValue(op2), 2)):
            mbr = mbr[0] + mbr
            mbr = mbr[:16]
        r[int(op1[0], 2)] = mbr
    elif int(opcode, 2) == 13:  # MUL
        if op3[0] == '':  # if no op3
            mbr = int(getValue(op1), 2)
            mbr *= int(getValue(op2), 2)
        else:
            mbr = int(getValue(op2), 2)
            mbr *= int(getValue(op3), 2)
        r[int(op1[0], 2)] = mbr
        # printRegisters()
    elif int(opcode, 2) == 15:  # END
        # printRegisters()
        # print("Exiting program")
        exit()
    # print()


# Returns binary string! eg '10101010"
def getValue(operand):
    is_register = '1'
    if len(operand) > 2:  # op2 or op3
        is_register = operand[2]
    if operand[1] == '0':  # direct
        if is_register == '1':
            return bin(r[int(operand[0], 2)]).split('b')[1]
        else:
            return operand[0]
    else:  # indirect
        if is_register:
            return main_memory[int(r[int(operand[0], 2)] / 32)]
        else:
            return main_memory[int(int(operand[0], 2) / 32)]


def printRegisters():
    print("r:", end=" ")
    print(*r)
    print("   0 1 2 3 4 5 6 7 8 9 A B C D E F")


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    decodeFile(open(sys.argv[1], 'rb'))
