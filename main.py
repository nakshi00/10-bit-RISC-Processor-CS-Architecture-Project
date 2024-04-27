from array import *
import re

# register constants and their respective binary codes
Zero = "00"
s0 = "01"
s1 = "10"
s2 = "11"


# register constants and their respective hex codes
Zerohex = "0"
s0hex = "1"
s1hex = "2"
s2hex = "3"


# opcode constants and their respective binary codes

Add = "0000"
Sub = "0001"
Addi = "0010"
And = " 0011"
OR= "0100"
beq = "0101"
slti= "0110"
Jump = "0111"
lw ="1000"
sw ="1001"



# opcode constants and their respective hexidecimal codes
Addhex = "O"
Subhex = "1"
Addihex = "2"
Andhex = " 3"
ORhex= "4"
beqhex = "5"
sltihex= "6"
Jumphex = "7"
lwhex ="8"
swhex ="9"


# write to output txt file
def write_to_output(string):
    f = open("output.txt", "a")
    f.write(string + "\n")
    f.close()


# write to outputhex txt file
def write_to_outputhex(string):
    g = open("outputhex.txt", "a")
    g.write(string + "\n")
    g.close()


# error notification
def error_register():
    write_to_output("The registers trying to be used don't exist")
    write_to_outputhex("The registers trying to be used don't exist")




def error_ins():
    write_to_output("The instruction in this line doesn't exist ")
    write_to_outputhex("The instruction in this line doesn't exist in our design")


def error_num_outofrange():
    write_to_output("The immediate number supplied is out of range")
    write_to_outputhex("The immediate number supplied is out of range")


# Takes string, recognizes which opcode it is & assigns it's binary code
def assign_Op(op):
    if (op == "add"):
        return Add
    elif (op == "sub"):
        return Sub
    elif (op == "addi"):
        return Addi
    elif (op == "and"):
        return And
    elif (op == "or"):
        return OR
    elif (op == "beq"):
        return beq
    elif (op == "slti"):
        return slti
    elif (op == "lw"):
        return  lw
    elif (op == "sw"):
        return sw
    elif (op == "j"):
        return Jump
    else:
        error_ins()


# Takes string, recognizes which opcode it is & assigns it's hex code
def assign_hexOp(op):
    if (op == "add"):
        return Addhex
    elif (op == "sub"):
        return Subhex
    elif (op == "addi"):
        return Addihex
    elif (op == "and"):
        return Andhex
    elif (op == "or"):
        return ORhex
    elif (op == "beq"):
        return  beqhex
    elif (op == "lw"):
        return lwhex
    elif (op == "sw"):
        return swhex
    elif (op == "j"):
        return Jumphex
    else:
        error_ins()


# Takes string, recognizes which register it is & assigns it's binary code
def assign_reg(Reg):
    if (Reg == "$Zero"):
        return Zero
    elif (Reg == "$s0"):
        return s0
    elif (Reg == "$s1"):
        return s1
    elif (Reg == "$s2"):
        return s2
    else:
        error_register()
        return False


# Takes string, recognizes which register it is & assigns it's hex code
def assign_reghex(Reg):
    if (Reg == "$Zero"):
        return Zerohex
    elif (Reg == "$s0"):
        return s0hex
    elif (Reg == "$s1"):
        return s1hex
    elif (Reg == "$s2"):
        return s2hex
    else:
        error_register()
        return False




# converts decimal string to a binary in 2 bit for Itype within range and format
def binary_2bit(op_check, strformat_num):
    num = int(strformat_num)

    if (op_check == "beq" or op_check == "addi" or op_check =="slti" and num > 0 and num < 4):
        r = '{0:02b}'.format(int(num)) #02d formats an integer (d) to a field of minimum width 2 (2),
        return r

    else:
        error_num_outofrange()
        return False


