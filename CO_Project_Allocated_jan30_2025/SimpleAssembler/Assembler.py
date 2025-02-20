import sys

class PC:
    next = 0
    def __init__(self, ins):
        self.ins = ins
        self.index = 0
        self.tokens_in_ins = []
        self.index += PC.next
        PC.next += 4
    def covert_to_tokens(self):
        word = ""
        for it2 in self.ins:
            if it2 == ' ' or it2 == ',' or it2 == '(' or it2 == ')':
                if word == " ":
                    continue
                elif word != " " and word != "":
                    self.tokens_in_ins.append(word)
                    word = ""
            else:
                word += it2
        if word != "":
            self.tokens_in_ins.append(word)
            word = ""

    def check_and_correct_R(self, ins_type, register_enco):
        if (self.tokens_in_ins[0] not in ins_type) or (self.tokens_in_ins[1] not in register_enco) or (self.tokens_in_ins[2] not in register_enco) or (self.tokens_in_ins[3] not in register_enco):
            print("Condition failed in R type instruction : " + self.tokens_in_ins[0] + " " + self.tokens_in_ins[1] + " " + self.tokens_in_ins[2] + " " + self.tokens_in_ins[3])
            return False
        return True

    def check_and_correct_I(self, ins_type, register_enco):
        if self.tokens_in_ins[0] not in ins_type:
            return False
        else:
            if self.tokens_in_ins[0] == "lw":
                if self.tokens_in_ins[1] not in register_enco or self.tokens_in_ins[3] not in register_enco or int(self.tokens_in_ins[2]) > 4095 or int(self.tokens_in_ins[2]) < -4096:
                    return False
            elif self.tokens_in_ins[0] == "jalr" or self.tokens_in_ins[0] == "addi" or self.tokens_in_ins[0] == "sltiu":
                if self.tokens_in_ins[1] not in register_enco or self.tokens_in_ins[2] not in register_enco or int(self.tokens_in_ins[3]) > 4095 or int(self.tokens_in_ins[3]) < -4096:
                    return False
        return True

    def check_and_correct_S(self, ins_type, register_enco):
        if self.tokens_in_ins[0] not in ins_type or self.tokens_in_ins[1] not in register_enco or self.tokens_in_ins[3] not in register_enco or int(self.tokens_in_ins[2]) > 2047 or int(self.tokens_in_ins[2]) < -2048:
            return False
        return True

    def check_and_correct_B(self, ins_type, register_enco):
        if self.tokens_in_ins[0] not in ins_type or self.tokens_in_ins[1] not in register_enco or self.tokens_in_ins[2] not in register_enco or int(self.tokens_in_ins[3]) > 4095 or int(self.tokens_in_ins[3]) < -4096:
            return False
        return True

    def check_and_correct_B(self, ins_type, register_enco, label):
        if self.tokens_in_ins[0] not in ins_type or self.tokens_in_ins[1] not in register_enco or self.tokens_in_ins[2] not in register_enco:
            return False
        return True

    def check_and_correct_U(self, ins_type, register_enco):
        if self.tokens_in_ins[0] not in ins_type or self.tokens_in_ins[1] not in register_enco or int(self.tokens_in_ins[2]) > 2147483647 or int(self.tokens_in_ins[2]) < -2147483648:
            return False
        return True
    def check_and_correct_J(self, ins_type, register_enco, label=None):
        if label is not None:
            if self.tokens_in_ins[0] not in ins_type or self.tokens_in_ins[1] not in register_enco:
                return False
            return True
        else:
            if self.tokens_in_ins[0] not in ins_type or self.tokens_in_ins[1] not in register_enco or int(self.tokens_in_ins[2]) > 1048575 or int(self.tokens_in_ins[2]) < -1048576:
                return False
            return True

    def check_and_correct(self, ins_type, register_enco, label):
        if ins_type[self.tokens_in_ins[0]] == 'R':
            return self.check_and_correct_R(ins_type, register_enco)
        elif ins_type[self.tokens_in_ins[0]] == "I":
            return self.check_and_correct_I(ins_type, register_enco)
        elif ins_type[self.tokens_in_ins[0]] == "S":
            return self.check_and_correct_S(ins_type, register_enco)
        elif ins_type[self.tokens_in_ins[0]] == "B" and self.tokens_in_ins[3] in label:
            return self.check_and_correct_B(ins_type, register_enco, label)
        elif ins_type[self.tokens_in_ins[0]] == "B":
            return self.check_and_correct_B(ins_type, register_enco,label)
        elif ins_type[self.tokens_in_ins[0]] == "U":
            return self.check_and_correct_U(ins_type, register_enco)
        elif ins_type[self.tokens_in_ins[0]] == "J" and self.tokens_in_ins[2] in label:
            return self.check_and_correct_J(ins_type, register_enco, label)
        elif ins_type[self.tokens_in_ins[0]] == "J":
            return self.check_and_correct_J(ins_type, register_enco,label)
        elif ins_type[self.tokens_in_ins[0]] == "A":
            return True
        else:
            return False


