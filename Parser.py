import sys
from typing import *
from Instruction import *

next_instruction_id = 0

def parse() -> List[Instruction]:
    instructions = list()

    lines = sys.stdin.readlines()
    for line in lines:
        ixn = None
        parts = line.replace(',', '').split()
        if (parts[0] == 'loadI'):
            ixn = parse_loadI(parts)
        elif (parts[0] == 'loadAI'):
            ixn = parse_loadAI(parts)
        elif (parts[0] == 'storeAI'):
            ixn = parse_storeAI(parts)
        elif (parts[0] == 'load' or parts[0] == 'store'):
            ixn = parse_load_store(parts)
        elif (parts[0] == 'add' or parts[0] == 'sub' or parts[0] == 'mult' or parts[0] == 'div'):
            ixn = parse_add_sub_mult_div(parts) 
        elif (parts[0] == 'outputAI'):
            ixn = parse_outputAI(parts)

        if (ixn == None):
            print(f"Unsupported instruction: {parts[0]}")
            exit(2)

        instructions.append(ixn)

    return instructions

def parse_loadI(parts: List[str]) -> Instruction:
    global next_instruction_id
    if (parts[0] != "loadI"):
        print(f"ERR: parse_loadI received {parts[0]} on accident")
        exit(1)
    
    if (len(parts) != 4):
        print(f"ERR: parse_loadI has {len(parts)} parts instead of 4.")
        exit(1)
    
    ixn = Instruction (
            next_instruction_id,
            OpCode.LOADI, 
            int(parts[1]), 
            int(parts[3][1::]), 
            -1
        )

    next_instruction_id += 1
    return ixn

def parse_loadAI(parts: List[str]) -> Instruction:
    global next_instruction_id
    if (parts[0] != "loadAI"):
        print(f"ERR: parse_loadAI received {parts[0]} on accident")
        exit(1)
    
    if (len(parts) != 5):
        print(f"ERR: parse_loadAI has {len(parts)} parts instead of 5.")
        exit(1)
    
    ixn = Instruction (
            next_instruction_id,
            OpCode.LOADAI, 
            int(parts[1][1::]), 
            int(parts[2]), 
            int(parts[4][1::])
        )

    next_instruction_id += 1
    return ixn


def parse_storeAI(parts: List[str]) -> Instruction:
    global next_instruction_id
    if (parts[0] != "storeAI"):
        print(f"ERR: parse_storeAI received {parts[0]} on accident")
        exit(1)
    
    if (len(parts) != 5):
        print(f"ERR: parse_storeAI has {len(parts)} parts instead of 5.")
        exit(1)
    
    ixn = Instruction (
            next_instruction_id,
            OpCode.STOREAI, 
            int(parts[1][1::]), 
            int(parts[3][1::]), 
            int(parts[4])
        )

    next_instruction_id += 1
    return ixn

def parse_add_sub_mult_div(parts: List[str]) -> Instruction:
    global next_instruction_id
    if (parts[0] != "add" and parts[0] != "sub" and parts[0] != "mult" and parts[0] != "div"):
        print(f"ERR: parse_add_sub_mult_div received {parts[0]} on accident")
        exit(1)
    
    if (len(parts) != 5):
        print(f"ERR: parse_storeAI has {len(parts)} parts instead of 5.")
        exit(1)

    op = OpCode.ADD if parts[0] == 'add' else \
            OpCode.SUB if parts[0] == 'sub' else \
                OpCode.MUL if parts[0] == 'mult' else \
                    OpCode.DIV
    
    ixn = Instruction (
            next_instruction_id,
            op,
            int(parts[1][1::]), 
            int(parts[2][1::]), 
            int(parts[4][1::])
        )

    next_instruction_id += 1
    return ixn


def parse_load_store(parts: List[str]) -> Instruction:
    global next_instruction_id
    if (parts[0] != "store" and parts[0] != "load"):
        print(f"ERR: parse_load_store received {parts[0]} on accident")
        exit(1)
    
    if (len(parts) != 4):
        print(f"ERR: parse_load_store has {len(parts)} parts instead of 4.")
        exit(1)

    op = OpCode.LOAD if parts[0] == 'load' else OpCode.STORE
    
    ixn = Instruction (
            next_instruction_id,
            op,
            int(parts[1][1::]), 
            int(parts[3][1::]), 
            -1
        )

    next_instruction_id += 1
    return ixn

def parse_outputAI(parts: List[str]) -> Instruction:
    global next_instruction_id
    if (parts[0] != "outputAI"):
        print(f"ERR: parse_outputAI received {parts[0]} on accident")
        exit(1)
    
    if (len(parts) != 3):
        print(f"ERR: parse_outputAI has {len(parts)} parts instead of 3.")
        exit(1)
    
    ixn = Instruction (
            next_instruction_id,
            OpCode.OUTPUTAI, 
            int(parts[1][1::]), 
            int(parts[2]), 
            -1
        )

    next_instruction_id += 1
    return ixn

if __name__ == '__main__':
    parse()
