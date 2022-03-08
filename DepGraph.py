import sys
from enum import Enum
from typing import *
from Instruction import Instruction, OpCode

class DepGraphNode:
    def __init__(self, instruction: Instruction):
        self.id = instruction.id
        self.instruction = instruction
        self.trueDeps = []
        self.antiDeps = []
        self.weight = 0
    
    def __str__(self):
        return f"(W={self.weight}) {str(self.instruction)}"

class DepGraph:
    def __init__(self, instructions: List[Instruction]):
        self.nodes = {}
        self.instructions = instructions

        for ixn in instructions:
            if (str(ixn.id) in self.nodes.keys()):
                continue
            trueDeps = self.findTrueDeps(ixn)
            antiDeps = self.findAntiDeps(ixn)
            node = self.getOrInsertNode(ixn)
            node.trueDeps = trueDeps
            node.antiDeps = antiDeps

    def getOrInsertNode(self, instruction: Instruction) -> DepGraphNode:
        try:
            v = self.nodes[str(instruction.id)]
            return v
        except:
            self.nodes[str(instruction.id)] = DepGraphNode(instruction)
            return self.nodes[str(instruction.id)]

    def findTrueDeps(self, instruction: Instruction) -> List[DepGraphNode]:
        op = instruction.opcode

        trueDeps = []

        # ADD, MUL, SUB, DIV
        if op == OpCode.ADD or op == OpCode.SUB or op == OpCode.MUL or op == OpCode.DIV:
            field1Dep = self.findTrueRegisterDeps(instruction, instruction.field1)
            field2Dep = self.findTrueRegisterDeps(instruction, instruction.field2)

            if (field1Dep == None or field2Dep == None):
                print("findTrueDeps: ADD,SUB,MUL,DIV cannot have None register deps")
                exit(1);

            trueDeps = [field1Dep, field2Dep]

        # LOADI
        elif op == OpCode.LOADI:
            # can't have dependency on an immediate
            return []
        
        # STOREAI
        elif op == OpCode.STOREAI:
            field1Dep = self.findTrueRegisterDeps(instruction, instruction.field1)

            if field1Dep == None:
                print("findTrueDeps: STOREAI cannot have a None field1 dep")
                exit(1)

            trueDeps = [field1Dep]

        # LOADAI
        elif op == OpCode.LOADAI:
            field1Dep = self.findTrueRegisterDeps(instruction, instruction.field1)
            field2Dep = self.findTrueMemoryDeps(instruction, instruction.field2);
            if field1Dep == None:
                print("findTrueDeps: LOADAI cannot have a None field1 dep")
                exit(1)

            if field2Dep == None:
                print("findTrueDeps: LOADAI has a mem dep outside of block - ignoring", file = sys.stderr)
                trueDeps = [field1Dep]
            else:
                trueDeps = [field1Dep, field2Dep]
        
        # OUPUTAI
        elif op == OpCode.OUTPUTAI:
            field1Dep = self.findTrueRegisterDeps(instruction, instruction.field1);
            field2Dep = self.findTrueMemoryDeps(instruction, instruction.field2);
            if (field1Dep == None or field2Dep == None):
                print("findTrueDeps: OUTPUTAI cannot have a None regsiter or memory dep")
                exit(1)

            trueDeps = [field1Dep, field2Dep]
        else:
            print(f"findTrueDeps: OpCode {op} not yet implemented")
            exit(1)
        
        return [self.getOrInsertNode(x) for x in trueDeps]


    def findAntiDeps(self, instruction: Instruction) -> List[DepGraphNode]:
        op = instruction.opcode

        antiDeps = []

        # ADD, SUB, MUL, DIV
        if op == OpCode.ADD or op == OpCode.SUB or op == OpCode.MUL or op == OpCode.DIV:
            field3Dep = self.findAntiRegisterDeps(instruction, instruction.field3)
            if field3Dep:
                antiDeps = [field3Dep]
        # LOADI
        elif op == OpCode.LOADI:
            field3Dep = self.findAntiRegisterDeps(instruction, instruction.field3)
            if field3Dep:
                antiDeps = [field3Dep]

        # OUTPUTAI
        elif op == OpCode.OUTPUTAI:
            # outputAI can't have anti deps
            return []

        # LOADAI
        elif op == OpCode.LOADAI:
            field3Dep = self.findAntiRegisterDeps(instruction, instruction.field3)
            if field3Dep:
                antiDeps = [field3Dep]

        # STOREAI
        elif op == OpCode.STOREAI:
            field3Dep = self.findAntiMemoryDeps(instruction, instruction.field3)
            if field3Dep:
                antiDeps = [field3Dep]
        else:
            print(f"findAntiDeps: OpCode {op} not yet implemented")
            exit(1)

        return [self.getOrInsertNode(x) for x in antiDeps]


    def findTrueRegisterDeps(self, instruction: Instruction, register: int) -> Optional[Instruction]:
        previousIxns = self.getPreviousInstructions(instruction)
        if (previousIxns == None):
            print(f"\t Found no previous ixns for {str(instruction)}", file = sys.stderr)
            return None 

        print(f"previous ixns for finding reg deps for {instruction}", file = sys.stderr)
        for ixn in previousIxns:
            print(f"\t {str(ixn)}", file = sys.stderr)

        for ixn in previousIxns:
            # LOADI
            if ixn.opcode == OpCode.LOADI:
                if ixn.field2 == register:
                    return ixn

            # ADD, SUB, MUL, DIV, LOADAI
            elif ixn.opcode == OpCode.ADD or \
                 ixn.opcode == OpCode.SUB or \
                 ixn.opcode == OpCode.MUL or \
                 ixn.opcode == OpCode.DIV or \
                 ixn.opcode == OpCode.LOADAI:

                    if ixn.field3 == register:
                        return ixn
            # STOREAI
            elif ixn.opcode == OpCode.STOREAI:
                # SKIP
                continue
            # OUTPUTAI
            elif ixn.opcode == OpCode.OUTPUTAI:
                # SKIP
                continue
            else:
                print(f"findTrueRegisterDeps: opcode {ixn.opcode} not yet implemented")
                exit(1)

        return None

    def findTrueMemoryDeps(self, instruction: Instruction, address: int) -> Optional[Instruction]:
        previousIxns = self.getPreviousInstructions(instruction)
        if (previousIxns == None):
            print(f"\t Found no previous mem deps for {str(instruction)}", file = sys.stderr)
            return None
        
        for ixn in previousIxns:
            
            # STOREAI
            if ixn.opcode == OpCode.STOREAI:
                if ixn.field3 == address:
                    return ixn
            # LOADAI
            elif ixn.opcode == OpCode.LOADAI: 
                if ixn.field2 == address:
                    return ixn

            # ADD,SUB,MUL,DIV,LOADI,OUTPUTAI
            elif ixn.opcode == OpCode.ADD or ixn.opcode == OpCode.SUB or \
                 ixn.opcode == OpCode.MUL or ixn.opcode == OpCode.DIV or \
                 ixn.opcode == OpCode.LOADI or ixn.opcode == OpCode.OUTPUTAI:
                # SKIP
                continue
            else:
                print(f"findTrueMemoryDeps: opcode {ixn.opcode} not yet implemented")
                exit(1)

        return None

    def findAntiMemoryDeps(self, instruction: Instruction, address: int) -> Optional[Instruction]:
        previousIxns = self.getPreviousInstructions(instruction)
        if (previousIxns == None):
            print(f"\t Found no previous anti mem deps for {str(instruction)}", file = sys.stderr)
            return None
        
        for ixn in previousIxns:
            # LOADAI
            if ixn.opcode == OpCode.LOADAI:
                if ixn.field2 == address:
                    return ixn
            # OUTPUTAI
            elif ixn.opcode == OpCode.OUTPUTAI: 
                if ixn.field2 == address:
                    return ixn

            # ADD,SUB,MUL,DIV,LOADI,STOREAI
            elif ixn.opcode == OpCode.ADD or ixn.opcode == OpCode.SUB or \
                 ixn.opcode == OpCode.MUL or ixn.opcode == OpCode.DIV or \
                 ixn.opcode == OpCode.LOADI or ixn.opcode == OpCode.STOREAI:
                
                # SKIP
                continue;
            else:
                print(f"findAntiMemoryDeps: opcode {ixn.opcode} not yet implemented")
                exit(1)

        return None

    def findAntiRegisterDeps(self, instruction: Instruction, register: int) -> Optional[Instruction]: 
        previousIxns = self.getPreviousInstructions(instruction)
        if (previousIxns == None):
            print(f"\t Found no previous ixns for {str(instruction)}", file = sys.stderr)
            return None 

        print(f"previous ixns for finding anti reg deps for {instruction}", file = sys.stderr)
        for ixn in previousIxns:
            print(f"\t {str(ixn)}", file = sys.stderr)
        
            op = ixn.opcode
            if op == OpCode.LOADI:
                # LOADI cannot be an anti dep
                return None
            
            # ADD, SUB, DIV, MUL
            elif op == OpCode.ADD or op == OpCode.SUB or op == OpCode.MUL or op == OpCode.DIV:
                if ixn.field1 == register or ixn.field2 == register:
                    return ixn
            
            # LOADAI
            elif op == OpCode.LOADAI:
                if ixn.field1 == register:
                    return ixn

            # STOREAI
            elif op == OpCode.STOREAI:
                # SKIP
                continue
            
            # OUTPUTAI
            elif op == OpCode.OUTPUTAI:
                # SKIP
                continue
            else:
                print(f"findAntRegisterDep: opcode {op} not yet implemented");
                exit(1)

        return None

    def getPreviousInstructions(self, instruction: Instruction) -> Optional[List[Instruction]]:
        try:
            reversedIxns = self.instructions[::-1]
            return reversedIxns[reversedIxns.index(instruction) + 1::]
        except:
            return None

    def getLeaves(self) -> List[DepGraphNode]:
        leaves = []
        for node in self.nodes.values():
            if len(node.trueDeps) == 0 and len(node.antiDeps) == 0:
                leaves.append(node)

        return leaves

    def getDependentParents(self, node: DepGraphNode) -> List[DepGraphNode]:
        parents = []

        for trueDep in node.trueDeps:
            parents.append(trueDep)
        
        for antiDep in node.antiDeps:
            parents.append(antiDep)

        return parents

    def getDependents(self, node: DepGraphNode) -> List[DepGraphNode]:
        deps = []

        for candidate in self.nodes.values():
            trueDepIds = [x.id for x in candidate.trueDeps]
            antiDepIds = [x.id for x in candidate.antiDeps]
            if node.id in trueDepIds or node.id in antiDepIds:
                deps.append(candidate)

        return deps

    def printDebug(self):
        for node in self.getLeaves():
            self._printDebugHelper(node, 0)

    def _printDebugHelper(self, node: DepGraphNode, level: int):
        space = "".join([" " for _ in range(level)])
        print(f"{space}{node}", file = sys.stderr)
        for dep in self.getDependents(node):
            self._printDebugHelper(dep, level + 2)