opcode = {
    "add": "0110011",
    "sub": "0110011",
    "sll": "0110011",
    "slt": "0110011",
    "sltu": "0110011",
    "xor": "0110011",
    "srl": "0110011",
    "or": "0110011",
    "and": "0110011",
    "addi": "0010011",
    "sltiu": "0010011",
    "lw": "0000011",
    "sw": "0100011",
    "jalr": "1100111",
    "beq": "1100011",
    "bne": "1100011",
    "blt": "1100011",
    "bge": "1100011",
    "bltu": "1100011",
    "bgeu": "1100011",
    "lui": "0110111",
    "auipc": "0010111",
    "jal": "1101111"
}

Register_enco = {
    "zero": "00000",
    "ra": "00001",
    "sp": "00010",
    "gp": "00011",
    "tp": "00100",
    "t0": "00101",
    "t1": "00110",
    "t2": "00111",
    "s0": "01000",
    "s1": "01001",
    "a0": "01010",
    "a1": "01011",
    "a2": "01100",
    "a3": "01101",
    "a4": "01110",
    "a5": "01111",
    "a6": "10000",
    "a7": "10001",
    "s2": "10010",
    "s3": "10011",
    "s4": "10100",
    "s5": "10101",
    "s6": "10110",
    "s7": "10111",
    "s8": "11000",
    "s9": "11001",
    "s10": "11010",
    "s11": "11011",
    "t3": "11100",
    "t4": "11101",
    "t5": "11110",
    "t6": "11111"
}

funct3 = {
    "add": "000",
    "sub": "000",
    "sll": "001",
    "slt": "010",
    "sltu": "011",
    "xor": "100",
    "srl": "101",
    "or": "110",
    "and": "111",
    "addi": "000",
    "sltiu": "011",
    "lw": "010",
    "sw": "010",
    "jalr": "000",
    "beq": "000",
    "bne": "001",
    "blt": "100",
    "bge": "101",
    "bltu": "110",
    "bgeu": "111",
    "lui": "000",
    "auipc": "000",
    "jal": "000"
}

funct7 = {
    "add": "0000000",
    "sub": "0100000",
    "sll": "0000000",
    "slt": "0000000",
    "sltu": "0000000",
    "xor": "0000000",
    "srl": "0000000",
    "or": "0000000",
    "and": "0000000"
}

ins_type = {
    "add": 'R',
    "sub": 'R',
    "sll": 'R',
    "slt": 'R',
    "sltu": 'R',
    "xor": 'R',
    "srl": 'R',
    "or": 'R',
    "and": 'R',
    "addi": 'I',
    "sltiu": 'I',
    "sw": 'S',
    "lw": 'I',
    "jalr": 'I',
    "beq": 'B',
    "bne": 'B',
    "blt": 'B',
    "bge": 'B',
    "bltu": 'B',
    "bgeu": 'B',
    "lui": 'U',
    "auipc": 'U',
    "jal": 'J',
    "mul": 'A',
    "rst": 'A',
    "halt": 'A',
    "rvrs": 'A',
}

register_storage = {
    "zero": 0,
    "ra": 0,
    "sp": 0,
    "gp": 0,
    "tp": 0,
    "t0": 0,
    "t1": 0,
    "t2": 0,
    "s0": 0,
    "s1": 0,
    "a0": 0,
    "a1": 0,
    "a2": 0,
    "a3": 0,
    "a4": 0,
    "a5": 0,
    "a6": 0,
    "a7": 0,
    "s2": 0,
    "s3": 0,
    "s4": 0,
    "s5": 0,
    "s6": 0,
    "s7": 0,
    "s8": 0,
    "s9": 0,
    "s10": 0,
    "s11": 0,
    "t3": 0,
    "t4": 0,
    "t5": 0,
    "t6": 0
}
program = []
file = open(f"{sys.argv[1]}", "r")
line = file.readline()
while line:
    program.append(PC(line.strip()))
    line = file.readline()