# converts decimal string to a binary in 6 bit for j type within range and format
def binary_6bit(op_check , strformat_num):
    num = int(strformat_num)
    if (op_check == "j" and num > 0 and num < 64):
        r = '{0:06b}'.format(int(num))
        return r

    else:
        error_num_outofrange()
        return 0


def Rtype(op_check, rs_check, rt_check, rd_check):
    op = assign_Op(op_check)
    rs = assign_reg(rs_check)
    rt = assign_reg(rt_check)
    rd = assign_reg(rd_check)

    if (rs != False and rt != False and rd != False):
        binary_str = op + rs + rt + rd

        # writes machine code as op, rs, rt, rd
        write_to_output(binary_str)

    ophex = assign_hexOp(op_check)
    rshex = assign_reghex(rs_check)
    rthex = assign_reghex(rt_check)
    rdhex = assign_reghex(rd_check)
    if (rshex != False and rthex != False and rdhex != False):
        hex_str = ophex + rshex + rthex + rdhex
        write_to_outputhex(hex_str)


def Itype(op_check, rs_check, rt_check, imm_check):
    op = assign_Op(op_check)
    rt = assign_reg(rt_check)
    rs = assign_reg(rs_check)
    imm = binary_2bit(op_check, imm_check)

    if (imm !=False and rs != False and rt != False):
        binary_str = op + rs + rt + imm

        # writes machine code as op, rs, rt, imm
        write_to_output(binary_str)

    ophex = assign_hexOp(op_check)
    rshex = assign_reghex(rs_check)
    rthex = assign_reghex(rt_check)
    if (imm !=False and rshex != False and rthex != False):
        immhex = '{:x}'.format(int(imm, 2))
        hex_str = ophex + rshex + rthex + immhex
        write_to_outputhex(hex_str)


def Jtype(op_check, imm_check):
    op = assign_Op(op_check)
    imm = binary_6bit(op_check,imm_check)

    if (imm != False):
        binary_str = op + imm
        # writes machine code as op, imm
        write_to_output(binary_str)

    ophex = assign_hexOp(op_check)
    if (imm != False):
        immhex = '{:x}'.format(int(imm, 2))
        hex_str = ophex + immhex + "00"
        write_to_outputhex(hex_str)



def wtype(op_check, r1st_check, imm_check, r2nd_check):
    patn = re.sub(r"[([{})\]]", "", r2nd_check)

    op = assign_Op(op_check)
    rt = assign_reg(r1st_check)
    imm = binary_2bit(op_check, imm_check)
    rs = assign_reg(patn)

    if (imm > False and rt != False and rs != False):
        binary_str = op + rs + rt + imm

        # writes machine code as op, rt, rs, imm
        write_to_output(binary_str)

    ophex = assign_hexOp(op_check)
    rthex = assign_reghex(r1st_check)
    rshex = assign_reghex(patn)
    if (imm > False and rthex != False and rshex != False):
        immhex = '{:x}'.format(int(imm, 2))
        hex_str = ophex + rshex + rthex + immhex
        write_to_outputhex(hex_str)


def Main():
    f = open("input.txt", "r")
    line_list = f.readlines()

    for i in range(0, len(line_list)):
        word_list = line_list[i].split()
        # print(word_list)

        if (len(word_list) == 4):

            if (word_list[0] == "add" or word_list[0] == "sub"or word_list[0] == "and" or word_list[0] == "or"):
                Rtype(word_list[0], word_list[1], word_list[2], word_list[3])

            elif (word_list[0] == "addi" or word_list[0] == "slti" or word_list[0] == "beq"):
                Itype(word_list[0], word_list[1], word_list[2], word_list[3])

            elif (word_list[0] == "lw" or word_list[0] == "sw"):
                wtype(word_list[0], word_list[1], word_list[2])

            else:
                error_ins()
                continue


        elif (len(word_list) == 2):

            if (word_list[0] == "j"):
                Jtype(word_list[0], word_list[1])



            else:
                error_ins()
                continue





    f.close()
if __name__ == '__main__':
    Main()
