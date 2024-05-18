# MISA (My Instruction Set Architecture) v0.1
# May 2023
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
# "Misa your humble servant!" - .jarjar binks
#
# "I may have gone too far in a few places."


File usage:
	navigate to folder in cmd terminal
	To assemble:
		"python MISA_ASM.py [filename].asm"
		this generates [filename].bin
	To execute:
		"python main.py [filename].bin"

This assembly language is kinda wacky. 
There are 16 registers (r0-r15) each 16bits large.
There are 0x10000 words of memory with 16bit addressing.
Instructions are 32 bits:
6 bits for the opcode (though I only actually use 4 for now)
5 bits for op1 (1 to flag indirect and 4 for the register reference)
11 bits for op2 (1 to flag long ie. extend op2 to 16 bits (really 18) by using op3's space, 1 to flag indirect, and 1 to flag whether it's a register)
10 bits for op3 (1 to flag indirect, and 1 to flag whether it's a register)
When writing assembly you don't need to worry about any of those flags except the indirect one (explained below)

How to write:
INSTR op1 op2 op3

Currently, case matters; the opcode must be capitalized and anything else lowercase.
Commas aren't needed; make sure you use spaces correctly instead.
First operand (usually the destination) must be a register.
Second operand can be a register, address, or value.
Third operand (often optional) can be a register, address, or value.

Write "i" or "i:" before any operand to mark it as indirect. For a register, this makes its value act as a pointer, and for a literal, it makes it itself a pointer. (idk if that really counts as "indirect" but whatever.)
For example, consider the following two examples:
ADD r1 r2 r3
This adds the value stored in r2 with the value stored in r3 and writes it into r1.
ADD i:r1 i:r2 i:r3 (or ADD ir1 ir2 ir3)
This adds the value at the address stored in r2 with the value at the address stored in r3 and writes it into the address stored in r1.

Note that codes such as AND have some varying functionality. For example, as well as using it as we did above, you could also do this:
ADD r0 0x1000
First, note how there are now only two operands; in this case, AND will simply add the second operand's value to r0's, overwriting r0's initial value.
Second, note that the second operand is 0x1000 (decimal 4,096), which is a 13-bit value, even though an operand can normally only store 8 bits. In this case, because there was no third operand, the second operand was able to hold a value up to 16 bits (technically 18). You could also use this to write from a custom address using "i:" since memory goes up to 0x10000. Just note that you can't write TO a direct address since the first operand must be a register.

And now for specific information about available opcodes (there are two leading zeros to each one that I left off because I'm not really using them, I only have less than 16 instructions but those last two bits are just so the total size is 32 bits).
Remember that "i:" can be placed before most any operand to use the address it points to rather than the value directly given.
Also remember that if op3 is not used, op2 can be 16bits instead of 8.

Note: ADR is special, it is the only instruction whose first (and only) operand isn't a register and can be more than 4/5 bits long
0: Set Address: ADR [op1]
op1 = address
Set the starting memory location for instructions to be stored.
eg) ADR 0x1000 # instructions will be written starting at memory address 0x1000)

1: Write: LOD [op1] [op2]
op1 = destination register
op2 = source
Write to a register from memory or another register.
eg) LOD r0 5 # write the value 5 into r0
eg) LOD r0 i:0x100 # write the value stored at 0x100 into r0
eg) LOD i:r0 r2 # write the value of r2 into the address pointed to by r0

NOTE FOR STR: THIS ONE SWAPS THE SOURCE AND DESTINATION FROM THE USUAL
Also, if you use a register for op2, it will automatically be indirect.
2: Store: STR [op1] [op2]
op1 = source register
op2 = destination
Write from a register to memory
eg) STR r1 0x200 # write r1's value into memory at address 0x200
eg) STR r3 i:r4 # write r3's value into memory at the address given by r4

3: Add: ADD [op1] [op2] [op3]
op1 = destination register
op2 = addend (expandable to 16 bits)
op3 = addend (optional)
Increment op1 by the value at op2, or add op2 and op3 together and store at op1.
eg) ADD r4 8 # r4's value will now be 8 greater than it was previously
eg) ADD r5 i:0x4000 # r5's value will be increased by the value stored at 0x4000
eg) ADD r0 r1 r2 # add r1 and r2 together and store the result in r0
eg) ADD i:r6 r7 1 # add 1 to r7 then store the result at the address given by r6

4: Subtract: SUB [op1] [op2] [op3]
Decrement op1 by the value at op2, or subtract op3 from op2 and store at op1.

5: Input: INP [op1]
op1 = destination (register or address)
Request input and store at op1

6: Output: OUT [op1]
op1 = source (value, register or address; remember to use "i:" if an address)
Output the value at op1 to the console

7: Branch if Equal: BEQ [op1] [op2] [op3]
Compare op1 to op2 and, if equal, branch to the label specified by op3

8: Branch if Greater Than: BGT [op1] [op2] [op3]
If op1 > op2, branch to the label specified by op3

9: Branch if Less Than: BLT [op1] [op2] [op3]
If op1 < op2, branch to the label specified by op3

A: Shift Left: SLL [op1] [op2]
op1 = value to shift
op2 = (optional) number of times to shift
Binary shift op1 left op2 times, otherwise just once

B: Shift Right Logical: SRL [op1] [op2]
op1 = value to shift
op2 = (optional) number of times to shift
Logical binary shift op1 right op2 times, otherwise just once

C: Shift Right Arithmetic: SRA [op1] [op2]
op1 = value to shift
op2 = (optional) number of times to shift
Arithmetic binary shift op1 right op2 times, otherwise just once

D: Multiply: MUL [op1] [op2] [op3]
op1 = destination register (multiplicand if no op3)
op2 = multiplicand (multiplier if no op3; expandable to 16 bits)
op3 = multiplier (optional)
Works like ADD and SUB but with multiplication.
I didn't think it was necessary with looping but I have all this extra space for opcodes so whatever.

F: Halt: END
Halt execution of the program.