file.close()
error = False
label = {}
for it in program:
    it.covert_to_tokens()
    print(it.index, it.tokens_in_ins)
for it in program:
    if ((it.tokens_in_ins[0])[len(it.tokens_in_ins[0]) - 1] == ':'):
        label[it.tokens_in_ins[0][:len(it.tokens_in_ins[0]) - 1]] = it.index
        print(it.tokens_in_ins[0][:len(it.tokens_in_ins[0]) - 1], "   " ,it.index)
        it.tokens_in_ins.pop(0)
    else:
        
        temp = ins_type[it.tokens_in_ins[0]]
        print(temp)
        if temp != 'R' and temp != "S" and temp != "U" and temp != "I" and temp != "B" and temp != "J" and temp != "A":
            error = True
            print("Error in the instruction at Line", it.index / 4)
            break
for it in label:
    print(it, label[it])
file2 = open(f"{sys.argv[2]}", "w")
for it in program:
    if (error != True) and (it.check_and_correct(ins_type, Register_enco, label) == False):
        error = True
        print("Error in the instruction at Line", it.index / 4)
        break
if error == False:
    if error == False and program[len(program) - 1].tokens_in_ins[0] != "beq" and program[len(program) - 1].tokens_in_ins[1] != "zero" and program[len(program) - 1].tokens_in_ins[2] != "zero" and program[len(program) - 1].tokens_in_ins[3] != "0":
        error = True
        print("ERROR : beq zero,zero,0 -- Missing from program")
if error == False:
    for it in program:
        temp_binary = ""
        if ins_type[it.tokens_in_ins[0]] == "R":
            temp_binary += funct7[it.tokens_in_ins[0]]
            temp_binary += Register_enco[it.tokens_in_ins[3]]
            temp_binary += Register_enco[it.tokens_in_ins[2]]
            temp_binary += funct3[it.tokens_in_ins[0]]
            temp_binary += Register_enco[it.tokens_in_ins[1]]
            temp_binary += opcode[it.tokens_in_ins[0]]
        elif ins_type[it.tokens_in_ins[0]] == "B":
            data = ""
            if it.tokens_in_ins[3] in label:
                offset = label[it.tokens_in_ins[3]] - it.index
                offset = int(offset)
                if offset < 0:
                    imm = bin(offset & 0xFFF)[3:]  # Take the least significant 12 bits for negative offsets
                    imm = '1' * (13 - len(imm)) + imm  # Fill leading bits with 1s for negative offset
                else:
                    imm = bin(offset)[2:].zfill(13)  # Convert positive offset to binary and pad with zeros if necessary
            else:
                offset = int(it.tokens_in_ins[3])
                if offset < 0:
                    imm = bin(offset & 0xFFF)[3:]  # Take the least significant 12 bits for negative offsets
                    imm = '1' * (13 - len(imm)) + imm  # Fill leading bits with 1s for negative offset
                else:
                    imm = bin(offset)[2:].zfill(13)  # Convert positive offset to binary and pad with zeros if necessary
data = imm
            temp_binary += data[0]
            for i in range(2, 8):
                temp_binary += data[i]
            temp_binary += Register_enco[it.tokens_in_ins[2]]
            temp_binary += Register_enco[it.tokens_in_ins[1]]
            temp_binary += funct3[it.tokens_in_ins[0]]
            for i in range(8, 12):
                temp_binary += data[i]
            temp_binary += data[1]
            temp_binary += opcode[it.tokens_in_ins[0]]
        elif ins_type[it.tokens_in_ins[0]] == "U":
            if it.tokens_in_ins[2] in label:
                offset = it.index - label[it.tokens_in_ins[2]]
                data = bin(offset)[2:].zfill(32)
            else:
                offset = int(it.tokens_in_ins[2])
                if offset < 0:
                    imm = bin(offset & 0xFFF)[3:]  # Take the least significant 12 bits for negative offsets
                    imm = '1' * (32 - len(imm)) + imm  # Fill leading bits with 1s for negative offset
                else:
                    imm = bin(offset)[2:].zfill(32)  # Convert positive offset to binary and pad with zeros if necessary
            data = imm[0:20]
            temp_binary += data
            temp_binary += Register_enco[it.tokens_in_ins[1]]
            temp_binary += opcode[it.tokens_in_ins[0]]
