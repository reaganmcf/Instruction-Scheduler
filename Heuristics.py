from DepGraph import DepGraph, DepGraphNode
from Instruction import Instruction, OpCode
from random import randint

# NOTE: loadI 1024 => r0 MUST be loaded first no matter what
# as a result, we give it a huge weighting

# Heuristic 1:
# Longest Latency Weighted Path
def longestLatencyWeightedPath(g: DepGraph) -> DepGraph:
    for node in g.getLeaves():
        llwp_helper(g, node)
    return g

def llwp_helper(g: DepGraph, node: DepGraphNode) -> DepGraphNode:
    ixnWeight = getLatency(node.instruction)
    if len(g.getDependents(node)) == 0:
        node.weight = ixnWeight
    else:
        maxDependentWeight = 0
        for dep in g.getDependents(node):
            llwp_helper(g, dep)
            maxDependentWeight = max(maxDependentWeight, dep.weight)
        
        node.weight = maxDependentWeight + ixnWeight

    if node.instruction.id == 0 and node.instruction.opcode == OpCode.LOADI:
        node.weight = 999
        return node

    return node

# Heuristic 2:
# Highest Latency Instruction
def highestLatencyInstruction(g: DepGraph) -> DepGraph:
    for node in g.nodes.values():
        if node.instruction.id == 0 and node.instruction.opcode == OpCode.LOADI:
            node.weight = 999
        else:
            node.weight = getLatency(node.instruction)

    return g

# Heuristic 3:
# Random!
def randomWeights(g: DepGraph) -> DepGraph:
    for node in g.nodes.values():
        if node.instruction.id == 0 and node.instruction.opcode == OpCode.LOADI:
            node.weight = 999
        else:
            node.weight = randint(1, 5)
    return g

def getLatency(instruction: Instruction) -> int:
    op = instruction.opcode

    if op == OpCode.ADD or op == OpCode.SUB:
        return 1
    elif op == OpCode.MUL or op == OpCode.DIV:
        return 3
    elif op == OpCode.LOADI or op == OpCode.OUTPUTAI:
        return 1
    else:
        return 5
