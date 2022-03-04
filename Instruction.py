from enum import Enum
class OpCode(Enum):
    LOADI = 0
    LOADAI = 1
    LOAD = 2
    STOREAI = 3
    STORE = 4
    ADD = 5
    SUB = 6
    MUL = 7
    DIV = 8
    OUTPUTAI = 9

class Instruction:
    def __init__(self, id: int, opcode: OpCode, field1: int, field2: int, field3: int):
        self.id = id
        self.opcode = opcode
        self.field1 = field1
        self.field2 = field2
        self.field3 = field3

    def __str__(self):
        if (self.opcode == OpCode.LOAD):
            return f"(id={self.id}) load r{self.field1} => r{self.field2}"
        elif (self.opcode == OpCode.LOADI):
            return f"(id={self.id}) loadI {self.field1} => r{self.field2}"
        elif (self.opcode == OpCode.LOADAI):
            return f"(id={self.id}) loadAI r{self.field1}, {self.field2} => r{self.field3}"
        elif (self.opcode == OpCode.STORE):
            return f"(id={self.id}) store r{self.field1} => r{self.field2}"
        elif (self.opcode == OpCode.STOREAI):
            return f"(id={self.id}) storeAI r{self.field1} => r{self.field2}, {self.field3}"
        elif (self.opcode == OpCode.ADD):
            return f"(id={self.id}) add r{self.field1}, r{self.field2} => r{self.field3}"
        elif (self.opcode == OpCode.SUB):
            return f"(id={self.id}) sub r{self.field1}, r{self.field2} => r{self.field3}"
        elif (self.opcode == OpCode.MUL):
            return f"(id={self.id}) mult r{self.field1}, r{self.field2} => r{self.field3}"
        elif (self.opcode == OpCode.DIV):
            return f"(id={self.id}) div r{self.field1}, r{self.field2} => r{self.field3}"
        else:
            return f"(id={self.id}) outputAI r{self.field1} {self.field2}"
